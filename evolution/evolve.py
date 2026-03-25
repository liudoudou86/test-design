#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent
FEEDBACK_FILE = SKILL_DIR / "feedback.json"


def load_data():
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": []}


def save_data(data):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_feedback(test_case_id, feedback_type, comment):
    data = load_data()
    entry = {
        "id": test_case_id,
        "feedback_type": feedback_type,
        "comment": comment,
        "timestamp": datetime.now().isoformat(),
        "resolved": False,
    }
    data.setdefault("entries", []).append(entry)
    save_data(data)
    return f"反馈已记录：{feedback_type} - {comment}"


def get_status():
    data = load_data()
    entries = data.get("entries", [])
    by_type = {}
    for e in entries:
        t = e.get("feedback_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
    return {"total": len(entries), "by_type": by_type}


def get_rules():
    """从feedback中提取规则（基于ALL类型的entry）"""
    data = load_data()
    keywords_map = {
        "encoding": "强制使用 UTF-8 with BOM 生成CSV",
        "formatting": "测试步骤使用真实换行符\\n而非<br>标签",
        "missing": "补充遗漏测试点",
        "redundant": "过滤相似模式",
        "格式改进": "前置条件/测试步骤/预期结果使用换行符分隔",
    }
    rules = []
    for entry in data.get("entries", []):
        if entry.get("id") == "ALL":
            rules.append(
                {
                    "type": entry.get("feedback_type"),
                    "action": keywords_map.get(
                        entry.get("feedback_type"), entry.get("comment")
                    ),
                }
            )
    return rules


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: evolve.py <command> [args]")
        print("Commands:")
        print("  status              显示反馈统计")
        print("  add-feedback <ID> <类型> <内容>  添加反馈")
        print("  get-rules           查看当前规则")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "status":
        print(json.dumps(get_status(), ensure_ascii=False, indent=2))
    elif cmd == "add-feedback" and len(sys.argv) >= 5:
        print(add_feedback(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])))
    elif cmd == "get-rules":
        print(json.dumps(get_rules(), ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
