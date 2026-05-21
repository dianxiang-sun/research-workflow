#!/usr/bin/env python3
"""
Reflexion + MPR tools for /research skill.
Handles structured reflections, predicate rules, and outcome tracking.

Usage:
  research-reflect log-reflection --skill <mode> --task <desc> --result <success|partial|failure> --what-happened <text> --lesson <text>
                                  [--router-miss-original-phrase <text> --router-miss-expected-mode <mode>
                                   --router-miss-actual-mode <mode> --router-miss-score <0.0-1.0>
                                   --router-miss-threshold <0.0-1.0>]
  research-reflect log-rule --phase <N> --rule <IF...THEN text> --confidence <0.0-1.0> --source <reflection_id>
  research-reflect log-outcome --skill <mode> --task <desc> --approach <text> --score <1-5> --failure-reasons <text>
  research-reflect query-reflections --skill <mode> [--limit N]
  research-reflect query-rules --phase <N> [--min-confidence 0.5]
  research-reflect query-outcomes --skill <mode> [--limit N]
  research-reflect boost-rule --rule-id <id> [--phase <N>]
  research-reflect weaken-rule --rule-id <id> [--phase <N>]
  research-reflect retire-rule --rule-id <id>
  research-reflect export-summary
  research-reflect stats

L8 hard-status guard (boost-rule / weaken-rule):
  status='hard' requires confidence >= 0.7, times_tested >= 3, AND >= 2 distinct
  pass phases (from rules.jsonl validation_events). Without --phase, validation
  events lack phase context and rule cannot harden (stays 'soft'). Boost/weaken
  on retired rules raise an error.

L8 race fix (v4): all rules.jsonl writers (log-rule, boost-rule, weaken-rule,
retire-rule) acquire a persistent POSIX-only fcntl.flock on rules.lock around
their read-modify-write. Windows fails loudly (no silent no-op).
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import hashlib
import argparse
from contextlib import contextmanager

# L8 v4: POSIX fcntl advisory lock for rules.jsonl writers (race fix).
# Windows lacks fcntl — concurrent rules.jsonl mutations will SystemExit loudly
# rather than silently race. Run reflect.py on POSIX (Mac/Linux/WSL).
try:
    import fcntl
except ImportError:
    fcntl = None


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


def _emit_json(records: list[dict]):
    """Emit raw JSONL records after query filters; do not normalize schema,
    truncate fields, or add computed convenience fields."""
    print(json.dumps(records, indent=2, ensure_ascii=False))


def _apply_limit(records: list[dict], limit: int) -> list[dict]:
    if limit < 0:
        raise SystemExit("--limit must be >= 0")
    if limit == 0:
        return records
    return records[-limit:]


def find_duplicate(records: list[dict], candidate: dict, keys: tuple) -> str | None:
    """Return the id of the first record whose every dedup-key field equals the
    candidate's, else None. Content-only — id / timestamp / confidence / counters
    are ignored; values are str()-compared so int/str phase values match."""
    for r in records:
        if all(str(r.get(k)) == str(candidate.get(k)) for k in keys):
            return r.get("id")
    return None


# --- L8: rule strength helpers (boost/weaken) ---

def _upgrade_rule_v2(rule: dict):
    """Ensure rule has validation_events array + schema_version >= 2.
    Legacy v1 rules auto-upgrade on first boost/weaken touch."""
    rule.setdefault("validation_events", [])
    rule["schema_version"] = max(int(rule.get("schema_version", 1)), 2)


def _append_validation(rule: dict, phase, result: str):
    """Append a validation event {phase, ts, result} to rule.validation_events.
    result must be 'pass' or 'fail'. Raises SystemExit if rule is retired
    (use log-rule to create a replacement rule with a new id)."""
    if rule.get("status") == "retired":
        raise SystemExit(
            f"Rule {rule.get('id')} is retired. Create a new rule with "
            f"log-rule (it will receive a new id; update any references) "
            f"instead of boost/weaken on retired rules."
        )
    _upgrade_rule_v2(rule)
    event = {
        "phase": str(phase) if phase is not None else None,
        "ts": datetime.now().isoformat(),
        "result": result,
    }
    rule["validation_events"].append(event)
    if phase is None:
        print(
            "[warn] no --phase provided; rule cannot harden without phase "
            "context (status guard requires >= 2 distinct pass phases).",
            file=sys.stderr,
        )


@contextmanager
def _rules_lock():
    """L8 v4 advisory lock for rules.jsonl read-modify-write.
    All RULES_FILE writers (log-rule, boost-rule, weaken-rule, retire-rule) MUST
    acquire this before reading + writing, else concurrent invocations lose
    updates (round-22 reproducer: 8 parallel boost calls left only 1 event).
    POSIX-only via fcntl.flock; lock file persistent (do not unlink — inode
    reuse can split lock; see Codex round-23 artifact)."""
    if fcntl is None:
        raise SystemExit(
            "rules.jsonl mutation requires POSIX fcntl locking; Windows is "
            "unsupported. Run on Mac/Linux/WSL, or set "
            "RESEARCH_SKILL_STATE_DIR to a POSIX filesystem."
        )
    lock_path = MEMORY_DIR / "rules.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+") as lock_fd:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)


def _recompute_rule_strength(rule: dict):
    """Recompute confidence and status from counters + validation_events.
    Hard-status guard (L8): confidence >= 0.7 AND times_tested >= 3 AND
    >= 2 distinct PASS phases (fail events do NOT contribute to phase diversity)."""
    tested = rule.get("times_tested", 0)
    validated = rule.get("times_validated", 0)
    rule["confidence"] = min(0.99, validated / max(tested, 1))
    pass_phases = {
        e.get("phase") for e in rule.get("validation_events", [])
        if e.get("phase") is not None and e.get("result") == "pass"
    }
    rule["status"] = "hard" if (
        rule["confidence"] >= 0.7
        and tested >= 3
        and len(pass_phases) >= 2
    ) else "soft"


def cmd_log_reflection(args):
    # L8(c): Optional structured router-miss fields (all 5 required together if any given)
    rm_fields = [
        ("original-phrase", args.router_miss_original_phrase),
        ("expected-mode", args.router_miss_expected_mode),
        ("actual-mode", args.router_miss_actual_mode),
        ("score", args.router_miss_score),
        ("threshold", args.router_miss_threshold),
    ]
    rm_provided = [n for n, v in rm_fields if v is not None]
    if rm_provided and len(rm_provided) != len(rm_fields):
        missing = [n for n, v in rm_fields if v is None]
        raise SystemExit(
            "log-reflection: when any --router-miss-* flag is given, ALL 5 are "
            f"required. Missing: {', '.join('--router-miss-' + m for m in missing)}."
        )

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

    if rm_provided:
        # L8(c): validate score + threshold in [0, 1] (catches gross out-of-range typos)
        for fname, fval in [("score", args.router_miss_score),
                            ("threshold", args.router_miss_threshold)]:
            if not (0.0 <= fval <= 1.0):
                raise SystemExit(
                    f"log-reflection: --router-miss-{fname} = {fval} must be in [0, 1]."
                )
        record["router_miss"] = {
            "original_phrase": args.router_miss_original_phrase,
            "expected_mode": args.router_miss_expected_mode,
            "actual_mode": args.router_miss_actual_mode,
            "router_score": args.router_miss_score,
            "router_score_threshold": args.router_miss_threshold,
        }
        record["schema_version"] = 2  # bump on router_miss presence

    append_jsonl(REFLECTIONS_FILE, record)
    print(json.dumps(record, indent=2, ensure_ascii=False))
    # Auto-extract rule if failure
    if args.result == "failure" and args.lesson:
        print("\n[Auto] Consider extracting a predicate rule from this failure.")
        print(f'  research-reflect log-rule --phase {args.skill} --rule "IF ... THEN ..." --confidence 0.5 --source {record["id"]}')


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
    # L8 v4: lock around dedup-check + append to serialize with concurrent boost/weaken/retire.
    with _rules_lock():
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
    limit = args.limit if args.limit is not None else (0 if args.json_output else 10)
    records = _apply_limit(records, limit)
    if args.json_output:
        _emit_json(records)
        return
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
    if args.json_output:
        _emit_json(records)
        return
    for r in records:
        badge = "🔴 HARD" if r.get("status") == "hard" else "🟡 SOFT"
        print(f'{badge} [conf={r["confidence"]:.1f}] {r["rule"][:100]}')


def cmd_query_outcomes(args):
    records = read_jsonl(OUTCOMES_FILE)
    if args.skill:
        records = [r for r in records if r.get("skill_mode") == args.skill]
    limit = args.limit if args.limit is not None else (0 if args.json_output else 10)
    records = _apply_limit(records, limit)
    if args.json_output:
        _emit_json(records)
        return
    for r in records:
        stars = "★" * r.get("score", 0) + "☆" * (5 - r.get("score", 0))
        print(f'{stars} [{r["timestamp"][:10]}] {r["skill_mode"]}: {r.get("task", "")[:60]}')
        if r.get("failure_reasons"):
            print(f'     Failures: {r["failure_reasons"][:80]}')


def cmd_boost_rule(args):
    """Increment times_tested + times_validated, append PASS validation event,
    recompute strength via L8 hard-status guard (see _recompute_rule_strength).
    Raises SystemExit if rule is retired. L8 v4: read-modify-write under
    rules.lock fcntl flock (concurrent-safe with other RULES_FILE writers)."""
    with _rules_lock():
        records = read_jsonl(RULES_FILE)
        updated = False
        new_records = []
        for r in records:
            if r["id"] == args.rule_id:
                r["times_tested"] = r.get("times_tested", 0) + 1
                r["times_validated"] = r.get("times_validated", 0) + 1
                _append_validation(r, args.phase, "pass")
                _recompute_rule_strength(r)
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
    """Increment times_tested only (NOT times_validated), append FAIL validation
    event, recompute strength via L8 hard-status guard. Raises SystemExit if
    rule is retired. L8 v4: read-modify-write under rules.lock fcntl flock."""
    with _rules_lock():
        records = read_jsonl(RULES_FILE)
        updated = False
        new_records = []
        for r in records:
            if r["id"] == args.rule_id:
                r["times_tested"] = r.get("times_tested", 0) + 1
                # DO NOT increment times_validated
                _append_validation(r, args.phase, "fail")
                _recompute_rule_strength(r)
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
    """Set rule status to retired and confidence to 0.0. L8 v4: read-modify-
    write under rules.lock fcntl flock (concurrent-safe with other RULES_FILE
    writers)."""
    with _rules_lock():
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
    parser = argparse.ArgumentParser(prog="research-reflect", description="Research skill reflection & learning tools")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("log-reflection")
    p.add_argument("--skill", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--result", required=True, choices=["success", "partial", "failure"])
    p.add_argument("--what-happened", required=True)
    p.add_argument("--lesson", required=True)
    # L8(c): structured router-miss fields (all 5 required together if any given)
    p.add_argument("--router-miss-original-phrase", default=None,
                   help="L8(c): the phrase the user typed that the router mis-classified")
    p.add_argument("--router-miss-expected-mode", default=None,
                   help="L8(c): the mode the phrase should have routed to")
    p.add_argument("--router-miss-actual-mode", default=None,
                   help="L8(c): the mode the router actually returned (or '<none>' if below threshold)")
    p.add_argument("--router-miss-score", type=float, default=None,
                   help="L8(c): the router similarity score (float in [0, 1])")
    p.add_argument("--router-miss-threshold", type=float, default=None,
                   help="L8(c): the router threshold at miss time (float in [0, 1]; see semantic_router.py)")

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
    p.add_argument("--limit", type=int, default=None,
                   help="Max records; 0 = all. Default: 10, or all with --json.")
    p.add_argument("--json", dest="json_output", action="store_true",
                   help="Output raw records as JSON array (full fields, no truncation).")

    p = sub.add_parser("query-rules")
    p.add_argument("--phase", default=None)
    p.add_argument("--min-confidence", type=float, default=0.0)
    p.add_argument("--domain", default=None, help="Filter rules by domain (* matches all)")
    p.add_argument("--json", dest="json_output", action="store_true",
                   help="Output raw records as JSON array (full fields, no truncation).")

    p = sub.add_parser("query-outcomes")
    p.add_argument("--skill", default=None)
    p.add_argument("--limit", type=int, default=None,
                   help="Max records; 0 = all. Default: 10, or all with --json.")
    p.add_argument("--json", dest="json_output", action="store_true",
                   help="Output raw records as JSON array (full fields, no truncation).")

    p = sub.add_parser("boost-rule")
    p.add_argument("--rule-id", required=True)
    p.add_argument("--phase", type=int, default=None,
                   help="L8(b): phase number where rule was validated. Without --phase, "
                        "rule cannot harden (status guard requires >= 2 distinct pass phases).")

    p = sub.add_parser("weaken-rule")
    p.add_argument("--rule-id", required=True)
    p.add_argument("--phase", type=int, default=None,
                   help="L8(b): phase number where rule failed validation. "
                        "Fail events do not contribute to hard-status pass-phase diversity.")

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
