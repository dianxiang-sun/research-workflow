# Gate Check-Dimension Matrix

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

Legend: `★` = deep check · `○` = light scan. `/research gate` step 2 selects this phase's columns from the matrix.

> Row-code namespace: most matrix subitems use category letter + number (`A*`, `B*`, `C*`, `E*`, `F*`, `H*`). Dataset Validity uses `DV*` and Resource Planning uses `RP*` because the D-family row codes are reserved for the review rubric and the G-family row codes are reserved for Global Rules in their own files.

```
                                    Ph0  Ph1  Ph2  Ph3  Ph4  Ph5  Ph6  Ph7
A. Novelty & Positioning
   A1 One-sentence differentiation   ★         ★    ○              ★    ★
   A2 "Just engineering" defense                ★                       ★
   A3 Literature freshness           ★    ○         ○              ★    ★
B. Evaluation Validity
   B1 Causal chain RQ→metric→oracle       ○    ★    ★         ★    ★    ★
   B2 Oracle reliability                             ★         ★    ★    ★
   B3 Tool meta-validity                             ★         ★         ★
   B4 LLM-evaluates-LLM circularity                 ★         ★         ★
   B5 Claim scope ≤ evidence scope                             ★    ★    ★
C. Experimental Fairness
   C1 Cost-equivalent comparison                     ★         ★         ★
   C2 Information/resource parity                    ★         ★         ★
   C3 Ablation causal isolation                      ★         ★         ★
   C4 Code freeze integrity                     ○    ○    ★    ★
D. Dataset Validity
   DV1 Task-format alignment         ○              ★                   ★
   DV2 Ground truth / oracle gap                     ★         ★         ★
   DV3 Representativeness                            ★         ○         ★
   DV4 Statistical power                             ★         ★
E. Reproducibility
   E1 Non-determinism handling                            ○    ★         ★
   E2 Environment lockdown                                ★    ★
   E3 Reproduction cost                                   ○    ★    ○    ★
F. Practical Significance
   F1 Cost-effectiveness trade-off                              ★    ★    ★
   F2 Deployment feasibility                                    ○    ★    ★
   F3 Generalization boundaries                                 ○    ★    ★
G. Resource Planning
   RP1 Cost with retry multiplier    ○              ★    ○    ★
   RP2 Timeline with Hofstadter     ○              ★         ★
   RP3 Kill conditions / stop-loss   ○              ★         ★
H. Writing & Presentation
   H1 Narrative arc coherence                                        ★    ★
   H2 Related work completeness                                      ★    ★
   H3 Threats to validity coverage                                   ★    ★
   H4 Page budget compliance                                         ★    ★
```
