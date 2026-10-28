# The Little Book of Clinical ML

*One idea and one figure per page. Generated from 1 built notebooks; regenerated on every build.*

## 00 — Mathematical Foundations

### Vectors, Matrices & Operations

Write a patient's twelve test results down in a fixed order and you have a **vector**: an ordered list of numbers, one per test, always in the same order. Stack the lists for 2,000 patients, one patient per line, and you have a **matrix**: a table with patients as rows and tests as columns, the same shape as a results spreadsheet. Now picture each patient as an arrow. It starts at the *average* patient and points towards that person's own pattern of results: long if the results are far from average, short if they are close. To compare two patients, line their results up test by test, multiply each matching pair and add the answers. That total is the **dot product**. It is large when both patients are high (or both low) on the same tests, near zero when their results have nothing in common, and negative when one is high where the other is low. **Cosine similarity** is the dot product with the arrows' lengths divided out. It asks only "do these two arrows point the same way?", so the same pattern counts as a match whether it is mild or severe. **Distance** asks how far apart the two arrow tips are. A new patient whose arrow points the way the diseased patients' arrows point is probably diseased. The catch: the arrows depend on the units each test is written in, so the units quietly decide who counts as similar.

> 📈 *New patients who point the same way as the typical diseased patient are usually diseased*

<sub>P1 · predict · `00_mathematical_foundations/01_linear_algebra/01_vectors_matrices_operations.ipynb`</sub>
