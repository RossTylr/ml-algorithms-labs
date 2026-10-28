# Skeptic Digest

Newest first. Every entry is a place a strong model got it subtly wrong. Read this as a syllabus of real pitfalls.

## 00.01.02

BLOCKED — REVISE in both skeptic rounds.

Round 2:
- F1 🔬 Called the near-zero direction (12) the "least determined" and said "only the top direction is stable". λ12 = 0.0036 sits 0.817 below λ11, the second-largest gap, so by Davis–Kahan it is well identified: bootstrap stability is 1.000 at n = 100, 300 and 1,400. Directions 2–11 (gaps 0.004–0.098) are the unsettled ones. The code also excludes component 12 from "the 11 separated ones", which swaps the groups.
- F2 🔬 Said the eigenvalues sum to 12.01, "the trace of the correlation matrix". A correlation matrix has trace exactly 12. S_tr is np.cov (ddof=1) of data standardised with .std(0) (ddof=0), so its trace is 12·1400/1399 = 12.0086.
- F3 🗣️ "|cos|" and "AUC" are used in Plain paragraphs and the Clinical Reading but never defined. A nurse cannot tell what 0.88 or 0.90 means.

Round 1:
- F1 GOAL On a `predict` notebook, it explained why direction 1 predicts ("the disease shifts bm_01 and bm_02 together"), and the explanation was wrong. About 95% of λ1 comes from the duplicated pair (2.114 vs 1 + corr(01,12) = 1.996). Direction 1 carries signal only because the copied test happens to be strong: if bm_12 copies noise test bm_10 instead, λ1 = 2.01 and held-out AUC = 0.53.
- F2 PREREG An unregistered supervised top-k experiment with a 500-resample bootstrap supplied the Clinical Reading's headline number (0.88, 0.84–0.92), and it was not marked (exploratory).
- F3 🔬 "Eigenvalues are properties of the cloud; eigenvectors are properties of the cloud and the units" is false. Eigenvalues depend on units too: rescaling one test took λ1 from 2.11 to 9.14. Rotation invariance is what separates them.
