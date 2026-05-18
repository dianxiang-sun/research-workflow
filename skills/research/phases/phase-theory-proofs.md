# Phase: Theory / Formal Proofs

> Replaces Phases 3-5 for `paper_type: theory`.
> Theory papers prove things rather than measuring them empirically.

## When This Phase Activates

After Phase 2 (design — formal problem definition + proof strategy), theory papers enter this phase instead of Phases 3-5. Proceed to Phase 6 (write) after completing this phase.

```
Phase 0 (explore) → Phase 1 (foundation) → Phase 2 (design: formalization) → THIS PHASE → Phase 6 (write) → Phase 7 (review) → Phase 8 (rebuttal)
```

## Protocol

### 1. Theorem Statement Formalization

Before proving anything, state exactly WHAT you're proving:

- **Formal definitions**: Every concept used in the theorem must be precisely defined
- **Assumptions**: List ALL assumptions explicitly (reviewers WILL challenge unstated ones)
- **Theorem statement**: Precise, unambiguous, with quantifiers (∀, ∃) explicit
- **Scope**: What does the theorem apply to? What are the boundary conditions?

**Self-check**: Can someone with only your definitions and assumptions understand the theorem statement without reading the rest of the paper?

### 2. Proof Strategy Selection

Choose approach BEFORE attempting the proof:

| Strategy | When to Use | Key Risk |
|----------|------------|----------|
| **Direct proof** | A → B straightforward | May be tedious; missing a case |
| **Proof by contradiction** | Direct proof seems hard; negation yields useful structure | Subtle errors in negation |
| **Proof by induction** | Structure is recursive or layered | Base case oversight; induction step gap |
| **Proof by construction** | Need to show existence | Construction may not cover all cases |
| **Case analysis** | Problem decomposes into finite cases | Missing a case; cases not exhaustive |
| **Reduction** | Reduce to known result | Reduction must be gap-free |

### 3. Lemma Decomposition

Break the main theorem into smaller, provable lemmas:

```
Theorem 1 (Main Result)
  ├── Lemma 1 (Foundation) — establishes base property
  ├── Lemma 2 (Key Step) — the hard part; likely the novel contribution
  ├── Lemma 3 (Composition) — combines Lemmas 1+2
  └── Proof of Theorem 1 — follows from Lemma 3 + known result X
```

**Rules**:
- Each lemma should be independently verifiable
- Identify which lemma is the HARD one (that's your contribution)
- Easy lemmas may cite known results (don't re-prove standard facts)

### 4. Proof Development

For each lemma/theorem:

1. **Sketch first**: Write a 3-5 sentence proof sketch before the full proof
2. **Identify gaps**: Where does the argument feel hand-wavy? Those are the danger zones
3. **Formalize**: Fill in every step; make sure each step follows logically from the previous
4. **Counterexample search**: Actively try to BREAK your proof
   - Try edge cases on every assumption
   - Try removing each assumption — does the theorem still hold? (if yes, the assumption is unnecessary)
   - Try constructing a counterexample to the theorem itself

### 5. Proof Verification

| Method | Effort | Confidence |
|--------|--------|-----------|
| **Self-review** (re-read after 24h) | Low | Low-Medium |
| **Peer review** (co-author/colleague) | Medium | Medium-High |
| **Formal verification** (Coq, Lean, Isabelle) | High | Very High |
| **Computer search** (for small cases, SAT) | Medium | High (for covered cases) |

**Minimum**: Self-review + peer review. Formal verification for ambitious claims.

### 6. Practical Implications

Theory papers risk the "so what?" critique. Bridge the gap:

- **Constructive proofs**: If your proof is constructive, can you extract an algorithm?
- **Bounds**: If you prove bounds, are they tight? How do they compare to empirical observations?
- **Impossibility results**: If you prove something is impossible, what are the practical implications?
- **Example instantiation**: Show your theorem applied to a concrete, well-known instance

## Emitted Artifact

`Theory & Proofs Record` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Method Design Record (formalization)` → scores `Theory & Proofs Record`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below.

- Every definition is precise and unambiguous?
- All assumptions are explicitly stated?
- Proof strategy is chosen and justified?
- Lemma decomposition identifies the hard part?
- Every proof step follows from previous steps (no hand-waving)?
- Counterexample search conducted and documented?
- At least self-review + one peer review completed?
- Practical implications articulated (not just abstract math)?
