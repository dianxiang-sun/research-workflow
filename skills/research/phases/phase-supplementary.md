# Phase: Supplementary Materials, Artifacts, Collaboration, and Ethics

> Covers everything surrounding the paper itself: supplementary content, reproducibility artifacts, multi-author workflows, and research ethics.

## Applies to: ALL paper types (sections 3-4 have EMPIRICAL-specific additions)

---

## Section 1: Supplementary Materials Strategy

### What Goes Where
- **Main body**: anything required to understand the contribution and evaluate the claims
- **Appendix (in-paper)**: proofs, extended formulations, detailed algorithm pseudocode that referees need but general readers skip
- **External supplementary**: additional experiments, full result tables, dataset samples, screenshots, extended related work
- **Rule of thumb**: if removing it does not break the paper's argument, it is supplementary

### Structure Template
```
Appendix A: Formal Proofs / Theoretical Details
Appendix B: Additional Experimental Results
  B.1: Full ablation tables
  B.2: Per-category breakdowns
  B.3: Failure case analysis
Appendix C: Implementation Details
  C.1: Hyperparameters and configuration
  C.2: Prompt templates (if LLM-based)
  C.3: Infrastructure and compute details
Appendix D: Dataset Details
  D.1: Construction methodology
  D.2: Sample distribution statistics
  D.3: Licensing and access information
```

### Cross-Referencing Conventions
- Every appendix section must be referenced from the main body at least once
- Use consistent labels: "See Appendix B.2 for full results" (not "see supplementary")
- If supplementary is a separate PDF, number pages continuously or clearly label sections
- Reviewers often skip supplementary — never hide critical information there

---

## Section 2: Artifact Evaluation

### Artifact Contents Checklist
- [ ] Source code (complete, not a subset)
- [ ] Data or instructions to obtain data (respect licensing)
- [ ] Build/install scripts (Makefile, setup.py, requirements.txt)
- [ ] Reproduction scripts: one command to reproduce each table/figure in the paper
- [ ] README.md with structured documentation (see template below)
- [ ] LICENSE file (OSI-approved for reusable badge)
- [ ] Dockerfile or container definition (strongly recommended)
- [ ] Expected output files or checksums for validation

### Anonymization
- Remove personal info: names, emails, internal server paths, API keys
- Grep for: username, home directory paths, organization-specific URLs
- Replace API keys with placeholders: `export OPENAI_API_KEY="your-key-here"`
- Check git history — use `git filter-repo` if secrets were ever committed
- Test the anonymized artifact: clone fresh, grep for identifying info

### README Template
```markdown
# [Paper Title] - Artifact

## Overview
Brief description of what this artifact contains and what it reproduces.

## Requirements
- Hardware: [RAM, GPU, disk space]
- Software: [OS, Python version, key dependencies]
- External: [API keys needed, data downloads, accounts]
- Estimated reproduction time: [X hours/minutes]

## Setup
Step-by-step installation instructions (copy-pasteable commands).

## Reproduction Steps
### Table 1: [Description]
$ bash scripts/reproduce_table1.sh
Expected output: results/table1.csv (should match Table 1 within +/- 0.5%)

### Figure 2: [Description]
$ bash scripts/reproduce_figure2.sh
Expected output: figures/figure2.pdf

## Expected Output
Description of what correct output looks like, with checksums or reference files.

## Troubleshooting
Common issues and their solutions.
```

### Docker Packaging
- Base image: use official language images (python:3.10-slim, not latest)
- Pin ALL dependency versions in requirements.txt (pip freeze output)
- Include a docker-compose.yml if multiple services are needed
- Test on a machine that has never run your code before
- Document GPU passthrough if needed (nvidia-docker)

### Badge Levels
| Badge | Requirement | Key Test |
|-------|-------------|----------|
| **Available** | Archived on persistent platform (Zenodo, Figshare) with DOI | URL works, content matches paper description |
| **Functional** | Documented, exercisable, key results reproducible | Fresh clone + README instructions produce claimed results |
| **Reusable** | Well-structured, extensible, OSI license, exceeds minimal documentation | A stranger could extend your tool for a new dataset/task |

