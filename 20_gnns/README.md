# Module 20 — Graph Neural Networks

**Tier** 3 · **Notebooks** 4 · **Prerequisites** 13, 15

> Learning on referral and comorbidity graphs.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [GCN & MPNN](01_message_passing/01_gcn_mpnn.ipynb) | P4 | predict | `referrals` | `kipf2017` | Node classification on the referral network |
| 01.02 | [GraphSAGE & GAT](01_message_passing/02_graphsage_gat.ipynb) | P4 | predict | `referrals` | `velickovic2018` | Inductive; attention on neighbours |
| 01.03 | [GIN & Graph Transformers](01_message_passing/03_gin_graph_transformers.ipynb) | P2 | decide | `synthetic` | `xu2019` | Molecule-style graph-level tasks |
| 02.01 | [TGN & Heterogeneous GNNs](02_advanced/01_tgn_heterogeneous_gnns.ipynb) | P4 | predict | `referrals` |  | Evolving multi-type care networks |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 20_gnns` checks all of it.
