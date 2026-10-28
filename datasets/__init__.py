"""
datasets — ten synthetic clinical companion datasets. All deterministic under SEED=42.

Every generator builds its outcome from a KNOWN mechanism, so notebooks can check an algorithm against
the truth. Nothing here is real patient data. Reference studies in curriculum.yaml are "in the spirit of".

    from datasets import load_screening, load_admissions, load_trial, load_vitals, load_prescribing,
                         load_cohort, load_notes, load_referrals, load_imaging, load_evac
    from datasets import synthetic
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 42


def _rng(seed):
    return np.random.RandomState(seed)


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


# ─────────────────────────── P1 screening ───────────────────────────
def load_screening(n=2000, n_biomarkers=12, prevalence=0.15, seed=SEED, return_truth=False):
    """
    Biomarker panel + disease status. Two biomarkers are strongly informative, three weakly,
    the rest noise. One pair is collinear by construction (for VIF notebooks).

    Columns: age, sex, bm_01..bm_12, disease (0/1)
    Truth (return_truth=True): dict with informative indices and the generating log-odds.
    """
    r = _rng(seed)
    disease = r.binomial(1, prevalence, n)
    age = r.normal(55, 14, n).clip(18, 95)
    sex = r.choice(["F", "M"], n)

    X = r.normal(0, 1, (n, n_biomarkers))
    # strong: bm_01, bm_02 ; weak: bm_03..bm_05 ; collinear: bm_12 ≈ bm_01
    X[:, 0] += 1.6 * disease
    X[:, 1] += 1.2 * disease + 0.3 * (age - 55) / 14
    X[:, 2] += 0.5 * disease
    X[:, 3] += 0.4 * disease
    X[:, 4] += 0.3 * disease
    X[:, 11] = X[:, 0] + r.normal(0, 0.1, n)

    df = pd.DataFrame(X, columns=[f"bm_{i + 1:02d}" for i in range(n_biomarkers)])
    df.insert(0, "sex", sex)
    df.insert(0, "age", age.round(1))
    df["disease"] = disease
    if return_truth:
        return df, {"strong": ["bm_01", "bm_02"], "weak": ["bm_03", "bm_04", "bm_05"], "collinear": ("bm_12", "bm_01"), "prevalence": prevalence}
    return df


# ─────────────────────────── P2 admissions ───────────────────────────
def load_admissions(n=5000, seed=SEED, start="2022-01-01"):
    """
    Acute admissions with LOS, 30-day readmission and in-hospital mortality driven by a known model.
    Includes a daily arrival series usable for time-series notebooks (groupby admit_date).

    Columns: patient_id, admit_date, age, sex, department, admission_type, severity (1-10),
             comorbidity_count, prior_admissions, deprivation_quintile, gp_practice,
             los_days, readmit_30d, died, discharge_destination (leaks `died` — for leakage notebooks)
    """
    r = _rng(seed)
    days = r.exponential(1.0, n).cumsum()
    days = (days / days.max() * 1095).astype(int)  # ~3 years
    admit = pd.to_datetime(start) + pd.to_timedelta(days, unit="D")
    # weekly seasonality + winter surge for the arrival series
    dow = admit.dayofweek.values
    weekend = (dow >= 5)

    age = r.normal(62, 18, n).clip(18, 98)
    sex = r.choice(["F", "M"], n)
    dept = r.choice(["cardiology", "respiratory", "general_medicine", "orthopaedics", "surgery"], n, p=[0.2, 0.2, 0.3, 0.15, 0.15])
    adm_type = r.choice(["emergency", "elective", "urgent"], n, p=[0.55, 0.3, 0.15])
    severity = r.uniform(1, 10, n).round(1)
    comorb = r.poisson(1.8, n).clip(0, 9)
    prior = r.poisson(0.7, n).clip(0, 12)
    imd = r.choice([1, 2, 3, 4, 5], n)
    practice = r.choice([f"P{i:03d}" for i in range(400)], n)

    los = np.exp(0.2 + 0.012 * age + 0.11 * severity + 0.09 * comorb + 0.25 * (adm_type == "emergency")
                 + 0.15 * (dept == "orthopaedics") + r.normal(0, 0.45, n)).clip(0.5, 90)
    p_readmit = _sigmoid(-3.6 + 0.02 * (age - 62) + 0.22 * severity + 0.35 * comorb + 0.30 * prior + 0.10 * (imd - 3))
    readmit = r.binomial(1, p_readmit)
    p_died = _sigmoid(-6.0 + 0.04 * (age - 62) + 0.35 * severity + 0.2 * comorb)
    died = r.binomial(1, p_died)
    dest = np.where(died == 1, "mortuary", r.choice(["home", "care_home", "rehab"], n, p=[0.75, 0.15, 0.1]))
    readmit = np.where(died == 1, 0, readmit)

    return pd.DataFrame({
        "patient_id": r.choice(np.arange(1, n // 2), n),  # repeat patients by design (group splits)
        "admit_date": admit, "age": age.round(0).astype(int), "sex": sex, "department": dept,
        "admission_type": adm_type, "severity": severity, "comorbidity_count": comorb,
        "prior_admissions": prior, "deprivation_quintile": imd, "gp_practice": practice,
        "weekend_admission": weekend.astype(int),
        "los_days": los.round(1), "readmit_30d": readmit, "died": died, "discharge_destination": dest,
    }).sort_values("admit_date").reset_index(drop=True)


# ─────────────────────────── P3 trial ───────────────────────────
def load_trial(n=800, true_effect=-0.35, seed=SEED, return_truth=False):
    """
    Two-arm RCT. Outcome = standardised symptom score at 12 weeks (lower = better).
    Treatment effect is `true_effect` SD, heterogeneous by baseline severity. Adherence and
    censoring included for ITT vs per-protocol and survival notebooks.

    Columns: arm (control/treatment), age, sex, site (1-5), baseline_score, adherence (0-1),
             outcome_12w, time_to_event_days, event (1 observed / 0 censored)
    """
    r = _rng(seed)
    arm = r.choice(["control", "treatment"], n)
    t = (arm == "treatment").astype(float)
    age = r.normal(58, 12, n).clip(18, 90)
    sex = r.choice(["F", "M"], n)
    site = r.choice([1, 2, 3, 4, 5], n)
    baseline = r.normal(0, 1, n)
    adherence = np.where(t == 1, r.beta(5, 1.5, n), 1.0)
    site_fx = r.normal(0, 0.15, 5)[site - 1]
    effect = true_effect * (1 + 0.4 * baseline) * adherence  # heterogeneous + diluted by non-adherence
    outcome = 0.6 * baseline + t * effect + site_fx + r.normal(0, 0.8, n)

    hazard = np.exp(0.3 * baseline - 0.5 * t * adherence)
    tte = r.exponential(180 / hazard).clip(1, 365)
    event = r.binomial(1, 0.7, n)

    df = pd.DataFrame({
        "arm": arm, "age": age.round(0).astype(int), "sex": sex, "site": site,
        "baseline_score": baseline.round(2), "adherence": adherence.round(2),
        "outcome_12w": outcome.round(2), "time_to_event_days": tte.round(0).astype(int), "event": event,
    })
    if return_truth:
        return df, {"true_effect_sd": true_effect, "heterogeneity_slope": 0.4}
    return df


# ─────────────────────────── P4 vitals ───────────────────────────
def load_vitals(n_patients=40, hours=120, deterioration_rate=0.25, seed=SEED):
    """
    Hourly vitals per patient over `hours`. A fraction deteriorate: from a random onset hour,
    HR and RR climb, SpO2 and SBP fall, temp rises, over ~12h. Sensor faults (spike, stuck, dropout)
    injected at low rate for anomaly notebooks.

    Columns: patient_id, hour, timestamp, hr, rr, spo2, sbp, temp,
             deteriorating (0/1 ground truth), onset_hour (NaN if never), fault_type (none/spike/stuck/dropout)
    """
    r = _rng(seed)
    rows = []
    t0 = pd.Timestamp("2024-03-01")
    for pid in range(n_patients):
        base = dict(hr=r.normal(78, 8), rr=r.normal(16, 2), spo2=r.normal(96.5, 1.2), sbp=r.normal(125, 12), temp=r.normal(36.8, 0.25))
        det = r.random() < deterioration_rate
        onset = int(r.uniform(hours * 0.3, hours * 0.8)) if det else np.nan
        h = np.arange(hours)
        circ = np.sin(2 * np.pi * (h % 24) / 24)
        ramp = np.zeros(hours)
        if det:
            ramp = np.clip((h - onset) / 12, 0, 1.5)
        hr = base["hr"] + 3 * circ + 28 * ramp + r.normal(0, 3, hours)
        rr = base["rr"] + 0.8 * circ + 9 * ramp + r.normal(0, 1, hours)
        spo2 = (base["spo2"] - 0.3 * circ - 6 * ramp + r.normal(0, 0.6, hours)).clip(70, 100)
        sbp = base["sbp"] + 5 * circ - 25 * ramp + r.normal(0, 5, hours)
        temp = base["temp"] + 0.2 * circ + 1.6 * ramp + r.normal(0, 0.15, hours)
        fault = np.array(["none"] * hours, dtype=object)
        for _ in range(r.poisson(1.2)):
            k = r.randint(0, hours); kind = r.choice(["spike", "stuck", "dropout"])
            fault[k] = kind
            if kind == "spike": hr[k] += r.choice([-1, 1]) * 60
            elif kind == "stuck":
                e = min(hours, k + 6); hr[k:e] = hr[k]; spo2[k:e] = spo2[k]; fault[k:e] = "stuck"
            else: spo2[k] = np.nan; sbp[k] = np.nan
        rows.append(pd.DataFrame({
            "patient_id": pid, "hour": h, "timestamp": t0 + pd.to_timedelta(h, unit="h"),
            "hr": hr.round(0), "rr": rr.round(0), "spo2": spo2.round(1), "sbp": sbp.round(0), "temp": temp.round(1),
            "deteriorating": int(det), "onset_hour": onset, "fault_type": fault,
        }))
    return pd.concat(rows, ignore_index=True)


# ─────────────────────────── P2 prescribing ───────────────────────────
DRUG_CLASSES = {
    "cardio": ["statin", "ace_inhibitor", "beta_blocker", "aspirin", "ccb", "diuretic"],
    "diabetes": ["metformin", "sulfonylurea", "sglt2", "insulin"],
    "respiratory": ["saba", "ics", "laba", "lama"],
    "mental_health": ["ssri", "benzodiazepine", "antipsychotic", "mirtazapine"],
    "pain": ["paracetamol", "nsaid", "opioid", "gabapentinoid"],
    "gi": ["ppi", "laxative", "antiemetic"],
    "anticoag": ["warfarin", "doac", "lmwh"],
}


def load_prescribing(n_patients=10000, seed=SEED, as_frame=False):
    """
    Per-patient medication baskets with comorbidity codes. Co-prescription within a class is common;
    certain pairs (nsaid+anticoag, opioid+benzodiazepine, two serotonergics) raise an adverse-event flag.

    Returns list of baskets (default) or a long DataFrame (as_frame=True) with columns
    patient_id, age_band, item, kind (drug/condition), adverse_event.
    """
    r = _rng(seed)
    baskets, meta = [], []
    for pid in range(n_patients):
        age_band = r.choice(["18-39", "40-64", "65-79", "80+"], p=[0.2, 0.35, 0.3, 0.15])
        k = {"18-39": 1, "40-64": 2, "65-79": 3, "80+": 4}[age_band]
        n_classes = min(r.poisson(k) + 1, len(DRUG_CLASSES))
        classes = r.choice(list(DRUG_CLASSES), n_classes, replace=False)
        items = set()
        for c in classes:
            items.add(f"cond:{c}")
            drugs = DRUG_CLASSES[c]
            items.update(r.choice(drugs, min(len(drugs), r.poisson(1.5) + 1), replace=False))
        ae = int(({"nsaid", "warfarin"} <= items) or ({"nsaid", "doac"} <= items)
                 or ({"opioid", "benzodiazepine"} <= items) or ({"ssri", "mirtazapine"} <= items and r.random() < 0.6))
        baskets.append(sorted(items)); meta.append((pid, age_band, ae))
    if not as_frame:
        return baskets
    rows = [(pid, ab, it, "condition" if it.startswith("cond:") else "drug", ae) for (pid, ab, ae), b in zip(meta, baskets) for it in b]
    return pd.DataFrame(rows, columns=["patient_id", "age_band", "item", "kind", "adverse_event"])


# ─────────────────────────── P1 cohort ───────────────────────────
def load_cohort(n=10000, seed=SEED):
    """
    Population health records with five latent risk segments (ground truth in `segment`).
    15 numeric features; segments differ in means and spreads so clustering is learnable but not trivial.
    """
    r = _rng(seed)
    segs = {
        "healthy":        (3500, dict(age=38, bmi=24, sbp=118, hba1c=5.3, egfr=95, ldl=2.8, gp_visits=1, ed_visits=0.1, meds=0.5, smoker=0.1, alcohol=5, activity=4, imd=3, sleep=7.2, pain=1)),
        "rising_risk":    (2500, dict(age=52, bmi=29, sbp=134, hba1c=5.9, egfr=85, ldl=3.4, gp_visits=3, ed_visits=0.3, meds=2, smoker=0.25, alcohol=12, activity=2.5, imd=3.4, sleep=6.6, pain=2.5)),
        "chronic_stable": (2000, dict(age=66, bmi=30, sbp=138, hba1c=7.1, egfr=70, ldl=2.5, gp_visits=6, ed_visits=0.6, meds=5, smoker=0.15, alcohol=6, activity=2, imd=3.5, sleep=6.4, pain=4)),
        "complex":        (1200, dict(age=74, bmi=28, sbp=142, hba1c=7.8, egfr=52, ldl=2.3, gp_visits=12, ed_visits=2.2, meds=9, smoker=0.1, alcohol=3, activity=1, imd=3.8, sleep=5.8, pain=6)),
        "frail":          (800,  dict(age=84, bmi=23, sbp=130, hba1c=6.4, egfr=40, ldl=2.0, gp_visits=15, ed_visits=3.5, meds=11, smoker=0.03, alcohol=1, activity=0.5, imd=3.6, sleep=5.5, pain=6.5)),
    }
    frames = []
    for name, (cnt, mu) in segs.items():
        d = {k: r.normal(v, max(abs(v) * 0.18, 0.3), cnt) for k, v in mu.items()}
        d["smoker"] = r.binomial(1, mu["smoker"], cnt)
        d["imd"] = r.choice([1, 2, 3, 4, 5], cnt)
        df = pd.DataFrame(d); df["segment"] = name; frames.append(df)
    out = pd.concat(frames, ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)
    for c in ["age", "gp_visits", "ed_visits", "meds", "pain"]:
        out[c] = out[c].clip(lower=0).round(0)
    out["sex"] = r.choice(["F", "M"], len(out))
    return out


# ─────────────────────────── P1 notes ───────────────────────────
_SYMPTOMS = {
    "cardiac": ["chest pain", "radiating to arm", "shortness of breath", "sweating", "palpitations"],
    "respiratory": ["cough", "wheeze", "shortness of breath", "fever", "productive sputum"],
    "neuro": ["headache", "confusion", "weakness one side", "slurred speech", "visual disturbance"],
    "abdominal": ["abdominal pain", "vomiting", "diarrhoea", "no appetite", "bloating"],
    "msk": ["ankle pain", "fell", "swelling", "unable to weight bear", "bruising"],
    "minor": ["sore throat", "mild headache", "runny nose", "tired", "feels generally unwell"],
}
_URGENT = {"cardiac": 0.7, "neuro": 0.75, "respiratory": 0.4, "abdominal": 0.35, "msk": 0.15, "minor": 0.05}


def load_notes(n=5000, seed=SEED):
    """
    Short synthetic triage notes with presenting complaint, urgency (1 urgent / 0 routine) and
    disposition. Template-generated so topic structure is recoverable by LSA/LDA.
    Columns: note, complaint, urgent, disposition
    """
    r = _rng(seed)
    rows = []
    for _ in range(n):
        c = r.choice(list(_SYMPTOMS))
        k = r.randint(2, 5)
        sx = list(r.choice(_SYMPTOMS[c], k, replace=False))
        dur = r.choice(["since this morning", "for two days", "for a week", "started suddenly", "on and off for months"])
        age = r.randint(18, 95)
        note = f"{age}yo presents with {', '.join(sx)} {dur}. "
        urgent = int(r.random() < _URGENT[c] * (1.3 if age > 70 else 1.0))
        note += r.choice(["obs stable.", "looks unwell.", "pain score 7/10.", "no red flags.", "previous similar episode."])
        dispo = r.choice(["admit", "treat_and_discharge"], p=[0.75, 0.25]) if urgent else r.choice(["discharge", "gp_follow_up", "treat_and_discharge"])
        rows.append((note, c, urgent, dispo))
    return pd.DataFrame(rows, columns=["note", "complaint", "urgent", "disposition"])


# ─────────────────────────── P4 referrals ───────────────────────────
def load_referrals(n_nodes=600, avg_degree=6, seed=SEED):
    """
    Referral network between clinicians/teams across 5 sites and 6 specialties (community structure
    by site, hub structure by specialty). Returns (nodes_df, edges_df).
    """
    r = _rng(seed)
    site = r.choice(range(5), n_nodes)
    spec = r.choice(["gp", "ed", "cardiology", "respiratory", "radiology", "pharmacy"], n_nodes, p=[0.35, 0.15, 0.12, 0.12, 0.13, 0.13])
    nodes = pd.DataFrame({"node_id": range(n_nodes), "site": site, "specialty": spec, "volume": r.exponential(40, n_nodes).round(0)})
    edges, seen = [], set()
    target = n_nodes * avg_degree // 2
    hubs = np.isin(spec, ["radiology", "ed"])
    while len(edges) < target:
        u = r.randint(n_nodes)
        pool = np.where(site == site[u])[0] if r.random() < 0.75 else np.arange(n_nodes)
        w = 1.0 + 3.0 * hubs[pool]
        v = r.choice(pool, p=w / w.sum())
        if u != v and (u, v) not in seen and (v, u) not in seen:
            seen.add((u, v)); edges.append((u, v, int(r.poisson(8) + 1)))
    return nodes, pd.DataFrame(edges, columns=["source", "target", "n_referrals"])


# ─────────────────────────── P1 imaging ───────────────────────────
def load_imaging(n=4000, size=16, seed=SEED, return_masks=False):
    """
    Synthetic lesion patches. Background: smooth tissue texture + noise. Positive patches contain a
    blob (lesion) with random position, radius, intensity and eccentricity. Ground-truth masks available
    for segmentation notebooks.

    Returns X (n, size, size) float32 in [0,1], y (n,) int; plus masks (n, size, size) if requested.
    """
    r = _rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    X = np.zeros((n, size, size), dtype=np.float32)
    M = np.zeros((n, size, size), dtype=np.uint8)
    y = r.binomial(1, 0.5, n)
    for i in range(n):
        tex = 0.45 + 0.08 * np.sin(2 * np.pi * (xx * r.uniform(0.05, 0.2) + yy * r.uniform(0.05, 0.2)) + r.uniform(0, 6))
        img = tex + r.normal(0, 0.04, (size, size))
        if y[i]:
            cx, cy = r.uniform(4, size - 4, 2); rad = r.uniform(1.5, 3.5); ecc = r.uniform(0.6, 1.4)
            d = ((xx - cx) / ecc) ** 2 + ((yy - cy) * ecc) ** 2
            mask = d < rad ** 2
            img = img + mask * r.uniform(0.25, 0.5) * np.exp(-d / (2 * rad ** 2))
            M[i] = mask
        X[i] = np.clip(img, 0, 1)
    if return_masks:
        return X, y, M
    return X, y


# ─────────────────────────── P5 evac ───────────────────────────
def load_evac(size=6, seed=SEED):
    """
    Casualty evacuation grid. Start = point of injury, goal = Role 2. Terrain cells cost extra
    time; threat cells carry a per-step risk; a Role 1 cell gives a partial reward (stabilisation).
    Returns a dict consumable by a tiny GridWorld env in shared/rl.py.
    """
    r = _rng(seed)
    terrain = (r.random((size, size)) < 0.2).astype(int)   # 1 = slow going
    threat = (r.random((size, size)) < 0.15).astype(int)   # 1 = exposed lane
    terrain[0, 0] = terrain[-1, -1] = 0; threat[0, 0] = threat[-1, -1] = 0
    return {
        "size": size, "start": (0, 0), "goal": (size - 1, size - 1), "role1": (size // 2, size // 2),
        "terrain": terrain, "threat": threat,
        "step_cost": -0.04, "terrain_cost": -0.08, "threat_risk": 0.1, "role1_reward": 0.3, "goal_reward": 1.0,
        "clock_limit": size * 4,
    }


# ─────────────────────────── P1/P5 areas (disease mapping, access) ───────────────────────────
def load_areas(n_side=7, n_facilities=3, seed=SEED, return_truth=False):
    """
    Synthetic small areas on an n_side×n_side grid (default 49 ≈ 50). Each area has population, expected
    count (from age structure), and observed count drawn with relative risk = exp(spatial + unstructured).
    The spatial component is a smooth field (Gaussian kernel on the grid), so neighbouring areas share risk —
    exactly what a BYM/CAR model is built to recover. Facilities sit on a few cells for 2SFCA.

    Returns areas_df (area_id, row, col, population, expected, observed, has_facility, travel_min_to_nearest)
    and adjacency (queen) as a dict {area_id: [neighbour ids]}. return_truth adds the true log-RR components.
    """
    r = _rng(seed)
    n = n_side * n_side
    rows, cols = np.divmod(np.arange(n), n_side)
    pop = r.lognormal(np.log(4000), 0.5, n).astype(int)
    expected = pop * r.uniform(0.004, 0.009, n)
    # smooth spatial field: kernel-weighted sum of a few random bumps
    bumps = r.uniform(0, n_side - 1, (3, 2)); amp = r.normal(0, 0.5, 3)
    d2 = ((rows[:, None] - bumps[:, 0]) ** 2 + (cols[:, None] - bumps[:, 1]) ** 2)
    spatial = (amp * np.exp(-d2 / (2 * 1.8 ** 2))).sum(1)
    unstructured = r.normal(0, 0.15, n)
    rr = np.exp(spatial + unstructured)
    observed = r.poisson(expected * rr)
    fac = np.zeros(n, int); fac[r.choice(n, n_facilities, replace=False)] = 1
    fr, fc = rows[fac == 1], cols[fac == 1]
    dist = np.sqrt((rows[:, None] - fr) ** 2 + (cols[:, None] - fc) ** 2).min(1)
    travel = (dist * 9 + r.normal(0, 2, n)).clip(2, None).round(0)
    df = pd.DataFrame({"area_id": np.arange(n), "row": rows, "col": cols, "population": pop,
                       "expected": expected.round(2), "observed": observed, "has_facility": fac,
                       "travel_min_to_nearest": travel})
    adj = {}
    for i in range(n):
        nb = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0: continue
                rr_, cc_ = rows[i] + dr, cols[i] + dc
                if 0 <= rr_ < n_side and 0 <= cc_ < n_side:
                    nb.append(int(rr_ * n_side + cc_))
        adj[i] = nb
    if return_truth:
        return df, adj, {"log_rr": spatial + unstructured, "spatial": spatial, "unstructured": unstructured}
    return df, adj


from . import synthetic  # noqa: E402,F401
