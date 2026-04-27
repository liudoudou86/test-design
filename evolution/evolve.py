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
    """返回所有 ALL 类型的反馈条目作为规则，由 AI 自行推断"""
    data = load_data()
    rules = [e for e in data.get("entries", []) if e.get("id") == "ALL"]
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