### Blockchain-Specific Reproducibility [DOMAIN:security/blockchain]

Smart contract research has unique reproducibility challenges:

| Challenge | Mitigation |
|-----------|-----------|
| Blockchain state changes over time | Record exact block number; provide fork-state snapshot or instructions |
| RPC endpoint non-determinism | Pin RPC provider + endpoint; document rate limits and fallback |
| Gas price variations | Fix gas price in config; document if results are gas-sensitive |
| Compiler version sensitivity | Pin solc version exactly (e.g., 0.8.24, not ^0.8.0); use solc-select |
| Tool version sensitivity | Pin ALL tools (Slither, Mythril, Foundry) to exact versions |
| EVM version differences | Document target EVM version; test on specified fork |

**Replication package must include**:
- [ ] Exact compiler version + settings (optimizer runs, EVM target)
- [ ] Exact tool versions (not just "Slither" but "Slither 0.10.1")
- [ ] Fork configuration (block number, RPC endpoint, chain)
- [ ] Gas settings used during testing
- [ ] Instructions to reproduce from clean environment

### Test-From-Scratch Validation
Before submission, perform this exact sequence:
1. Create a fresh VM or container (no pre-existing dependencies)
2. Clone the repository from the submission URL
3. Follow the README instructions verbatim (no "oh I also need to do X")
4. Run reproduction scripts and compare output to paper claims
5. Document any discrepancy and fix the README or scripts
6. Repeat until the process is fully self-contained

---

## Section 3: Multi-Author Collaboration Protocol

### Writing Assignment Matrix

| Section | Primary Author | Reviewer 1 | Reviewer 2 | Draft Deadline | Review Deadline |
|---------|---------------|-----------|-----------|----------------|-----------------|
| Abstract | Lead | All | — | D-14 | D-12 |
| Intro | Lead | Co-author A | Advisor | D-21 | D-18 |
| Method | Implementer | Lead | Co-author B | D-21 | D-18 |
| Eval | Experimenter | Implementer | Co-author A | D-14 | D-12 |
| Related Work | Co-author A | Lead | Co-author B | D-14 | D-12 |
| Discussion | Lead | All | — | D-10 | D-8 |

- Each co-author reviews at least 2 sections they did not write
- Reviews are substantive (not just "looks good"): check claims, flow, and missing references

### Shared Editing Platforms

| Platform | Pros | Cons | Best For |
|----------|------|------|----------|
| Overleaf | Real-time collaboration, WYSIWYG preview | Merge conflicts on simultaneous edits, history is opaque | Active co-writing phase (D-21 to D-7) |
| Git + LaTeX | Full version control, branching, blame | No real-time preview, merge conflicts in .tex | Final polish phase (D-7 to D-0), long-term archival |

- Convention: if using Overleaf, export to Git at each milestone (draft, review, camera-ready)
- Never have two authors editing the same section simultaneously without coordination

### Conflict Resolution
- **Framing disagreements**: try both framings in a short paragraph, show to advisor, advisor decides
- **Scope disagreements**: defer to the paper's stated contribution — if it is out of scope, cut it
- **Data interpretation disagreements**: present both interpretations to advisor with supporting evidence
- **Escalation path**: authors discuss -> lead author proposes -> advisor decides (final)

### Contribution Tracking
Use CRediT (Contributor Roles Taxonomy) or equivalent:
- Conceptualization, Methodology, Software, Validation, Formal Analysis, Investigation
- Data Curation, Writing (Original Draft), Writing (Review & Editing), Visualization
- Supervision, Project Administration, Funding Acquisition
- Document contributions EARLY (not at submission time) to avoid disputes

