# Skill Integration

> Reference detail for the `research` skill. `SKILL.md` and the phase files point here.

## Companion commands — optional, not bundled with this plugin

The phase files reference nine `/companion-command` items where they would *enhance* a step. **None of them ship with `research-workflow`** — they are independent commands the user may have installed separately, in another plugin or as personal commands. The skill works without any of them: every reference degrades to an inline manual fallback documented in the corresponding phase file.

| Situation | If the `/command` is available | Inline manual fallback (always available) |
|---|---|---|
| 3+ papers batch | `/map-reduce-papers` + `/canary-check` | Read each paper end-to-end; fill the structured notes table (`phase-1-foundation.md` §1) one row at a time; cap core papers at ≤ 12 |
| Single paper | `/speed-read` | Read end-to-end; same structured notes table |
| Writing statistics | `/verify-before-write` — **G1 hard requirement** | **MUST re-open the source PDF, locate the statistic in context, copy the exact value + unit + sample size, and confirm the surrounding sentence's truth claim** (`phase-1-foundation.md:21` + `phase-6-write.md:102`). Skipping is a G1 (zero-fabrication) violation. |
| Citation check | `/verify-citations` — **G1 hard requirement** | **MUST run the CitationAgent contract** per `reference/capability-critique.md`: ≥ 2 metadata sources + retraction screen + author + title + year match. Skipping is a G1 violation. |
| Doc quality | `/pipeline-review` | Self-review pass against the `phase-7-review.md` rubric |
| Architecture | `/architecture-review` | Self-architecture audit using the G-V-R loop (`reference/capability-critique.md`) |
| Batch tasks | `/disk-first-batch` + `/canary-check` | Manual canary on 5-10 items first, then full batch with checkpoint files |
| Session end | `/session-checkpoint` | Manually update `research-state.yaml` and append to `findings.md` Open Questions |

The two **G1 hard requirement** rows are not optional behavior — only the *command* is optional. The verification itself MUST happen, via the inline fallback whenever the command is unavailable. Silent skipping on "the command isn't installed" is a G1 violation, not a tolerated degradation.

## MCP Integrations (Optional, Enhance Capabilities)

Install for enhanced automation:
- **Semantic Scholar**: Add to `~/.claude/.mcp.json` — enables automated paper search, citation tracing
- **GPT-Researcher**: Deep recursive research with auto-report generation

| Situation | Delegates to |
|-----------|-------------|
| Literature search (automated) | Semantic Scholar MCP (if installed) |
| Deep recursive research | GPT-Researcher MCP (if installed) |

The skill works without these MCPs but degrades to manual search. When MCPs are available, `/research-workflow:research explore` and `/research-workflow:research novelty-watch` auto-use them.
