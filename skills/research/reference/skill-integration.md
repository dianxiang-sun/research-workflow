# Skill Integration

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

| Situation | Delegates to |
|-----------|-------------|
| 3+ papers batch | `/map-reduce-papers` + `/canary-check` |
| Single paper | `/speed-read` |
| Writing statistics | `/verify-before-write` |
| Citation check | `/verify-citations` |
| Doc quality | `/pipeline-review` |
| Architecture | `/architecture-review` |
| Batch tasks | `/disk-first-batch` + `/canary-check` |
| Session end | `/session-checkpoint` |
| Literature search (automated) | Semantic Scholar MCP (if installed) |
| Deep recursive research | GPT-Researcher MCP (if installed) |

### MCP Integrations (Optional, Enhance Capabilities)

Install for enhanced automation:
- **Semantic Scholar**: Add to `~/.claude/.mcp.json` — enables automated paper search, citation tracing
- **GPT-Researcher**: Deep recursive research with auto-report generation

The skill works without these MCPs but degrades to manual search.
When MCPs are available, `/research explore` and `/research novelty-watch` auto-use them.
