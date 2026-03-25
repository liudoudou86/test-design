#!/usr/bin/env python3

import argparse
import json
from typing import Optional

from jira import JIRA


class JiraIssueParser:
    def __init__(self, server_url: str, username: str, password: str):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.jira = None

    def connect(self):
        for api_version in ["3", "2"]:
            try:
                options = {"server": self.server_url, "rest_api_version": api_version}
                self.jira = JIRA(options, basic_auth=(self.username, self.password))
                self.jira.current_user()
                print(f"成功连接到 Jira: {self.server_url} (API v{api_version})")
                return True
            except Exception as e:
                if api_version == "2":
                    print(f"连接失败: {e}")
                    return False
                continue
        return False

    def get_issue(self, issue_key: str) -> Optional[dict]:
        try:
            issue = self.jira.issue(issue_key)
            return self._parse_issue(issue)
        except Exception as e:
            print(f"获取 Issue 失败: {e}")
            return None

    def _parse_issue(self, issue) -> dict:
        fields = issue.fields

        parsed = {
            "key": issue.key,
            "summary": fields.summary,
            "description": fields.description or "",
            "issue_type": fields.issuetype.name,
            "status": fields.status.name,
            "priority": fields.priority.name if fields.priority else None,
            "assignee": fields.assignee.displayName if fields.assignee else None,
            "reporter": fields.reporter.displayName if fields.reporter else None,
            "created": fields.created,
            "updated": fields.updated,
            "labels": fields.labels or [],
        }

        if hasattr(fields, "components") and fields.components:
            parsed["components"] = [c.name for c in fields.components]

        if hasattr(fields, "versions") and fields.fixVersions:
            parsed["fix_versions"] = [v.name for v in fields.fixVersions]

        if hasattr(fields, "attachment") and fields.attachment:
            parsed["attachments"] = [
                {"filename": a.filename, "content": a.content}
                for a in fields.attachment
            ]

        custom_fields = {}
        for field_name in dir(fields):
            if field_name.startswith("customfield_"):
                value = getattr(fields, field_name)
                if value:
                    custom_fields[field_name] = str(value)
        if custom_fields:
            parsed["custom_fields"] = custom_fields

        return parsed

    def search_issues(self, jql: str, max_results: int = 50) -> list:
        try:
            issues = self.jira.search_issues(jql, maxResults=max_results)
            return [self._parse_issue(issue) for issue in issues]
        except Exception as e:
            print(f"搜索失败: {e}")
            return []


def main(
    url: str,
    username: str,
    password: str,
    input_key: str,
    jql: bool = False,
    max_results: int = 50,
    output: Optional[str] = None,
):
    parser_instance = JiraIssueParser(url, username, password)

    if not parser_instance.connect():
        exit(1)

    if jql:
        results = parser_instance.search_issues(input_key, max_results)
        output_data = {"query": input_key, "count": len(results), "issues": results}
    else:
        result = parser_instance.get_issue(input_key)
        if result:
            output_data = result
        else:
            print(f"未找到 Issue: {input_key}")
            exit(1)

    output_json = json.dumps(output_data, ensure_ascii=False, indent=2)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"结果已保存到: {output}")
    else:
        print(output_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="解析 Jira Issue")
    parser.add_argument("issue_key", help="Jira Issue Key (如: YYSYBTB-3489)")
    parser.add_argument("--jql", action="store_true", help="将输入作为 JQL 查询处理")
    parser.add_argument(
        "--max-results", type=int, default=50, help="JQL 查询最大结果数 (默认: 50)"
    )
    parser.add_argument("--output", "-o", help="输出文件路径 (默认: 打印到控制台)")

    args = parser.parse_args()

    JIRA_URL = "https://jira.tasly.com/jira"
    JIRA_USERNAME = ""
    JIRA_PASSWORD = ""

    main(
        url=JIRA_URL,
        username=JIRA_USERNAME,
        password=JIRA_PASSWORD,
        input_key=args.issue_key,
        jql=args.jql,
        max_results=args.max_results,
        output=args.output,
    )
