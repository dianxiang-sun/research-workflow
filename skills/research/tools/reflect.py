#!/usr/bin/env python3
"""
Reflexion + MPR tools for /research skill.
Handles structured reflections, predicate rules, and outcome tracking.

Usage:
  python3 reflect.py log-reflection --skill <mode> --task <desc> --result <success|partial|failure> --what-happened <text> --lesson <text>
  python3 reflect.py log-rule --phase <N> --rule <IF...THEN text> --confidence <0.0-1.0> --source <reflection_id>
  python3 reflect.py log-outcome --skill <mode> --task <desc> --approach <text> --score <1-5> --failure-reasons <text>
  python3 reflect.py query-reflections --skill <mode> [--limit N]
  python3 reflect.py query-rules --phase <N> [--min-confidence 0.5]
  python3 reflect.py query-outcomes --skill <mode> [--limit N]
  python3 reflect.py boost-rule --rule-id <id>
  python3 reflect.py weaken-rule --rule-id <id>
  python3 reflect.py retire-rule --rule-id <id>
  python3 reflect.py export-summary
  python3 reflect.py stats
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import hashlib
import argparse


def _state_dir() -> Path:
    # Runtime state resolves OUTSIDE the skill bundle (M6 §14.4): env override, else default.
    override = os.environ.get("RESEARCH_SKILL_STATE_DIR")
    return Path(override).expanduser() if override else Path.home() / ".claude" / "research" / "memory"


MEMORY_DIR = _state_dir()
REFLECTIONS_FILE = MEMORY_DIR / "reflections.jsonl"
RULES_FILE = MEMORY_DIR / "rules.jsonl"
OUTCOMES_FILE = MEMORY_DIR / "outcomes.jsonl"


def gen_id(prefix: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.md5(f"{ts}{os.getpid()}".encode()).hexdigest()[:6]
    return f"{prefix}-{ts}-{h}"


def append_jsonl(filepath: Path, record: dict):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    records = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def find_duplicate(records: list[dict], candidate: dict, keys: tuple) -> str | None:
    """Return the id of the first record whose every dedup-key field equals the
    candidate's, else None. Content-only — id / timestamp / confidence / counters
    are ignored; values are str()-compared so int/str phase values match."""
    for r in records:
        if all(str(r.get(k)) == str(candidate.get(k)) for k in keys):
            return r.get("id")
    return None


def cmd_log_reflection(args):
    record = {
        "id": gen_id("ref"),
        "timestamp": datetime.now().isoformat(),
        "skill_mode": args.skill,
        "task": args.task,
        "result": args.result,  # success | partial | failure
        "what_happened": args.what_happened,
        "lesson": args.lesson,
        "schema_version": 1,
    }
    append_jsonl(REFLECTIONS_FILE, record)
    print(json.dumps(record, indent=2, ensure_ascii=False))
    # Auto-extract rule if failure
    if args.result == "failure" and args.lesson:
        print("\n[Auto] Consider extracting a predicate rule from this failure.")
        print(f'  python3 reflect.py log-rule --phase {args.skill} --rule "IF ... THEN ..." --confidence 0.5 --source {record["id"]}')


def cmd_log_rule(args):
    record = {
        "id": gen_id("rule"),
        "timestamp": datetime.now().isoformat(),
        "phase": args.phase,
        "rule": args.rule,  # "IF <condition> THEN <action>"
        "confidence": args.confidence,
        "times_tested": 0,
        "times_validated": 0,
        "source": args.source,  # reflection ID or "manual"
        "domain": args.domain,
        "status": "soft" if args.confidence < 0.7 else "hard",
        "schema_version": 1,
    }
    # T5 — dedup on apply: an identical rule (same phase / rule text / domain) is not
    # re-appended; rule strength evolves via boost/weaken-rule, never via re-logging.
    existing = find_duplicate(read_jsonl(RULES_FILE), record, ("phase", "rule", "domain"))
    if existing:
        print(f"[dedup] identical rule already logged as {existing} — not appended; "
              f"use 'boost-rule {existing}' if this recurrence validates it.")
        return
    append_jsonl(RULES_FILE, record)
    print(json.dumps(record, indent=2, ensure_ascii=False))


def cmd_log_outcome(args):
    record = {
        "id": gen_id("out"),
        "timestamp": datetime.now().isoformat(),
        "skill_mode": args.skill,
        "task": args.task,
        "approach": args.approach,
        "score": args.score,  # 1-5
        "failure_reasons": args.failure_reasons,
        "duration_minutes": getattr(args, "duration", None),
        "schema_version": 1,
    }
    append_jsonl(OUTCOMES_FILE, record)
    print(json.dumps(record, indent=2, ensure_ascii=False))


def cmd_query_reflections(args):
    records = read_jsonl(REFLECTIONS_FILE)
    if args.skill:
        records = [r for r in records if r.get("skill_mode") == args.skill]
    records = records[-(args.limit):]
    for r in records:
        status = "✅" if r["result"] == "success" else "⚠️" if r["result"] == "partial" else "❌"
        print(f'{status} [{r["timestamp"][:10]}] {r["skill_mode"]}: {r["lesson"][:80]}')


def cmd_query_rules(args):
    records = read_jsonl(RULES_FILE)
    if args.phase:
        records = [r for r in records if str(r.get("phase")) == str(args.phase)]
    if hasattr(args, 'domain') and args.domain:
        records = [r for r in records if r.get("domain", "*") in ("*", args.domain)]
    records = [r for r in records if r.get("confidence", 0) >= args.min_confidence]
    # Sort by confidence descending
    records.sort(key=lambda r: r.get("confidence", 0), reverse=True)
    for r in records:
        badge = "🔴 HARD" if r.get("status") == "hard" else "🟡 SOFT"
        print(f'{badge} [conf={r["confidence"]:.1f}] {r["rule"][:100]}')


def cmd_query_outcomes(args):
    records = read_jsonl(OUTCOMES_FILE)
    if args.skill:
        records = [r for r in records if r.get("skill_mode") == args.skill]
    records = records[-(args.limit):]
    for r in records:
        stars = "★" * r.get("score", 0) + "☆" * (5 - r.get("score", 0))
        print(f'{stars} [{r["timestamp"][:10]}] {r["skill_mode"]}: {r.get("task", "")[:60]}')
        if r.get("failure_reasons"):
            print(f'     Failures: {r["failure_reasons"][:80]}')


def cmd_boost_rule(args):
    """Increment times_tested and times_validated for a rule, update confidence."""
    records = read_jsonl(RULES_FILE)
    updated = False
    new_records = []
    for r in records:
        if r["id"] == args.rule_id:
            r["times_tested"] = r.get("times_tested", 0) + 1
            r["times_validated"] = r.get("times_validated", 0) + 1
            # Update confidence: Bayesian-ish
            r["confidence"] = min(0.99, r["times_validated"] / max(r["times_tested"], 1))
            r["status"] = "hard" if r["confidence"] >= 0.7 else "soft"
            updated = True
            print(f'Rule {r["id"]} boosted: confidence={r["confidence"]:.2f}, status={r["status"]}')
        new_records.append(r)
    if updated:
        import tempfile
        fd, tmp_path = tempfile.mkstemp(dir=MEMORY_DIR, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                for r in new_records:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            os.replace(tmp_path, RULES_FILE)
        except:
            os.unlink(tmp_path)
            raise
    else:
        print(f"Rule {args.rule_id} not found.")


def cmd_weaken_rule(args):
    """Increment times_tested but NOT times_validated; recalc confidence."""
    records = read_jsonl(RULES_FILE)
    updated = False
    new_records = []
    for r in records:
        if r["id"] == args.rule_id:
            r["times_tested"] = r.get("times_tested", 0) + 1
            # Confidence = validated / tested (do NOT increment validated)
            r["confidence"] = r.get("times_validated", 0) / max(r["times_tested"], 1)
            if r["confidence"] < 0.3:
                r["status"] = "soft"
            updated = True
            print(f'Rule {r["id"]} weakened: confidence={r["confidence"]:.2f}, status={r["status"]}')
            print(json.dumps(r, indent=2, ensure_ascii=False))
        new_records.append(r)
    if updated:
        import tempfile
        fd, tmp_path = tempfile.mkstemp(dir=MEMORY_DIR, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                for r in new_records:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            os.replace(tmp_path, RULES_FILE)
        except:
            os.unlink(tmp_path)
            raise
    else:
        print(f"Rule {args.rule_id} not found.")


def cmd_retire_rule(args):
    """Set rule status to retired and confidence to 0.0."""
    records = read_jsonl(RULES_FILE)
    updated = False
    new_records = []
    for r in records:
        if r["id"] == args.rule_id:
            r["status"] = "retired"
            r["confidence"] = 0.0
            updated = True
            print(f'Rule {r["id"]} retired.')
        new_records.append(r)
    if updated:
        import tempfile
        fd, tmp_path = tempfile.mkstemp(dir=MEMORY_DIR, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                for r in new_records:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            os.replace(tmp_path, RULES_FILE)
        except:
            os.unlink(tmp_path)
            raise
    else:
        print(f"Rule {args.rule_id} not found.")


def cmd_export_summary(args):
    """Print a human-readable markdown summary for /research evolve."""
    reflections = read_jsonl(REFLECTIONS_FILE)
    rules = read_jsonl(RULES_FILE)
    outcomes = read_jsonl(OUTCOMES_FILE)

    print("# Research Skill Summary\n")

    # Overall stats
    print("## Stats")
    print(f"- Reflections: {len(reflections)}")
    print(f"- Rules: {len(rules)} ({sum(1 for r in rules if r.get('status') == 'hard')} hard, {sum(1 for r in rules if r.get('status') == 'soft')} soft, {sum(1 for r in rules if r.get('status') == 'retired')} retired)")
    avg_score = sum(r.get("score", 0) for r in outcomes) / max(len(outcomes), 1)
    print(f"- Outcomes: {len(outcomes)} (avg score: {avg_score:.1f})")
    print()

    # Top 5 most recent reflections
    print("## Recent Reflections (top 5)")
    for r in reflections[-5:]:
        status = "SUCCESS" if r.get("result") == "success" else "PARTIAL" if r.get("result") == "partial" else "FAILURE"
        print(f"- [{status}] **{r.get('skill_mode', '?')}** ({r.get('timestamp', '')[:10]}): {r.get('lesson', '')[:120]}")
    print()

    # All hard rules
    hard_rules = [r for r in rules if r.get("status") == "hard"]
    print(f"## Hard Rules ({len(hard_rules)})")
    for r in hard_rules:
        print(f"- [conf={r.get('confidence', 0):.2f}] {r.get('rule', '')[:120]}")
    print()

    # Top 5 highest-scored outcomes
    sorted_outcomes = sorted(outcomes, key=lambda r: r.get("score", 0), reverse=True)
    print("## Top Outcomes (top 5)")
    for r in sorted_outcomes[:5]:
        print(f"- [score={r.get('score', 0)}] **{r.get('skill_mode', '?')}**: {r.get('task', '')[:100]}")
    print()


def cmd_stats(args):
    reflections = read_jsonl(REFLECTIONS_FILE)
    rules = read_jsonl(RULES_FILE)
    outcomes = read_jsonl(OUTCOMES_FILE)
    print(f"Reflections: {len(reflections)} ({sum(1 for r in reflections if r.get('result') == 'failure')} failures)")
    print(f"Rules: {len(rules)} ({sum(1 for r in rules if r.get('status') == 'hard')} hard, {sum(1 for r in rules if r.get('status') == 'soft')} soft)")
    print(f"Outcomes: {len(outcomes)} (avg score: {sum(r.get('score', 0) for r in outcomes) / max(len(outcomes), 1):.1f})")
    # Per-skill breakdown
    if outcomes:
        from collections import Counter
        mode_counts = Counter(r.get("skill_mode") for r in outcomes)
        print("\nPer-mode usage:")
        for mode, count in mode_counts.most_common():
            mode_outcomes = [r for r in outcomes if r.get("skill_mode") == mode]
            avg = sum(r.get("score", 0) for r in mode_outcomes) / len(mode_outcomes)
            print(f"  {mode}: {count} uses, avg score {avg:.1f}")


def main():
    parser = argparse.ArgumentParser(description="Research skill reflection & learning tools")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("log-reflection")
    p.add_argument("--skill", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--result", required=True, choices=["success", "partial", "failure"])
    p.add_argument("--what-happened", required=True)
    p.add_argument("--lesson", required=True)

    p = sub.add_parser("log-rule")
    p.add_argument("--phase", required=True)
    p.add_argument("--rule", required=True)
    p.add_argument("--confidence", type=float, default=0.5)
    p.add_argument("--source", default="manual")
    p.add_argument("--domain", default="*", help="Domain scope for this rule (* = global)")

    p = sub.add_parser("log-outcome")
    p.add_argument("--skill", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--approach", required=True)
    p.add_argument("--score", type=int, required=True, choices=[1, 2, 3, 4, 5])
    p.add_argument("--failure-reasons", default="")
    p.add_argument("--duration", type=float, default=None, help="Duration in minutes")

    p = sub.add_parser("query-reflections")
    p.add_argument("--skill", default=None)
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("query-rules")
    p.add_argument("--phase", default=None)
    p.add_argument("--min-confidence", type=float, default=0.0)
    p.add_argument("--domain", default=None, help="Filter rules by domain (* matches all)")

    p = sub.add_parser("query-outcomes")
    p.add_argument("--skill", default=None)
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("boost-rule")
    p.add_argument("--rule-id", required=True)

    p = sub.add_parser("weaken-rule")
    p.add_argument("--rule-id", required=True)

    p = sub.add_parser("retire-rule")
    p.add_argument("--rule-id", required=True)

    sub.add_parser("export-summary")

    sub.add_parser("stats")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {
        "log-reflection": cmd_log_reflection,
        "log-rule": cmd_log_rule,
        "log-outcome": cmd_log_outcome,
        "query-reflections": cmd_query_reflections,
        "query-rules": cmd_query_rules,
        "query-outcomes": cmd_query_outcomes,
        "boost-rule": cmd_boost_rule,
        "weaken-rule": cmd_weaken_rule,
        "retire-rule": cmd_retire_rule,
        "export-summary": cmd_export_summary,
        "stats": cmd_stats,
    }[args.command](args)


if __name__ == "__main__":
    main()
