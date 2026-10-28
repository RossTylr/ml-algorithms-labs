# Module 17 — RNNs & Sequences

**Tier** 3 · **Notebooks** 6 · **Prerequisites** 15

> Physiology and notes unfold in time.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Vanilla RNN & BPTT](01_rnn/01_vanilla_rnn_bptt.ipynb) | P1 | predict | `notes` |  | Character-level clinical notes |
| 01.02 | [LSTM & GRU](01_rnn/02_lstm_gru.ipynb) | P4 | predict | `vitals` | `rajkomar2018` | Rajkomar-style: a patient's admission timeline as a sequence → mortality; long-range deterioration on vitals |
| 01.03 | [Bidirectional & Seq2Seq](01_rnn/03_bidirectional_seq2seq.ipynb) | P1 | predict | `notes` |  | Note classification; code→description |
| 02.01 | [Bahdanau & Luong Attention](02_attention/01_bahdanau_luong_attention.ipynb) | P1 | predict | `notes` |  | Which words drove the triage decision |
| 03.01 | [TCN & WaveNet](03_convolutional_sequences/01_tcn_wavenet.ipynb) | P4 | predict | `vitals` | `zeng2022` | Vitals forecasting; waveform |
| 03.02 | [Neural ODEs](03_convolutional_sequences/02_neural_odes.ipynb) | P2 | decide | `synthetic` |  | Pharmacokinetic trajectories |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 17_sequences` checks all of it.
