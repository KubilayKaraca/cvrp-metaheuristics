# AI-Tool Usage Log (basis for Appendix B)

This file is the basis for **Appendix B – AI-tool usage statement** of the final report.
Section 7 of the project description requires Appendix B to state **which tools** were used,
**for which parts**, and to give **2–3 example prompts**. It also requires that we cite all
external sources and clearly mark which parts of the code are our own and which are adapted.
Add a row to the detailed log (Section 6) every time an AI tool is used.

## 1. Tools used

| Tool | Provider |
|---|---|
| Claude | Anthropic |

No other AI tools (e.g. ChatGPT, Copilot) have been used so far.

## 2. Parts of the project and how AI was used

| Part of the project | Tool | How the AI tool was used | Done by the team |
|---|---|---|---|
| Understanding the project description | Claude | Explanation of the tasks, requirements and concepts; work plan | — |
| Project organisation | Claude | Guidance on repository setup and division of work | Repository set up by the team |
| Milestone 1 – instance generator, map, build scripts | Claude | Code written by Claude (see Section 5) | Output checked by the team (total demand, K) |
| Milestone 1 – report | Claude | First draft written by Claude; writing plan, suggested sources and prompts; concept explanations; feedback on our text; grammar correction | Report rewritten by the team, each member writing one section (see Section 6) |

## 3. Example prompts

1. "Explain this project description to me completely." (original in Turkish)
2. "In the TSP → CVRP reduction, why do we choose K = 1, and why is choosing a large Q not enough on its own? Explain briefly, do not write text." (original in Turkish)
3. "This is the section we wrote. Do not rewrite it; only list the logical errors, missing steps and missed edge cases." (original in Turkish)

## 4. Responsibility

As required by Section 7, the team is fully responsible for the correctness of everything
submitted, including any AI-assisted text, proofs and code, and every member must be able
to explain every part of the report and code during the oral defense.

## 5. Code origin

| File | Origin |
|---|---|
| `src/team_seed.py` | Written by Claude (AI) |
| `src/distances.py` | Written by Claude (AI) |
| `src/generate_medidrone.py` | Written by Claude (AI) |
| `src/check_metric.py` | Written by Claude (AI) |
| `src/plot_instance.py` | Written by Claude (AI) |
| `src/m1_values.py` | Written by Claude (AI) |
| `scripts/build_m1.sh` | Written by Claude (AI) |
| `report/m1/m1.tex` | Written by Claude (AI) – first draft of the Milestone 1 report |

Each of these files also carries an origin note in its header. Code that we write ourselves
or adapt from published pseudocode will be marked the same way (own / adapted from …).

## 6. Detailed log

| Date | Member | Tool | Part of the project | Type of use |
|---|---|---|---|---|
| 2026-11-16 | Kubilay Karaca | Claude | Project description | Explanation of the tasks and requirements; work plan |
| 2026-11-16 | Kubilay Karaca | Claude | Project organisation | Guidance on repository setup and division of work |
| 2026-11-16 | Kubilay Karaca | Claude | Milestone 1 | Drafting of the instance generator, plotting and build scripts, the reduction sketches and the LaTeX report |
| 2026-11-16 | Kubilay Karaca | Claude | Milestone 1 | Revision of the draft to the scope required by the guideline |
| 2026-11-17 | Kubilay Karaca | Claude | Milestone 1 | Update of the team table, seed and instance after a fourth member joined |
| 2026-11-17 | Kubilay Karaca | Claude | Milestone 1 | Writing plan for the team: outline and division of the report, suggested sources and prompts for each section; explanation of the definitions of Hamiltonian Cycle, TSP (decision) and Bin Packing |
| 2026-11-17 | Tuana Pektaş | Claude | M1 – Section 1 (problem definitions, references) | Section written by the member using the AI-generated draft as a starting point and the AI-suggested sources; concept explanations, feedback and grammar correction with the prompts in Section 3 |
| 2026-11-18 | Zehra Gebeş | Claude | M1 – Section 2.1 Step A and 2.3 Composition | Section written by the member using the AI-generated draft as a starting point and the AI-suggested sources; concept explanations, feedback and grammar correction with the prompts in Section 3 |
| 2026-11-18 | Kubilay Karaca | Claude | M1 – Section 2.2 Step B and 2.4 Bin Packing | Section written by the member using the AI-generated draft as a starting point and the AI-suggested sources; concept explanations, feedback and grammar correction with the prompts in Section 3 |
| 2026-11-18 | Elif Ozan | Claude | M1 – Section 3 Seed, Section 4 Instance, merging | Section written by the member using the AI-generated draft as a starting point; instance and map produced with the AI-written generator; figures checked by the member (total demand, K); feedback on the merged report and grammar correction with the prompts in Section 3 |
| 2026-11-19 | Team | — | Milestone 1 | Report rewritten by the team based on the AI-assisted draft |

## 7. External sources suggested by the AI tool

All of these must also appear in the reference list of the report if they were used.

| Source | Used for |
|---|---|
| CMP3005 project description (Sections 2, 4 and 7) | Problem definition, task requirements, instance rules |
| R. M. Karp, "Reducibility among combinatorial problems", 1972 | NP-completeness of Hamiltonian Cycle and TSP |
| M. R. Garey, D. S. Johnson, *Computers and Intractability*, 1979 | NP-completeness of Bin Packing |
| OpenDSA (Virginia Tech), "Reduction of Hamiltonian Cycle to Traveling Salesman" | Step A |
| UNH lecture note, "NP-completeness proof by reduction" (adapted from CLRS §34.5.4) | Step A |
| J. Erickson, *Algorithms*, chapter on NP-hardness | Composition of reductions |
| "Approximation Algorithms for Capacitated Vehicle Routing Problems: A Comprehensive Survey", arXiv:2306.01826 | Step B, Bin Packing connection |
| M. Chiarandini, vehicle routing lecture slides (DM204, University of Southern Denmark) | Bin Packing connection |
