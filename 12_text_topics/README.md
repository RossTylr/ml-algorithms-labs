# Module 12 — Topic Modelling & Text

**Tier** 3 · **Notebooks** 5 · **Prerequisites** 08

> Structure in clinical free text.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [LSA](01_topic_models/01_lsa.ipynb) | P1 | `notes` | Triage notes — TF-IDF + SVD |
| 01.02 | [LDA](01_topic_models/02_lda.ipynb) | P1 | `notes` | Discharge summaries — Dirichlet priors |
| 01.03 | [NMF, CTM & BERTopic](01_topic_models/03_nmf_ctm_bertopic.ipynb) | P1 | `notes` | Parts-based; correlated complaint topics; transformer-based |
| 02.01 | [Word2Vec](02_embeddings/01_word2vec.ipynb) | P1 | `notes` | Clinical vocabulary geometry |
| 02.02 | [GloVe & FastText](02_embeddings/02_glove_fasttext.ipynb) | P1 | `notes` | Co-occurrence; subwords for misspelt drug names |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 12_text_topics` checks all of it.
