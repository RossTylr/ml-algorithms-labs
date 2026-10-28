# Folding the paper library into ml-algorithms-labs — plan (no action taken)

**Inventory**: ~230 PDFs across 13 topic folders + MIT Press set + WiP textbooks + Google ML course decks + videos. Roughly: 60 seminal/method papers, 40 surveys, 35 textbooks, 25 health/clinical, 30 essays/futures/blog captures, 20 duplicates or junk (Medium paywall captures, `.DS_Store`, a Nature letter about fossil amino acids that is actually the page *before* Rumelhart–Hinton–Williams 1986).

## 1. The decision that shapes everything else

The library is **four different kinds of thing** and should be folded in four different ways. Treating it as one reading list would be the drift.

| Kind | Count | Fold-in mechanism | Touches the manifest? |
|---|---|---|---|
| **A. Seminal method papers** (Cortes–Vapnik, Breiman RF, XGBoost, ResNet, Dropout, LSTM, Attention, DQN, Kipf GCN, node2vec, PageRank, Score-SDE, Mamba…) | ~45 | `study:` field on the notebook that teaches that method. Builder must reproduce the paper's *central figure* on synthetic clinical data — "Figure 2 of Breiman 2001, on `admissions`" | Yes — 45 one-line edits |
| **B. Clinical/health papers** (CheXNet, Esteva dermatology, Rajkomar EHR, AlphaFold, Nori sequential diagnosis, Brodeur physician reasoning, Bayesian disease mapping, big-data-in-healthcare reviews) | ~15 | Become the **subject** of existing notebooks (replace a generic subject) or seed `study:` entries. Two warrant new notebooks (see §4) | Yes — subject rewrites + 2 additions |
| **C. Critique / epistemics** (ASA p-value statement, Amrhein "rise up", Breiman Two Cultures, Domingos "Few Useful Things", Box "Science and Statistics", Pitfalls of GNN Evaluation, GSM-Symbolic, Reasoning Models Don't Say What They Think, Why LMs Hallucinate, Lottery Ticket, "Are Transformers Effective for TS", Shalizi linear regression) | ~15 | Feed the **skeptic**, not the builder. Each becomes a named check in `.claude/agents/skeptic.md` — e.g. "Amrhein: does the Clinical Reading treat p<0.05 as a bright line?" | No manifest change; agent file only |
| **D. Textbooks, surveys, essays, course decks, videos** | ~150 | `References` cell only, via a `refs:` list in the manifest; plus a `library/INDEX.md` catalogue. Never read by the builder in full. | `refs:` field, auto-rendered |

**D-1** Kind C is the creative fold. The library's critique papers are a ready-made adversarial checklist. The skeptic is the only seat allowed to generate findings, so that's where critique belongs.
**D-2** Nothing in kind D gets a notebook. A "textbook chapter notebook" is a summary, not physics.

## 2. Kind A — the `study:` map (what the builder reproduces)

Each line: notebook id → paper → the figure/table/claim to reproduce on clinical data.

| NB | Paper | Reproduce |
|---|---|---|
| 00.01.03 SVD | Shannon 1948 (entropy section) / Eckart–Young | rank-k error curve |
| 00.05.01 Info theory | Shannon 1948 | entropy of a biomarker before/after a test |
| 02.02.01 Hypothesis testing | ASA 2016 + Amrhein 2019 | the six ASA principles as six experiments |
| 02.02.03 Non-parametric | Hypothesis Testing with E-values 2024 | e-value vs p-value under optional stopping |
| 02.09.01 Bayes vs freq | Box 1976 "Science and Statistics" | iteration loop figure |
| 03.02.01 Feature eng | Zheng & Casari; Guyon 2004 feature selection | Guyon's filter/wrapper/embedded taxonomy |
| 04.01.01 OLS | Shalizi "Truth about Linear Regression" | §2 "what OLS estimates when the model is wrong" |
| 04.04.02 Lasso | Hastie–Tibshirani–Tibshirani 2018 "Best Subset, Forward Stepwise, or Lasso" | their Fig. 1 relative-risk vs SNR, on `screening` |
| 05.05.01 SVM | Cortes & Vapnik 1995 | soft-margin figure |
| 05.04.01 Trees | Breiman 2001 "Two Cultures" (as framing) | Rashomon effect: 20 trees, same accuracy, different splits |
| 06.02.01 Random forest | Breiman 2001 RF | strength/correlation bound; OOB vs test |
| 06.06.01 XGBoost | Chen & Guestrin 2016 | sparsity-aware split; Table of split-finding cost |
| 07.04.01 GMM/EM | Dempster–Laird–Rubin (cited via Bishop) | likelihood monotonicity |
| 08.03.01 Manifold | Platonic Representation Hypothesis 2024 | cross-model embedding alignment, toy version |
| 08.05.01 Feature selection | Guyon & Elisseeff 2004 | Fig. on correlation ≠ relevance |
| 09.01.01 Apriori | Agrawal (cite) + FAERS framing | lift distribution |
| 13.01.01 PageRank | Page–Brin 1998 | damping sweep, Fig. 3 |
| 13.03.01 Embeddings | DeepWalk 2014, node2vec 2016, LINE 2015 | node2vec Fig. 3 p/q grid |
| 14.02.01 Label propagation | Zhu–Ghahramani–Lafferty 2003 harmonic functions | harmonic solution on two-moons |
| 14.03.02 Contrastive | "Statistical Theory of Contrastive Pre-training" 2025 | spectral view toy |
| 15.01.02 MLP | Rumelhart–Hinton–Williams 1986 | XOR + the symmetry-breaking argument |
| 15.02.01 Backprop | same + Schmidhuber 2014 overview | computational graph |
| 15.03.03 Regularisation | Srivastava 2014 Dropout; Gal & Ghahramani 2016 | dropout as Bayesian approx — MC-dropout uncertainty on `imaging` |
| 15.03.05 Loss | Lottery Ticket 2019 | prune-and-rewind on a small MLP |
| 16.02.02 ResNet | He et al. 2016 | degradation plot (Fig. 1) on `imaging` |
| 16.02.03 EfficientNet | Tan & Le 2020 | compound-scaling grid |
| 16.03.02 Detection | YOLOv3 2018; Segment Anything 2023 | grid-cell prediction |
| 17.01.02 LSTM | Hochreiter–Schmidhuber 1997; Olah "Understanding LSTMs" | gate diagram reproduced in matplotlib |
| 17.03.01 TCN | SCINet 2022; "Are Transformers Effective for TS" 2022 | **DLinear beats the transformer** on `vitals` — a failure-mode notebook by design |
| 18.01.01 Attention | Vaswani 2017 | Fig. 1 + scaled-dot-product |
| 18.02.02 BERT | Devlin 2019 | MLM on `notes` |
| 18.02.03 GPT | Radford 2018/2019; Brown 2020; Kaplan scaling laws 2020; Densing Law 2024 | scaling-law log-log on tiny models |
| 18.03.03 Efficiency | Lester 2021 prompt tuning; Informer 2021 | parameter-efficient vs full |
| 18.03.04 SSM | Gu S4 2022; Mamba 2024 | selective-scan toy |
| 19.03.03 Score-based | Song et al. 2021 Score-SDE | Fig. 1 forward/reverse SDE on 2D |
| 19.02.01 GAN | Goodfellow 2014 | Fig. 1 four-panel training dynamics |
| 20.01.01 GCN | Kipf & Welling 2017; Li 2018 "Deeper Insights" | **over-smoothing** curve |
| 20.01.03 GIN | Xu 2019 "How Powerful" | WL-test failure case |
| 20.01.02 GAT | Veličković 2018 | attention heatmap on `referrals` |
| 21.03.01 DQN | Mnih 2015 | Fig. 2 Q-value trace |
| 21.06.03 RLHF/DPO | DeepSeek-R1 2025; "Reasoning models don't say what they think" | CoT faithfulness probe |
| 22.04.01 Prophet | Taylor & Letham 2018 | changepoint prior sweep |
| 23.02.02 GP | Bishop 2006 ch. 6 | kernel composition |
| 26.03.01 NAS | AlphaEvolve 2025; "AlphaGo Moment for Architecture Discovery" | evolutionary search on tiny MLP |
| 27.02.02 Explainers | Explainable ML for Scientific Insights 2020; Transformer Circuits | attribution agreement matrix |
| 28.03.01 Recommenders | Manning IR (BM25 chapter); MTEB 2023 | BM25 vs embedding retrieval on `notes` |
| 28.04.02 RAG | Lewis 2021 RAG; GraphRAG 2025; Gupta RAG survey | local vs global retrieval |
| 29.06.01 Fairness | Barocas–Hardt–Narayanan; Obermeyer (already) | their Ch. 3 criteria table |

## 3. Kind C — the skeptic's reading list (becomes checks, not notebooks)

Add to `.claude/agents/skeptic.md` as named checks the skeptic cites when it fires:

- **ASA-1..6** (Wasserstein 2016): does the Clinical Reading treat p<0.05 as evidence of importance? Does it confuse "no significant difference" with "no difference"?
- **Amrhein**: any dichotomania ("significant / not significant") in Findings?
- **Box**: "all models are wrong" — does the notebook say *how* this one is wrong?
- **Breiman-2C**: does an interpretability claim rest on a single model when many fit equally well (Rashomon)?
- **Domingos**: which of the "12 useful things" does the notebook violate? (overfitting, curse of dimensionality, correlation ≠ causation, more data > cleverer algorithm)
- **Shalizi**: does an OLS notebook claim coefficients are "effects"?
- **Shchur GNN-pitfalls**: are GNN comparisons on a single split?
- **GSM-Symbolic / CoT-faithfulness / Hallucination**: for any LLM notebook, does the Clinical Reading overclaim reasoning?
- **Zeng DLinear**: does a deep time-series notebook beat a linear baseline?
- **Lottery Ticket**: is a "the architecture matters" claim actually an initialisation effect?

**D-3** These are checks the skeptic *may* cite, capped at three findings as before. The list widens what it can see; it does not widen what it can say.

## 4. Kind B — clinical papers → subjects and two new notebooks

Subject rewrites (sharper than the current generic ones):
- 05.01.01 Logistic → framed as the baseline that CheXNet/Esteva are measured against ("radiologist-level" means beating *this* at what AUC?)
- 16.01.02 First CNN → "CheXNet in miniature": 14-class → 2-class on `imaging`, with the **class-activation map** from the paper
- 16.02.01 LeNet…VGG → Esteva 2017 framing: transfer learning vs from-scratch at 100/1k/10k patches
- 17.01.02 LSTM → Rajkomar 2018: sequence of admissions → mortality, with their **FHIR-timeline figure** reproduced as a plot
- 18.02.02 BERT → Brodeur 2024 "superhuman physician reasoning": what the benchmark actually measured vs what was claimed (skeptic-flavoured)
- 23.03.02 Bayesian nonparametrics → **Bayesian disease mapping** (Spatial Statistics 2022): BYM model on a synthetic 50-area grid. This is the one place the library adds a *method* the manifest lacked.
- 28.04.02 RAG/agents → Nori 2025 Sequential Diagnosis: the MAI-DxO orchestrator pattern as a toy — cost-per-diagnosis vs accuracy frontier

Two notebooks to add to the manifest:
- **23.03.03 Bayesian Disease Mapping (BYM / CAR)** — P1, dataset `cohort` + a new `areas` adjacency. Justified: it's a core health-DS method, absent from the manifest, and the paper is in hand.
- **28.02.03 Spatial Accessibility to Care (2SFCA)** — P4, from the Chicago GIS paper + Geocomputation primer. Justified: P4 is thin on geospatial; Role 2 placement is a P5 use.

**D-4** Only two additions. AlphaFold, AlphaEvolve, Gemini, Segment Anything are *references*, not notebooks — nothing in them is reproducible at this scale.

## 5. Kind D — the catalogue

`library/INDEX.md`, generated from a `library/library.yaml` (title, authors, year, kind A/B/C/D, folder, which notebooks cite it). The manifest gains an optional `refs: [key, key]` per notebook; `scaffold.py` renders them into the References cell. Builder is told: *cite from `refs:`; do not read the PDF unless `study:` names it*.

Duplicates to flag (not delete): Attention ×2, Amodei ×2, Books&Arts ×2, Schmidhuber ×2, Géron ×2, "Reasoning models" ×2, ResNet ×2, Mohri full + chapters, Murphy ×2 editions; five Medium paywall captures with no recoverable content; the 1986 Nature file is the wrong page.

## 6. Learning-loop hook

Each `study:` paper gets a sixth quiz question: *"What did the paper claim that the synthetic reproduction could not test?"* That's the question that keeps HC-7 honest and is the single highest-value thing a reader learns from a reproduction.

## 7. Execution order (when you say go)

1. `library/library.yaml` + `INDEX.md` generator — 1 slice, no manifest change.
2. Skeptic checks (§3) — 1 slice, agent file only.
3. Manifest `study:` + `refs:` edits (§2) and the seven subject rewrites (§4) — 1 slice, then `scaffold.py` regenerates READMEs. Existing stubs untouched because scaffold never overwrites.
4. Two new notebooks (§4) — manifest + `datasets.load_areas()` — 1 slice.
5. Re-run the T0 loop on one `study:` notebook (suggest 04.04.02 Lasso vs best-subset) to see whether "reproduce Fig. 1" is a prompt the builder can satisfy.

Nothing above runs until you say so.
