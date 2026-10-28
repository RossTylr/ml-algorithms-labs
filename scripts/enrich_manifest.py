#!/usr/bin/env python3
"""enrich_manifest.py — one-off, idempotent enrichment of curriculum.yaml from the paper-fold plan.

Adds, by targeted text edit (so the manifest keeps its hand-written flow style):
  goal:   predict | explain | decide      (rule by band, with overrides)
  gds:    1–6 Donoho division            (rule by module, with overrides)
  study:  <curated key>                  (explicit map)
  refs:   [<curated keys>]               (explicit map)
  subject rewrites                       (explicit map)
  error-analysis experiment              (P1/P2 classification notebooks in modules 05, 06, 15, 16)

Keys are "NN.topic_slug.n". Re-running changes nothing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "curriculum" / "curriculum.yaml"

GOAL_BY_BAND = {"P1": "predict", "P2": "decide", "P3": "explain", "P4": "predict", "P5": "decide"}
GOAL_OVERRIDE = {
    "00.probability.1": "explain", "00.information_theory.1": "explain", "02.correlation.1": "explain",
    "02.bayes_vs_freq.1": "explain", "04.multiple_linear.1": "explain", "04.multiple_linear.2": "explain",
    "04.bayesian_linear.1": "explain", "07.kmeans.1": "explain", "07.kmeans.2": "explain", "08.pca.1": "explain",
    "09.apriori.1": "explain", "09.apriori.2": "explain", "13.ranking.1": "explain", "13.communities.1": "explain",
    "27.global.1": "explain", "27.global.2": "explain", "27.local.1": "explain", "27.local.2": "explain", "27.deep.1": "explain", "27.deep.2": "explain",
    "28.causal.1": "explain", "28.causal.2": "explain", "29.fairness.1": "explain", "29.calibration_bias.1": "predict",
    "21.bandits.1": "decide", "05.online.2": "predict", "10.learned.2": "predict",
}
GDS_BY_MODULE = {"00": 3, "01": 3, "02": 4, "03": 1, "04": 4, "05": 4, "06": 4, "07": 4, "08": 2, "09": 4, "10": 4, "11": 4, "12": 2,
                 "13": 4, "14": 4, "15": 4, "16": 4, "17": 4, "18": 4, "19": 4, "20": 4, "21": 4, "22": 4, "23": 4, "24": 4, "25": 4,
                 "26": 3, "27": 6, "28": 4, "29": 6}
GDS_OVERRIDE = {"01.visualisation.1": 5, "01.pandas.1": 1, "01.pandas.2": 1, "01.data_wrangling.1": 1, "01.sql.1": 1,
                "01.reproducibility.1": 6, "03.feature_engineering.1": 2, "03.feature_engineering.2": 2, "03.scaling.1": 2,
                "03.encoding.1": 2, "03.eda.1": 1, "02.effect_sizes.1": 6, "02.ab_testing.1": 6, "08.feature_selection.1": 2,
                "08.feature_selection.2": 2, "12.embeddings.1": 2, "12.embeddings.2": 2}

STUDY = {
    "00.linear_algebra.3": "shannon1948", "00.information_theory.1": "shannon1948",
    "02.inferential.1": "wasserstein2016", "02.inferential.3": "ramdas2024", "02.bayes_vs_freq.1": "box1976",
    "03.feature_engineering.1": "guyon2004",
    "04.simple_linear.1": "shalizi2024", "04.regularised.2": "hastie2018",
    "05.logistic.1": "sideygibbons2019", "05.decision_trees.1": "breiman2001b", "05.svm.1": "cortes1995",
    "06.random_forest.1": "breiman2001", "06.xgboost.1": "chen2016",
    "08.manifold.3": "huh2024", "08.feature_selection.1": "guyon2004",
    "13.ranking.1": "page1998", "13.embeddings.1": "grover2016",
    "14.graph_based.1": "zhu2003", "14.deep.2": "contrastive2025",
    "15.neurons.2": "rumelhart1986", "15.backprop.1": "rumelhart1986", "15.training.3": "gal2016", "15.training.5": "frankle2019",
    "16.fundamentals.2": "rajpurkar2017", "16.classic.1": "esteva2017", "16.classic.2": "he2016", "16.classic.3": "tan2020", "16.tasks.2": "redmon2018",
    "17.rnn.2": "rajkomar2018", "17.convolutional_sequences.1": "zeng2022",
    "18.attention.1": "vaswani2017", "18.architectures.2": "devlin2019", "18.architectures.3": "kaplan2020", "18.variants.3": "lester2021", "18.variants.4": "gu2024",
    "19.gans.1": "goodfellow2014", "19.diffusion.3": "song2021",
    "20.message_passing.1": "kipf2017", "20.message_passing.2": "velickovic2018", "20.message_passing.3": "xu2019",
    "21.value_based.1": "mnih2015", "21.advanced_rl.3": "chen2025",
    "22.decomposition.1": "taylor2018",
    "26.nas.1": "novikov2025", "27.deep.1": "roscher2020",
    "28.recommenders.2": "manning2009", "28.llm.2": "lewis2021", "28.survival.1": "sideygibbons2019",
    "29.fairness.1": "barocas2023", "29.calibration_bias.1": "rajpurkar2022",
}
REFS = {
    "00.linear_algebra.1": ["deisenroth2020"], "00.linear_algebra.2": ["deisenroth2020"], "00.calculus.1": ["deisenroth2020"],
    "00.probability.2": ["dekking2005", "downey2024"], "00.probability.3": ["murphy2022"], "00.optimisation.1": ["kochenderfer2019"],
    "01.numpy.1": ["harris2020"], "01.visualisation.1": ["knaflic2015"], "01.reproducibility.1": ["chen2022"], "01.software_engineering.1": ["huyen2022"],
    "02.descriptive.1": ["downey2024"], "02.inferential.1": ["amrhein2019"], "02.inferential.2": ["dekking2005"], "02.effect_sizes.1": ["amrhein2019", "ng2022"],
    "03.pipelines.1": ["chen2022", "reddi2025"], "03.feature_engineering.1": ["zheng2018"], "03.feature_engineering.2": ["zheng2018"],
    "03.splitting.1": ["ng2022", "huyen2022"], "03.imbalance.1": ["lakshmanan2021"], "03.eda.1": ["donoho2017"],
    "04.simple_linear.1": ["esl2009"], "04.simple_linear.2": ["shalizi2024", "esl2009"], "04.polynomial.1": ["esl2009", "mehta2019"],
    "04.regularised.1": ["esl2009"], "04.regularised.3": ["esl2009"], "04.gaussian_process.1": ["murphy2023"],
    "05.logistic.1": ["hardt2021"], "05.knn.1": ["domingos2012"], "05.naive_bayes.1": ["manning2009"], "05.decision_trees.2": ["esl2009"],
    "05.svm.3": ["mohri2018"], "05.online.1": ["hardt2021"],
    "06.bagging.1": ["esl2009"], "06.random_forest.2": ["esl2009"], "06.adaboost.1": ["mohri2018"], "06.gradient_boosting.1": ["esl2009"],
    "07.gmm.1": ["bishop2006"], "07.graph_based.1": ["bronstein2021"],
    "08.pca.1": ["murphy2022"], "08.manifold.1": ["mehta2019"], "08.neural.1": ["prince2023"],
    "09.apriori.1": ["needham2020"],
    "10.learned.1": ["mehta2019"],
    "12.topic_models.1": ["manning2009"], "12.embeddings.1": ["jurafsky2018", "kozlowski2025"],
    "13.ranking.1": ["needham2020"], "13.embeddings.1": ["perozzi2014", "tang2015", "hamilton2018"],
    "15.neurons.1": ["hardt2021"], "15.neurons.2": ["prince2023", "fleuret2024"], "15.training.1": ["kochenderfer2019"], "15.training.3": ["srivastava2014"],
    "16.fundamentals.1": ["prince2023", "fleuret2024"], "16.classic.2": ["bronstein2021"], "16.tasks.2": ["kirillov2023"],
    "17.rnn.1": ["hochreiter1997", "jurafsky2018"], "17.rnn.2": ["hochreiter1997"], "17.convolutional_sequences.1": ["liu2022"],
    "18.attention.1": ["tunstall2022"], "18.architectures.3": ["radford2018", "radford2019", "brown2020"], "18.architectures.4": ["raffel2020"],
    "18.variants.1": ["kirillov2023"], "18.variants.3": ["zhou2021"], "18.variants.4": ["gu2022"],
    "19.autoencoders.2": ["prince2023"], "19.diffusion.1": ["song2021"],
    "20.message_passing.1": ["li2018", "shchur2019", "zhou2020"], "20.message_passing.2": ["bruna2014", "gilmer2017"], "20.message_passing.3": ["bronstein2021"], "20.advanced.1": ["schlichtkrull2018"],
    "21.bandits.1": ["sutton2018", "kochenderfer2022"], "21.tabular.1": ["sutton2018", "kochenderfer2022"], "21.tabular.3": ["sutton2018"],
    "21.value_based.2": ["bellemare2023"], "21.advanced_rl.1": ["albrecht2024"], "21.advanced_rl.3": ["deepseek2025", "mirzadeh2024"],
    "22.arima.1": ["hyndman2021"], "22.deep.2": ["zhou2021"],
    "23.inference.1": ["murphy2022", "barber2015"], "23.inference.3": ["murphy2023"], "23.models.1": ["gal2016"], "23.models.3": ["kochenderfer2019"],
    "24.networks.1": ["kochenderfer2022", "barber2015"], "24.sequential.1": ["bishop2006"], "24.filtering.1": ["kochenderfer2022"],
    "26.hpo.1": ["kochenderfer2019"], "26.nas.1": ["liu2025"],
    "27.global.1": ["munn2022", "breiman2001b"], "27.local.1": ["munn2022"], "27.deep.2": ["roscher2020"],
    "28.causal.1": ["hardt2021"], "28.llm.1": ["lester2021"], "28.llm.2": ["edge2025", "gupta2025", "nori2025"], "28.recommenders.2": ["muennighoff2023"],
    "29.classification_metrics.1": ["ng2022"], "29.validation.1": ["ng2022", "shchur2019"], "29.fairness.1": ["rajpurkar2022"],
}
SUBJECT = {
    "05.logistic.1": "Disease present/absent from two biomarkers — the baseline that every 'radiologist-level' claim is measured against",
    "16.fundamentals.2": "CheXNet in miniature — lesion present/absent end to end, with the class-activation map the paper is known for",
    "16.classic.1": "Esteva-style: transfer learning vs from-scratch at 100 / 1k / 10k patches",
    "17.rnn.2": "Rajkomar-style: a patient's admission timeline as a sequence → mortality; long-range deterioration on vitals",
    "18.architectures.2": "Masked LM on triage notes; fine-tune for urgency — and what a 'physician-level' benchmark actually measured",
    "28.llm.2": "Guideline-grounded answers; a Sequential-Diagnosis-style gatekeeper loop scored on accuracy AND information cost",
}
ERROR_ANALYSIS = "error analysis: 20 worst cases, categorised, vs clinician baseline"
EA_MODULES = {"05", "06", "15", "16"}


def main() -> int:
    text = MAN.read_text()
    lines = text.splitlines(keepends=True)
    mod = topic = None
    n_goal = n_gds = n_study = n_refs = n_subj = n_ea = 0
    for i, ln in enumerate(lines):
        m = re.match(r'  - id: "(\d\d)"', ln)
        if m:
            mod = m.group(1); continue
        m = re.match(r"      - slug: (\w+)", ln)
        if m:
            topic = m.group(1); continue
        m = re.match(r"          - \{n: (\d+), title:", ln)
        if not m:
            continue
        key = f"{mod}.{topic}.{m.group(1)}"
        band = re.search(r"band: (P\d)", ln)
        band = band.group(1) if band else "P1"
        new = ln
        if "goal:" not in new:
            goal = GOAL_OVERRIDE.get(key, GOAL_BY_BAND[band])
            gds = GDS_OVERRIDE.get(key, GDS_BY_MODULE[mod])
            new = re.sub(r"(band: P\d)", rf"\1, goal: {goal}, gds: {gds}", new, count=1); n_goal += 1; n_gds += 1
        if key in SUBJECT:
            new = re.sub(r'subject: "[^"]*"', f'subject: "{SUBJECT[key]}"', new, count=1); n_subj += 1
        if key in STUDY and "study:" not in new:
            new = re.sub(r"(dataset: \w+)", rf'\1, study: "{STUDY[key]}"', new, count=1); n_study += 1
        if key in REFS and "refs:" not in new:
            refs = ", ".join(REFS[key])
            new = re.sub(r"(visuals: \d+)", rf"refs: [{refs}], \1", new, count=1); n_refs += 1
        if mod in EA_MODULES and band in {"P1", "P2"} and ERROR_ANALYSIS not in new and "experiments: [" in new:
            new = new.replace("]}", f', "{ERROR_ANALYSIS}"]}}', 1) if new.rstrip().endswith("]}") else new
            n_ea += 1
        lines[i] = new
    MAN.write_text("".join(lines))
    print(f"enrich: goal {n_goal} · gds {n_gds} · study {n_study} · refs {n_refs} · subject {n_subj} · error-analysis {n_ea}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
