# Assumptions register — the synthetic generators

**None of these values is doctrine or measured.** Every number below was chosen so that a mechanism is learnable on
synthetic data; a notebook that quotes one is quoting an assumption, not a clinical fact (AGENTS.md, HC-7).

One row per numeric parameter, transcribed from the generator code: `datasets/__init__.py` (`load_screening`,
`load_admissions`, `load_trial`, `load_vitals`, `load_prescribing`, `load_cohort`, `load_notes`, `load_referrals`,
`load_imaging`, `load_evac`, `load_areas`) and `datasets/synthetic/__init__.py` (`dose_response`, `regression_variants`,
`classification_variants`, `clustering_variants`, `time_series_variants`, `manifold_variants`, `bandit_arms`).
Values are the defaults; a notebook may override the keyword arguments. Not listed, because they are not generators:
`datasets/baselines.py` (rule-based clinician proxies) and `load_ledger` (this repo's own build record).

**Used in** — modules with at least one notebook whose manifest `dataset:` is this generator, at the time of writing;
`curriculum/curriculum.yaml` is the authority. When a generator's code changes, change its rows here in the same commit.

| Dataset | Parameter | Value | Unit | Source | Assumed | Used in |
|---|---|---|---|---|---|---|
| screening | `load_screening` n — patients | 2000 | count | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | n_biomarkers — panel width | 12 | count | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | prevalence of disease | 0.15 | probability | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | age — mean | 55 | years | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | age — SD | 14 | years | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | age — clip range | 18–95 | years | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | sex — P(F) | 0.5 | probability | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | biomarker noise — SD of every bm_ before any shift | 1 | z units | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_01 shift when diseased (strong) | +1.6 | SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_02 shift when diseased (strong) | +1.2 | SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_02 age slope — per (age − 55)/14 | +0.3 | SD per age-SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_03 shift when diseased (weak) | +0.5 | SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_04 shift when diseased (weak) | +0.4 | SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_05 shift when diseased (weak) | +0.3 | SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| screening | bm_12 = bm_01 + noise — collinear-pair noise SD | 0.1 | SD | synthetic | true | 00 02 03 04 05 06 08 11 14 23 24 29 |
| admissions | `load_admissions` n — admissions | 5000 | count | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | calendar span — admit days drawn from a daily rate over | 1095 | days | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | weekday arrival uplift — rate × (1 + a) Mon–Fri | 0.25 | × weekend rate | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | winter surge amplitude — rate × (1 + b·max(0, cos(2π(day − peak)/365))) | 0.4 | × base rate | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | winter surge peak | 15 (mid-January) | day of year | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | start date | 2022-01-01 | date | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | patient_id pool — n // 2 ids drawn with replacement (repeat patients) | 2500 | count | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | age — mean | 62 | years | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | age — SD | 18 | years | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | age — clip range | 18–98 | years | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | department mix — cardiology / respiratory / general_medicine / orthopaedics / surgery | 0.20 / 0.20 / 0.30 / 0.15 / 0.15 | probability | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | admission_type mix — emergency / elective / urgent | 0.55 / 0.30 / 0.15 | probability | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | severity — uniform range | 1–10 | score | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | comorbidity_count — Poisson mean (clip 0–9) | 1.8 | conditions | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | prior_admissions — Poisson mean (clip 0–12) | 0.7 | admissions | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | deprivation_quintile — uniform over | 1–5 | quintile | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | gp_practice — number of practices | 400 | count | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS intercept | 0.2 | log days | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS age coefficient | 0.012 | log days per year | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS severity coefficient | 0.11 | log days per point | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS comorbidity coefficient | 0.09 | log days per condition | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS emergency admission | +0.25 | log days | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS orthopaedics | +0.15 | log days | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | log-LOS noise SD | 0.45 | log days | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | LOS clip range | 0.5–90 | days | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | readmit_30d log-odds intercept | −3.6 | log-odds | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | readmit_30d age coefficient (age − 62) | 0.02 | log-odds per year | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | readmit_30d severity coefficient | 0.22 | log-odds per point | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | readmit_30d comorbidity coefficient | 0.35 | log-odds per condition | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | readmit_30d prior-admissions coefficient | 0.30 | log-odds per admission | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | readmit_30d deprivation coefficient (quintile − 3) | 0.10 | log-odds per quintile | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | died log-odds intercept | −6.0 | log-odds | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | died age coefficient (age − 62) | 0.04 | log-odds per year | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | died severity coefficient | 0.35 | log-odds per point | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | died comorbidity coefficient | 0.2 | log-odds per condition | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| admissions | discharge_destination if alive — home / care_home / rehab (mortuary if died: the designed leak) | 0.75 / 0.15 / 0.10 | probability | synthetic | true | 00 01 02 03 04 06 19 21 22 23 26 27 28 29 |
| trial | `load_trial` n — participants | 800 | count | synthetic | true | 01 02 04 23 28 |
| trial | allocation — P(treatment) | 0.5 | probability | synthetic | true | 01 02 04 23 28 |
| trial | true_effect — mean treatment effect on outcome_12w | −0.35 | SD of outcome | synthetic | true | 01 02 04 23 28 |
| trial | heterogeneity slope — effect × (1 + slope × baseline) | 0.4 | per baseline SD | synthetic | true | 01 02 04 23 28 |
| trial | age — mean | 58 | years | synthetic | true | 01 02 04 23 28 |
| trial | age — SD | 12 | years | synthetic | true | 01 02 04 23 28 |
| trial | age — clip range | 18–90 | years | synthetic | true | 01 02 04 23 28 |
| trial | sites | 5 | count | synthetic | true | 01 02 04 23 28 |
| trial | site effect SD | 0.15 | SD of outcome | synthetic | true | 01 02 04 23 28 |
| trial | baseline_score — distribution | N(0, 1) | SD | synthetic | true | 01 02 04 23 28 |
| trial | adherence in treatment arm — Beta(a, b) | Beta(5, 1.5) | fraction | synthetic | true | 01 02 04 23 28 |
| trial | adherence in control arm | 1.0 | fraction | synthetic | true | 01 02 04 23 28 |
| trial | outcome_12w baseline coefficient | 0.6 | SD per baseline SD | synthetic | true | 01 02 04 23 28 |
| trial | outcome_12w noise SD | 0.8 | SD | synthetic | true | 01 02 04 23 28 |
| trial | hazard baseline coefficient | 0.3 | log-hazard per SD | synthetic | true | 01 02 04 23 28 |
| trial | hazard treatment coefficient (× adherence) | −0.5 | log-hazard | synthetic | true | 01 02 04 23 28 |
| trial | baseline mean time to event (exponential scale) | 180 | days | synthetic | true | 01 02 04 23 28 |
| trial | time_to_event clip range | 1–365 | days | synthetic | true | 01 02 04 23 28 |
| trial | event observed — P(event = 1), independent of time | 0.7 | probability | synthetic | true | 01 02 04 23 28 |
| vitals | `load_vitals` n_patients | 40 | count | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | hours per patient | 120 | hours | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | deterioration_rate — P(patient deteriorates) | 0.25 | probability | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | onset hour — uniform over this fraction of the stay | 0.3–0.8 | fraction of hours | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | deterioration ramp — hours to full effect | 12 | hours | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | deterioration ramp — cap | 1.5 | × full effect | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | hr — patient baseline mean | 78 | bpm | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | hr — patient baseline SD | 8 | bpm | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | hr — circadian amplitude | 3 | bpm | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | hr — deterioration shift at full ramp | +28 | bpm | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | hr — hourly noise SD | 3 | bpm | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | rr — patient baseline mean | 16 | breaths/min | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | rr — patient baseline SD | 2 | breaths/min | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | rr — circadian amplitude | 0.8 | breaths/min | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | rr — deterioration shift at full ramp | +9 | breaths/min | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | rr — hourly noise SD | 1 | breaths/min | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spo2 — patient baseline mean | 96.5 | % | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spo2 — patient baseline SD | 1.2 | % | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spo2 — circadian amplitude | −0.3 | % | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spo2 — deterioration shift at full ramp | −6 | % | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spo2 — hourly noise SD | 0.6 | % | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | sbp — patient baseline mean | 125 | mmHg | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | sbp — patient baseline SD | 12 | mmHg | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | sbp — circadian amplitude | 5 | mmHg | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | sbp — deterioration shift at full ramp | −25 | mmHg | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | sbp — hourly noise SD | 5 | mmHg | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | temp — patient baseline mean | 36.8 | °C | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | temp — patient baseline SD | 0.25 | °C | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | temp — circadian amplitude | 0.2 | °C | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | temp — deterioration shift at full ramp | +1.6 | °C | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | temp — hourly noise SD | 0.15 | °C | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spo2 clip range | 70–100 | % | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | sensor faults per patient — Poisson mean | 1.2 | faults | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | fault type — spike / stuck / dropout | 1/3 each | probability | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | spike size on hr | ±60 | bpm | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | stuck fault duration (hr, spo2 frozen) | 6 | hours | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| vitals | start timestamp | 2024-03-01 | date | synthetic | true | 01 03 04 05 10 17 18 22 23 24 |
| prescribing | `load_prescribing` n_patients | 10000 | count | synthetic | true | 01 09 28 |
| prescribing | age_band mix — 18-39 / 40-64 / 65-79 / 80+ | 0.20 / 0.35 / 0.30 / 0.15 | probability | synthetic | true | 01 09 28 |
| prescribing | condition classes per patient — Poisson(k) + 1, k by age band | k = 1 / 2 / 3 / 4 | classes | synthetic | true | 01 09 28 |
| prescribing | drug classes available (cardio, diabetes, respiratory, mental_health, pain, gi, anticoag) | 7 | count | synthetic | true | 01 09 28 |
| prescribing | drugs per class — Poisson(λ) + 1, capped at the class size | λ = 1.5 | drugs | synthetic | true | 01 09 28 |
| prescribing | adverse event — nsaid + warfarin or nsaid + doac | 1.0 | probability | synthetic | true | 01 09 28 |
| prescribing | adverse event — opioid + benzodiazepine | 1.0 | probability | synthetic | true | 01 09 28 |
| prescribing | adverse event — ssri + mirtazapine | 0.6 | probability | synthetic | true | 01 09 28 |
| cohort | `load_cohort` n — patients | 10000 | count | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | segment shares of n — healthy / rising_risk / chronic_stable / complex / frail (largest remainder) | 35 / 25 / 20 / 12 / 8 | % of n | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | segments | 5 | count | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | feature SD rule — max(0.18 × |segment mean|, 0.3) | 0.18; floor 0.3 | fraction; feature units | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | age — segment means, healthy / rising_risk / chronic_stable / complex / frail | 38 / 52 / 66 / 74 / 84 | years | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | bmi — segment means, healthy / rising_risk / chronic_stable / complex / frail | 24 / 29 / 30 / 28 / 23 | kg/m² | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | sbp — segment means, healthy / rising_risk / chronic_stable / complex / frail | 118 / 134 / 138 / 142 / 130 | mmHg | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | hba1c — segment means, healthy / rising_risk / chronic_stable / complex / frail | 5.3 / 5.9 / 7.1 / 7.8 / 6.4 | % | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | egfr — segment means, healthy / rising_risk / chronic_stable / complex / frail | 95 / 85 / 70 / 52 / 40 | mL/min/1.73m² | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | ldl — segment means, healthy / rising_risk / chronic_stable / complex / frail | 2.8 / 3.4 / 2.5 / 2.3 / 2.0 | mmol/L | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | gp_visits — segment means, healthy / rising_risk / chronic_stable / complex / frail | 1 / 3 / 6 / 12 / 15 | visits per year | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | ed_visits — segment means, healthy / rising_risk / chronic_stable / complex / frail | 0.1 / 0.3 / 0.6 / 2.2 / 3.5 | visits per year | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | meds — segment means, healthy / rising_risk / chronic_stable / complex / frail | 0.5 / 2 / 5 / 9 / 11 | medicines | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | smoker (Bernoulli) — segment means, healthy / rising_risk / chronic_stable / complex / frail | 0.10 / 0.25 / 0.15 / 0.10 / 0.03 | probability | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | alcohol — segment means, healthy / rising_risk / chronic_stable / complex / frail | 5 / 12 / 6 / 3 / 1 | units per week | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | activity — segment means, healthy / rising_risk / chronic_stable / complex / frail | 4 / 2.5 / 2 / 1 / 0.5 | sessions per week | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | sleep — segment means, healthy / rising_risk / chronic_stable / complex / frail | 7.2 / 6.6 / 6.4 / 5.8 / 5.5 | hours | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | pain — segment means, healthy / rising_risk / chronic_stable / complex / frail | 1 / 2.5 / 4 / 6 / 6.5 | score 0–10 | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | imd — uniform over (the segment means listed in code are overwritten) | 1–5 | quintile | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| cohort | sex — P(F) | 0.5 | probability | synthetic | true | 00 03 05 06 07 08 10 23 29 |
| notes | `load_notes` n — notes | 5000 | count | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | complaint categories (uniform) | 6 | count | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | symptoms per note | 2–4 | count | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | age in note — uniform | 18–94 | years | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | P(urgent) — cardiac / neuro / respiratory / abdominal / msk / minor | 0.70 / 0.75 / 0.40 / 0.35 / 0.15 / 0.05 | probability | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | P(urgent) multiplier when age > 70 | 1.3 | × | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | disposition if urgent — admit / treat_and_discharge | 0.75 / 0.25 | probability | synthetic | true | 05 08 12 17 18 21 24 28 |
| notes | disposition if routine — discharge / gp_follow_up / treat_and_discharge | 1/3 each | probability | synthetic | true | 05 08 12 17 18 21 24 28 |
| referrals | `load_referrals` n_nodes | 600 | count | synthetic | true | 13 20 |
| referrals | avg_degree — edges = n_nodes × avg_degree / 2 | 6 | edges per node | synthetic | true | 13 20 |
| referrals | sites | 5 | count | synthetic | true | 13 20 |
| referrals | specialty mix — gp / ed / cardiology / respiratory / radiology / pharmacy | 0.35 / 0.15 / 0.12 / 0.12 / 0.13 / 0.13 | probability | synthetic | true | 13 20 |
| referrals | node volume — exponential mean | 40 | referrals | synthetic | true | 13 20 |
| referrals | P(edge stays within the site) | 0.75 | probability | synthetic | true | 13 20 |
| referrals | hub weight — radiology and ed vs others | 4 : 1 | relative weight | synthetic | true | 13 20 |
| referrals | n_referrals per edge — Poisson(8) + 1 | 8 | referrals | synthetic | true | 13 20 |
| imaging | `load_imaging` n — patches | 4000 | count | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | patch size | 16 | pixels per side | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | P(lesion present) | 0.5 | probability | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | tissue texture — base intensity | 0.45 | intensity 0–1 | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | tissue texture — sinusoid amplitude | 0.08 | intensity 0–1 | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | tissue texture — spatial frequency range | 0.05–0.2 | cycles per pixel | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | pixel noise SD | 0.04 | intensity 0–1 | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | lesion centre range | 4 – size−4 | pixels | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | lesion radius range | 1.5–3.5 | pixels | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | lesion eccentricity range | 0.6–1.4 | ratio | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| imaging | lesion peak intensity range | 0.25–0.5 | intensity 0–1 | synthetic | true | 00 01 08 14 15 16 18 19 23 25 26 27 |
| evac | `load_evac` grid size | 6 | cells per side | synthetic | true | 21 24 |
| evac | P(terrain cell is slow going) | 0.2 | probability | synthetic | true | 21 24 |
| evac | P(cell is an exposed threat lane) | 0.15 | probability | synthetic | true | 21 24 |
| evac | step_cost | −0.04 | reward per step | synthetic | true | 21 24 |
| evac | terrain_cost | −0.08 | reward per slow step | synthetic | true | 21 24 |
| evac | threat_risk — per step in a threat lane | 0.1 | probability | synthetic | true | 21 24 |
| evac | role1_reward — stabilisation at Role 1 | 0.3 | reward | synthetic | true | 21 24 |
| evac | goal_reward — arrival at Role 2 | 1.0 | reward | synthetic | true | 21 24 |
| evac | clock_limit — size × 4 | 24 | steps | synthetic | true | 21 24 |
| areas | `load_areas` n_side — grid of n_side² areas | 7 | areas per side | synthetic | true | 23 28 |
| areas | n_facilities | 3 | count | synthetic | true | 23 28 |
| areas | population — lognormal median | 4000 | people | synthetic | true | 23 28 |
| areas | population — lognormal log-SD | 0.5 | log people | synthetic | true | 23 28 |
| areas | expected count per head — uniform range | 0.004–0.009 | cases per person | synthetic | true | 23 28 |
| areas | spatial bumps | 3 | count | synthetic | true | 23 28 |
| areas | spatial bump amplitude SD | 0.5 | log relative risk | synthetic | true | 23 28 |
| areas | spatial kernel bandwidth | 1.8 | cells | synthetic | true | 23 28 |
| areas | unstructured log-RR SD | 0.15 | log relative risk | synthetic | true | 23 28 |
| areas | travel time per cell of distance | 9 | minutes | synthetic | true | 23 28 |
| areas | travel time noise SD | 2 | minutes | synthetic | true | 23 28 |
| areas | travel time floor | 2 | minutes | synthetic | true | 23 28 |
| synthetic.dose_response | n | 300 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.dose_response | dose range — uniform | 0–10 | dose units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.dose_response | curve −a(d − d*)² + peak: curvature a | 0.08 | response per dose² | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.dose_response | optimal dose d* | 6 | dose units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.dose_response | peak response | 3.0 | response units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.dose_response | noise SD | 0.15 | response units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | n | 500 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | clean_linear coefficients | 3 / 1.5 / −2 | y per x | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | clean_linear intercept | 5 | y units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | clean_linear noise SD | 0.5 | y units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | heteroscedastic noise SD — 1 + 2|x0| | 1; 2 | y units; per |x0| | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | with_outliers — fraction of rows hit | 0.10 | fraction | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | with_outliers — outlier SD | 20 | y units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | multicollinear — copy-of-x0 noise SD | 0.05 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | multicollinear — y noise SD | 1 | y units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.regression_variants | nonlinear — sin(2x0) + x1² noise SD | 0.3 | y units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | n | 1000 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | separable — class_sep | 2.0 | SD | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | overlapping — class_sep | 0.5 | SD | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | moons — noise | 0.2 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | rings — noise | 0.1 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | rings — inner/outer factor | 0.5 | ratio | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | xor — noise SD | 0.1 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | rare_positive — class weights | 0.98 / 0.02 | probability | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | high_dimensional — features / informative / redundant | 50 / 5 / 10 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.classification_variants | triage — four classes T1 / T2 / T3 / T4 | 0.02 / 0.13 / 0.35 / 0.50 | probability | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | n | 1000 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | blobs — centres | 5 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | blobs — cluster SD | 1.0 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | variable_density — cluster SDs at x = −5 / 0 / 5 | 0.5 / 2.0 / 0.8 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | with_noise — uniform noise points (n / 5) over ± | 15 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | spirals — turns (t up to 3π) | 1.5 | turns | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | spirals — noise SD | 0.3 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | moons — noise | 0.1 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.clustering_variants | rings — noise; factor | 0.05; 0.5 | x units; ratio | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | n | 1095 | days | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | base level | 120 | attendances per day | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | trend | 0.02 | attendances per day per day | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | weekly amplitude | 8 | attendances | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | winter surge amplitude | 15 | attendances | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | winter peak day of year | 15 | day | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | noise SD | 4 | attendances | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | changepoint at n / 2 — step | +25 | attendances | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | outlier rate; outlier SD | 0.015; 50 | fraction; attendances | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.time_series_variants | random_walk step SD | 2 | attendances | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.manifold_variants | n | 1000 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.manifold_variants | swiss_roll noise | 0.5 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.manifold_variants | s_curve noise | 0.1 | x units | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.bandit_arms | k — treatment arms | 5 | count | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
| synthetic.bandit_arms | hidden response rates — uniform range | 0.15–0.55 | probability | synthetic | true | 00 01 02 03 04 05 07 08 11 15 16 17 18 19 20 21 24 27 28 |
