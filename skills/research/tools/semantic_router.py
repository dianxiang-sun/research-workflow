#!/usr/bin/env python3
"""
Semantic Router for /research skill — embedding-based intent matching.
Falls back to keyword matching if no embeddings available.

Uses TF-IDF vectors (no external API needed) for lightweight semantic matching.
Can be upgraded to OpenAI/sentence-transformers embeddings for higher quality.

Usage:
  python3 semantic_router.py route "<user message>"
  python3 semantic_router.py add-example --mode <mode> --phrase "<trigger phrase>"
  python3 semantic_router.py list-routes
  python3 semantic_router.py rebuild-index
"""

import json
import os
import sys
import argparse
import re
import math
from pathlib import Path
from collections import Counter


def _state_dir() -> Path:
    # Runtime state resolves OUTSIDE the skill bundle (M6 §14.4): env override, else default.
    override = os.environ.get("RESEARCH_SKILL_STATE_DIR")
    return Path(override).expanduser() if override else Path.home() / ".claude" / "research" / "memory"


ROUTES_FILE = _state_dir() / "routes.json"

# Default routes with example phrases per mode
DEFAULT_ROUTES = {
    "explore": {
        "description": "方向探索: 文献全景、gap分析、方向决策",
        "examples": [
            "research direction", "方向探索", "gap analysis", "文献调研",
            "literature survey", "literature review", "what to research",
            "研究方向", "选题", "topic selection", "what's been done",
            "有哪些相关工作", "这个领域的现状", "research landscape",
            "找一个好的研究方向", "哪个方向值得做"
        ]
    },
    "foundation": {
        "description": "问题奠基: 深读、motivation、RQ 制定",
        "examples": [
            "deep read", "深读", "motivation", "RQ", "research question",
            "研究问题", "问题定义", "problem formulation", "为什么这个问题重要",
            "动机", "痛点", "how to formulate RQ", "贡献点"
        ]
    },
    "design": {
        "description": "方法设计: novelty 压力测试、设计溯源",
        "examples": [
            "框架设计", "framework design", "method design", "方法设计",
            "system design", "novelty", "创新点", "新颖性", "技术路线",
            "设计方案", "架构", "how to design", "设计决策"
        ]
    },
    "eval-design": {
        "description": "评估设计: 数据集、指标、baseline、消融（最关键 Gate）",
        "examples": [
            "评估设计", "evaluation design", "实验设计", "experiment design",
            "baseline", "消融", "ablation", "数据集", "dataset", "metric",
            "指标", "怎么评估", "how to evaluate", "实验方案", "对比实验",
            "ground truth", "oracle", "公平比较"
        ]
    },
    "implement": {
        "description": "工程实现: 设计-代码对齐、测试、代码冻结",
        "examples": [
            "sprint", "实现", "implement", "code freeze", "代码冻结",
            "依赖锁定", "开始写代码", "coding", "TDD", "测试"
        ]
    },
    "experiment": {
        "description": "实验执行: 监控、诚实分析、成本追踪",
        "examples": [
            "跑实验", "run experiment", "实验结果", "experiment result",
            "baseline result", "cost tracking", "成本追踪", "开始实验",
            "实验监控", "结果分析", "跑完了"
        ]
    },
    "write": {
        "description": "论文写作: 叙事弧线、claim溯源、页面预算、Threats",
        "examples": [
            "写论文", "write paper", "论文写作", "write section",
            "LaTeX", "写作", "draft", "related work", "threats to validity",
            "摘要", "abstract", "introduction", "写 §", "开始写",
            "motivating example", "conclusion", "discussion"
        ]
    },
    "review": {
        "description": "模拟评审: 多视角审稿人、弱点分类、venue checklist",
        "examples": [
            "审稿", "review", "模拟评审", "simulated review", "peer review",
            "投稿", "submit", "submission checklist", "查缺补漏",
            "帮我审审", "看看有没有问题", "投稿前检查", "审查论文"
        ]
    },
    "rebuttal": {
        "description": "投稿后: reviewer 回复、camera-ready、转投策略",
        "examples": [
            "rebuttal", "回复审稿", "reviewer response", "camera ready",
            "转投", "venue pivot", "reject", "revision", "审稿意见",
            "修改意见", "major revision", "minor revision"
        ]
    },
    "gate": {
        "description": "对抗性 Gate: 站在审稿人角度找致命伤",
        "examples": [
            "硬伤", "fatal flaw", "致命", "审稿人会怎么说", "reviewer will",
            "能不能扛住", "weakness", "stand up to review", "pre-mortem",
            "有没有硬伤", "弱点", "致命缺陷", "会被拒吗"
        ]
    },
    "risk": {
        "description": "风险登记: 查看/更新已知风险和缓解策略",
        "examples": [
            "风险", "risk", "已知弱点", "known weakness", "limitation",
            "局限", "已知问题", "风险评估"
        ]
    },
    "cost": {
        "description": "成本预估: 含重试乘数的 bottom-up 估算",
        "examples": [
            "成本", "cost", "预算", "budget", "花多少钱",
            "how much cost", "API cost", "实验预算", "费用估算"
        ]
    },
    "novelty-watch": {
        "description": "新颖性监控: 扫描最新文献是否有竞争工作",
        "examples": [
            "有没有人做", "someone already", "竞争", "competing",
            "新颖性侵蚀", "novelty erosion", "最近的论文", "recent paper",
            "有没有类似工作", "被抢了吗"
        ]
    },
    "evolve": {
        "description": "技能进化: 从反思中提取规则、优化skill、自我改进",
        "examples": [
            "evolve", "进化", "improve skill", "优化skill",
            "skill越来越聪明", "自我改进", "update research skill"
        ]
    },
    "pilot": {
        "description": "可行性验证: 5-10个样本快速测试方法是否可行",
        "examples": [
            "pilot", "可行性", "feasibility", "先试试", "小规模测试",
            "能不能跑通", "prototype test", "验证一下", "试跑"
        ]
    },
    "advisor-prep": {
        "description": "导师会议准备: 进度汇报、问题讨论、决策请求",
        "examples": [
            "advisor meeting", "导师会议", "准备汇报", "meeting prep",
            "supervisor update", "和老师开会", "进度汇报", "discuss with advisor",
            "导师反馈", "advisor feedback", "组会"
        ]
    }
}


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric, filter short tokens.
    For CJK tokens > 2 chars, also generates 2-char sliding window bigrams."""
    text = text.lower()
    raw_tokens = re.findall(r'[\w\u4e00-\u9fff]+', text)
    tokens = []
    for t in raw_tokens:
        if len(t) <= 1:
            continue
        tokens.append(t)
        # CJK bigram generation: if token is all CJK and > 2 chars, add 2-char windows
        if len(t) > 2 and all('\u4e00' <= c <= '\u9fff' for c in t):
            for i in range(len(t) - 1):
                bigram = t[i:i+2]
                tokens.append(bigram)
    return tokens


def build_tfidf_index(routes: dict) -> tuple[dict, dict, int]:
    """Build TF-IDF vectors for each route from its examples.
    Uses total number of example phrases as document count for IDF (not number of routes)."""
    # Collect all documents — each example phrase is its own "document" for IDF
    doc_freq = Counter()  # how many example phrases contain each token
    route_vectors = {}
    n_docs = sum(len(data["examples"]) for data in routes.values())

    for mode, data in routes.items():
        # Combine all examples into one document per route for TF
        all_tokens = []
        for phrase in data["examples"]:
            phrase_tokens = set(tokenize(phrase))
            all_tokens.extend(tokenize(phrase))
            for token in phrase_tokens:
                doc_freq[token] += 1
        tf = Counter(all_tokens)
        route_vectors[mode] = tf

    # Compute TF-IDF
    tfidf_vectors = {}
    for mode, tf in route_vectors.items():
        tfidf = {}
        for token, count in tf.items():
            idf = math.log(n_docs / (1 + doc_freq.get(token, 0)))
            tfidf[token] = count * idf
        tfidf_vectors[mode] = tfidf

    return tfidf_vectors, doc_freq, n_docs


def cosine_sim(v1: dict, v2: dict) -> float:
    """Cosine similarity between two sparse vectors."""
    common = set(v1.keys()) & set(v2.keys())
    if not common:
        return 0.0
    dot = sum(v1[k] * v2[k] for k in common)
    mag1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in v2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def load_routes() -> dict:
    """Load routes: merge defaults with user-added examples."""
    routes = dict(DEFAULT_ROUTES)
    if ROUTES_FILE.exists():
        with open(ROUTES_FILE) as f:
            custom = json.load(f)
        for mode, data in custom.items():
            if mode in routes:
                # Merge examples (deduplicate)
                existing = set(routes[mode]["examples"])
                for ex in data.get("examples", []):
                    if ex not in existing:
                        routes[mode]["examples"].append(ex)
            else:
                routes[mode] = data
    return routes


def save_custom_routes(routes: dict):
    """Save only user-added routes/examples (delta from defaults)."""
    custom = {}
    for mode, data in routes.items():
        if mode in DEFAULT_ROUTES:
            default_examples = set(DEFAULT_ROUTES[mode]["examples"])
            new_examples = [e for e in data["examples"] if e not in default_examples]
            if new_examples:
                custom[mode] = {"examples": new_examples}
        else:
            custom[mode] = data
    ROUTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ROUTES_FILE, "w") as f:
        json.dump(custom, f, indent=2, ensure_ascii=False)


def cmd_route(args):
    """Route a user message to the best matching skill mode."""
    query = args.message
    routes = load_routes()
    tfidf_vectors, doc_freq, n_docs = build_tfidf_index(routes)

    # Build query vector using same n_docs for IDF
    query_tokens = tokenize(query)
    query_tf = Counter(query_tokens)
    query_tfidf = {}
    for token, count in query_tf.items():
        idf = math.log(n_docs / (1 + doc_freq.get(token, 0)))
        query_tfidf[token] = count * idf

    # Score all routes
    scores = []
    for mode, vector in tfidf_vectors.items():
        sim = cosine_sim(query_tfidf, vector)
        # Bonus for exact substring match
        for phrase in routes[mode]["examples"]:
            if phrase.lower() in query.lower():
                sim += 0.3
                break
        scores.append((mode, sim, routes[mode]["description"]))

    scores.sort(key=lambda x: x[1], reverse=True)

    # Output top matches above threshold
    threshold = 0.05
    matches = [s for s in scores if s[1] > threshold]

    if matches:
        for mode, sim, desc in matches[:3]:
            confidence = "HIGH" if sim > 0.3 else "MEDIUM" if sim > 0.15 else "LOW"
            print(f"- /research {mode} [{confidence}, {sim:.3f}] — {desc}")
    else:
        # No match
        pass


def cmd_add_example(args):
    """Add a new trigger phrase to a mode."""
    routes = load_routes()
    if args.mode not in routes:
        routes[args.mode] = {"description": f"Custom mode: {args.mode}", "examples": []}
    if args.phrase not in routes[args.mode]["examples"]:
        routes[args.mode]["examples"].append(args.phrase)
        save_custom_routes(routes)
        print(f"Added '{args.phrase}' to {args.mode}. Total examples: {len(routes[args.mode]['examples'])}")
    else:
        print(f"'{args.phrase}' already exists in {args.mode}")


def cmd_remove_example(args):
    """Remove a phrase from a mode's examples in routes.json."""
    routes = load_routes()
    if args.mode not in routes:
        print(f"Mode '{args.mode}' not found.")
        return
    if args.phrase in routes[args.mode]["examples"]:
        routes[args.mode]["examples"].remove(args.phrase)
        save_custom_routes(routes)
        print(f"Removed '{args.phrase}' from {args.mode}. Remaining examples: {len(routes[args.mode]['examples'])}")
    else:
        print(f"'{args.phrase}' not found in {args.mode}")