### Communication Cadence
- **Active writing phase**: weekly 30-min sync (progress, blockers, deadline check)
- **Review rounds**: 48-hour turnaround for section reviews (72h max)
- **Final week**: daily async check-in (Slack/email) + one sync call at D-3
- **Shared tracker**: a single document or issue board listing all open items with owners and deadlines

---

## Section 4: Research Ethics Checklist

### Universal (ALL paper types)
- [ ] **Data licensing verified**: commercial use rights? redistribution allowed? attribution required?
- [ ] **No PII in datasets**: personally identifiable information scrubbed or never collected
- [ ] **LLM usage disclosed**: which model(s), which phases of research, how much human oversight, whether outputs were manually verified
- [ ] **Compute footprint estimated**: total GPU-hours, API costs, and estimated carbon (use ML CO2 Impact calculator or similar)
- [ ] **Responsible disclosure**: if findings reveal vulnerabilities (especially in security research), follow coordinated disclosure before publication
- [ ] **Dual-use assessment**: could the method/tool be misused? Document mitigations or limitations
- [ ] **No undisclosed conflicts of interest**: funding sources, corporate affiliations, advisory roles
- [ ] **Open-source compliance**: all dependencies' licenses are compatible with your license
- [ ] **Reproducibility commitment**: artifact available or clear explanation of why not (proprietary data, privacy)

### Responsible Disclosure Protocol [DOMAIN:security]

If your research discovers real vulnerabilities in deployed systems:

**Timeline**:
1. Discovery → Document privately (DO NOT publish or discuss publicly)
2. Within 7 days → Contact vendor/project maintainer via security@/responsible disclosure channel
3. Set 90-day disclosure deadline (industry standard)
4. After vendor response:
   - Vendor acknowledges → coordinate fix timeline
   - Vendor ignores after 90 days → proceed with publication (standard practice)
   - Zero-day with active exploitation → coordinate with CERT/CC

**In the paper**:
- Anonymize vulnerable contracts/addresses unless vendor has patched and agreed to disclosure
- Do NOT include working exploit code — describe the vulnerability class, not the specific exploit
- State clearly: "We followed coordinated disclosure. Vendors were notified on [date]."
- If venue requires: include disclosure timeline in supplementary materials

**CVE Process** (optional but strengthens paper):
- File CVE through MITRE or vendor-specific program
- Reference CVE-ID in paper for traceability

**Red flags to avoid**:
- Publishing zero-day vulnerabilities without vendor notification → ethical violation
- Including contract addresses of unpatched live vulnerabilities → harms users
- Claiming responsible disclosure without evidence of vendor contact → reviewers may check

### [EMPIRICAL] Additional Requirements
- [ ] **IRB/ethics board approval** obtained (or determination of exemption documented)
- [ ] **Informed consent** from all human participants, with clear explanation of data use
- [ ] **Data anonymization protocol** defined and applied before analysis
- [ ] **Participant compensation** disclosed (amount, form) and fair for time required
- [ ] **Right to withdraw**: participants can withdraw data after the study
- [ ] **Data retention plan**: how long is participant data kept? where? who has access?
- [ ] **Demographic reporting**: if relevant, report participant demographics without enabling re-identification

### When In Doubt
- Check your venue's ethics guidelines (ACM, IEEE, USENIX each have specific policies)
- Consult your institution's research ethics office BEFORE data collection, not after
- "No one will notice" is never a valid ethics argument
- Document your ethical reasoning even if the answer is "no concerns" — reviewers increasingly check

## Emitted Artifact

`Supplementary & Artifact Package` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Paper Draft + experiment artifacts` → scores `Supplementary & Artifact Package`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below.

- Does every appendix section have at least one reference from the main body?
- Can a stranger reproduce the key results by following only the README?
- Has the artifact been tested from scratch on a clean environment?
- Is the ethics checklist complete with no unchecked items (or documented justifications for N/A)?
- Have all co-authors reviewed at least 2 sections they did not write?
- Is the CRediT contribution table filled in and agreed upon by all authors?
