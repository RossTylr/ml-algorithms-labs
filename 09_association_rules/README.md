# Module 09 — Association Rules

**Tier** 2 · **Notebooks** 5 · **Prerequisites** 02

> Which drugs are co-prescribed, which comorbidities cluster, which combinations flag adverse events.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Support, Confidence & Lift](01_apriori/01_support_confidence_lift.ipynb) | P2 | explain | `prescribing` | `FAERS-style pharmacovigilance signals` | Co-prescription patterns across 10k patients |
| 01.02 | [Frequent Itemset Generation](01_apriori/02_frequent_itemset_generation.ipynb) | P2 | explain | `prescribing` |  | The lattice |
| 02.01 | [FP-Tree & Vertical Formats](02_fp_eclat/01_fp_tree_vertical_formats.ipynb) | P2 | decide | `prescribing` |  | Same, no candidate generation |
| 03.01 | [Conviction, Leverage & Zhang](03_metrics_sequential/01_conviction_leverage_zhang.ipynb) | P2 | decide | `prescribing` |  | Ranking adverse-event rules |
| 03.02 | [GSP & PrefixSpan](03_metrics_sequential/02_gsp_prefixspan.ipynb) | P2 | decide | `prescribing` |  | Prescription sequences over time — escalation patterns |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 09_association_rules` checks all of it.
