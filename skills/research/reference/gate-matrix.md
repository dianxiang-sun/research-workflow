# Gate Check-Dimension Matrix

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

Legend: `★` = deep check · `○` = light scan. `/research gate` step 2 selects this phase's columns from the matrix.

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
   D1 Task-format alignment          ○              ★                   ★
   D2 Ground truth / oracle gap                      ★         ★         ★
   D3 Representativeness                             ★         ○         ★
   D4 Statistical power                              ★         ★
E. Reproducibility
   E1 Non-determinism handling                            ○    ★         ★
   E2 Environment lockdown                                ★    ★
   E3 Reproduction cost                                   ○    ★    ○    ★
F. Practical Significance
   F1 Cost-effectiveness trade-off                              ★    ★    ★
   F2 Deployment feasibility                                    ○    ★    ★
   F3 Generalization boundaries                                 ○    ★    ★
G. Resource Planning
   G1 Cost with retry multiplier     ○              ★    ○    ★
   G2 Timeline with Hofstadter      ○              ★         ★
   G3 Kill conditions / stop-loss    ○              ★         ★
H. Writing & Presentation
   H1 Narrative arc coherence                                        ★    ★
   H2 Related work completeness                                      ★    ★
   H3 Threats to validity coverage                                   ★    ★
   H4 Page budget compliance                                         ★    ★
```
