# Writing Memory Protocol (`/research mine-patterns`)

> Extract and reuse writing patterns across papers.
> Inspired by Galaxy-Dawn/claude-scholar's paper-miner concept.

## Purpose
Instead of starting every paper from scratch, mine your previous papers for:
- Sentence patterns that work well (introduction hooks, transition phrases, result reporting)
- Section structures that reviewers praised
- Common academic phrases in your domain
- Your preferred argumentation style

## Protocol

### 1. Pattern Extraction (run on accepted papers)
For each previously written/accepted paper:
1. Read the paper
2. Extract patterns into `.claude/research-writing-memory.md`:

```yaml
# Writing Patterns Memory
## Introduction Hooks
- [pattern]: "Despite significant advances in X, Y remains a critical challenge because Z"
  [source]: ASE 2026 paper, §1 para 1
  [why_it_works]: Acknowledges progress while identifying gap

## Result Reporting
- [pattern]: "RQ1: [Question]. [Direct answer]. [Key number]. [Implication]."
  [source]: ASE 2026 paper, §5.1
  [why_it_works]: Reviewer can skim and get the answer immediately

## Transition Phrases
- "This observation motivates..."
- "To address this limitation, we..."
- "The results suggest that... however..."

## Section Structures
- [Results]: One subsection per RQ → answer first → evidence → analysis → implications
  [source]: ASE 2026 paper
```

### 2. Pattern Application (during writing)
When writing a new paper:
1. Read `.claude/research-writing-memory.md`
2. Adapt (not copy) patterns to new content
3. Maintain consistent voice across papers
4. Add new successful patterns after each paper

### 3. Cross-Paper Consistency
Track recurring phrases/terms across papers to build your "research voice":
- Domain-specific terminology you always use
- Argumentation structures that get praised
- Common disclaimers/caveats you employ
