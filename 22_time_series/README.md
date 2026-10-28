# Module 22 — Time Series & Forecasting

**Tier** 2 · **Notebooks** 9 · **Prerequisites** 02, 04, 17

> Demand, vitals and outbreaks over time.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Moving Averages & Exponential Smoothing](01_smoothing/01_moving_averages_exponential_smoothing.ipynb) | P4 | predict | `admissions` |  | Three years of daily ED attendances |
| 02.01 | [Stationarity, ACF & PACF](02_arima/01_stationarity_acf_pacf.ipynb) | P4 | predict | `admissions` |  | Attendances — order selection |
| 02.02 | [ARIMA, SARIMA & SARIMAX](02_arima/02_arima_sarima_sarimax.ipynb) | P4 | predict | `admissions` |  | Weekly seasonality; bank holidays as exogenous |
| 02.03 | [VAR & Granger Causality](02_arima/03_var_granger_causality.ipynb) | P4 | predict | `admissions` |  | Five sites — does one site's surge predict another's? |
| 03.01 | [Prophet, TBATS & Theta](03_decomposition/01_prophet_tbats_theta.ipynb) | P4 | predict | `admissions` | `taylor2018` | Changepoints (a service redesign), multi-seasonality, benchmarks |
| 04.01 | [DeepAR & N-BEATS](04_deep/01_deepar_n_beats.ipynb) | P4 | predict | `admissions` |  | Probabilistic bed demand |
| 04.02 | [TFT, Informer & PatchTST](04_deep/02_tft_informer_patchtst.ipynb) | P4 | predict | `vitals` |  | Multi-horizon vitals |
| 04.03 | [Foundation Models — TimesFM, Chronos](04_deep/03_foundation_models_timesfm_chronos.ipynb) | P4 | predict | `admissions` |  | Zero-shot demand |
| 05.01 | [DTW, Matrix Profile & Changepoints](05_analysis/01_dtw_matrix_profile_changepoints.ipynb) | P4 | predict | `vitals` |  | Similar vital trajectories; recurring motifs; the moment deterioration began |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 22_time_series` gates the module.
