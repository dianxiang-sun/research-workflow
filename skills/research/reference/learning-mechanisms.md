# Learning Mechanisms

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

### Mechanism 1: Structured Reflection + Predicate Rules (Reflexion + MPR)

After every execution, Claude runs:
```bash
# Log what happened
research-reflect log-reflection \
  --skill <mode> --task "<desc>" --result <success|partial|failure> \
  --what-happened "<text>" --lesson "<text>"

# On failure: extract predicate rule
research-reflect log-rule \
  --phase <N> --rule "IF <condition> THEN <action>" \
  --confidence 0.5 --source <reflection_id>

# When a rule proves correct again: boost its confidence
research-reflect boost-rule --rule-id <id>
```

Rules with confidence ≥ 0.7 become **HARD rules** (mandatory checks).
Rules with confidence < 0.7 are **SOFT rules** (suggestions).
The hook automatically injects hard rules into every invocation.

### Mechanism 2: Outcome Quality Tracking (CrewAI Pattern)

Every execution logs: task → approach → quality score → failure reasons.
```bash
research-reflect log-outcome \
  --skill <mode> --task "<desc>" --approach "<text>" \
  --score <1-5> --failure-reasons "<text>"
```

Before starting a skill, query similar past outcomes for guidance:
```bash
research-reflect query-outcomes --skill <mode> --limit 5
```

### Mechanism 3: Dynamic Shell Injection (Runtime Context)

On every `/research` invocation, Claude runs these to load live context:

```bash
# Recent reflections (avoid repeating mistakes)
research-reflect query-reflections --skill <current_mode> --limit 3

# Applicable rules (inject as additional checks)
research-reflect query-rules --phase <current_phase> --min-confidence 0.3

# Past outcomes (learn from history)
research-reflect query-outcomes --skill <current_mode> --limit 3

# Overall stats (health check)
research-reflect stats
```

These outputs are injected as context BEFORE executing the skill mode.

### Mechanism 4: Three-Tier Memory Architecture (MemGPT/Letta Pattern)

→ See **`reference/capability-memory.md`** — the three-tier memory architecture (Core / Session / Archival).

### Mechanism 5: Semantic Routing (Replaces Keyword Grep)

The `UserPromptSubmit` hook uses TF-IDF semantic matching with learned examples:
```bash
# Route user message to best skill mode
research-router route "<user message>"

# Learn new trigger phrases from usage
research-router add-example \
  --mode <mode> --phrase "<new trigger phrase>"

# View all routes and learned examples
research-router list-routes
```

When user manually invokes a skill (hook didn't fire), Claude should:
1. Ask: "这句话应该触发哪个模式？我来学习一下"
2. Run `add-example` with the user's original phrase
3. Next time similar phrasing appears, hook will match it

### Post-Invocation Protocol

After EVERY `/research` mode execution:

**Always (10 seconds)**:
1. Update `.claude/research-state.yaml` (phase state + the emitted artifact's lifecycle status)
2. Quick score: `reflect.py log-outcome --skill <mode> --task "<desc>" --approach "<text>" --score <1-5>`

**Only on failure/partial (additional steps)**:
3. `reflect.py log-reflection` with lesson learned
4. Consider extracting predicate rule if pattern is generalizable
5. Ask user: "这次有什么没覆盖到的？"

**Only if hook didn't trigger** (user manually invoked skill):
6. Ask what phrase they used → `semantic_router.py add-example`

> Note: On success, do NOT ask "这次有什么没覆盖到的？" — respect the user's flow.
> The full reflection cycle is reserved for when things go WRONG, which is when lessons are most valuable.

### Progress Tracking (`.claude/research-state.yaml`)

Created on `/research init` from `templates/research-state.yaml`. Tracks phase
state, per-phase typed-artifact lifecycle, risks, decisions, and deadline
milestones (schema: `reference/capability-artifacts.md`).

Key behaviors:
- **Auto-update**: each mode updates the `phases:` state and the emitted artifact's lifecycle status
- **`/research status`**: reads `research-state.yaml` → phase / gate / artifact / risk / milestone display
- **Stale detection**: a phase `active` with a long-unmoved `started` date → nudge
- **Gate reminder**: a phase's artifact still `draft` while the phase looks done → "别忘了跑 /research gate"

### `/research evolve` mode:

Monthly self-improvement:
1. `reflect.py stats` → analyze usage patterns
2. Identify soft rules tested 5+ times → promote to hard
3. Identify modes never used → improve triggers or deprecate
4. Identify recurring reflection patterns → propose new phase protocol entries
5. Present proposals to user → apply approved changes to phase files
6. Run `semantic_router.py rebuild-index` after changes
