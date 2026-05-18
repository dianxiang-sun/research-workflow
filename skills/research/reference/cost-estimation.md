# Cost Estimation

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

```
Total = Σ(method × N × trials + Σ baselines + Σ ablations) × multiplier + debug(20%)

Multipliers: first-time=3.0×  familiar=1.5×  rerun=1.1×
Time: implementation=estimate×2  writing=2-4wk  review=1-2wk/round
Per-model: estimate per-token cost × avg prompt length × N
```

Track: `| Experiment | Estimated | Actual | Δ | Reason |`
Alert if cumulative Δ > 50%.
