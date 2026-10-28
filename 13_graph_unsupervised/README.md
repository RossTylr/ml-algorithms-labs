# Module 13 — Graph & Network (Unsupervised)

**Tier** 3 · **Notebooks** 3 · **Prerequisites** 00, 07

> Care pathways and referral networks as graphs.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [PageRank & HITS](01_ranking/01_pagerank_hits.ipynb) | P4 | explain | `referrals` | `page1998` | Which clinicians and units are the hubs of a referral network |
| 02.01 | [Louvain, Label Propagation & Girvan–Newman](02_communities/01_louvain_label_propagation_girvannewman.ipynb) | P4 | explain | `referrals` |  | Finding care communities |
| 03.01 | [DeepWalk, Node2Vec & Graph Autoencoders](03_embeddings/01_deepwalk_node2vec_graph_autoencoders.ipynb) | P4 | predict | `referrals` | `grover2016` | Units as vectors |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 13_graph_unsupervised` gates the module.