def cmd_list_routes(args):
    routes = load_routes()
    for mode, data in sorted(routes.items()):
        n_default = len(DEFAULT_ROUTES.get(mode, {}).get("examples", []))
        n_total = len(data["examples"])
        n_learned = n_total - n_default
        learned_tag = f" (+{n_learned} learned)" if n_learned > 0 else ""
        print(f"  {mode}: {n_total} examples{learned_tag} — {data['description']}")


def cmd_rebuild_index(args):
    routes = load_routes()
    tfidf_vectors, _, n_docs = build_tfidf_index(routes)
    total_terms = sum(len(v) for v in tfidf_vectors.values())
    print(f"Index rebuilt: {len(routes)} routes, {n_docs} example phrases, {total_terms} total terms")


def main():
    parser = argparse.ArgumentParser(description="Semantic router for /research skill")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("route")
    p.add_argument("message", help="User message to route")

    p = sub.add_parser("add-example")
    p.add_argument("--mode", required=True)
    p.add_argument("--phrase", required=True)

    p = sub.add_parser("remove-example")
    p.add_argument("--mode", required=True)
    p.add_argument("--phrase", required=True)

    sub.add_parser("list-routes")
    sub.add_parser("rebuild-index")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {"route": cmd_route, "add-example": cmd_add_example,
     "remove-example": cmd_remove_example,
     "list-routes": cmd_list_routes, "rebuild-index": cmd_rebuild_index
    }[args.command](args)


if __name__ == "__main__":
    main()
