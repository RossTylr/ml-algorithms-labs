# Module 17 — RNNs & Sequences

**Tier** 3 · **Notebooks** 6 · **Prerequisites** 15

> Physiology and notes unfold in time.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Vanilla RNN & BPTT](01_rnn/01_vanilla_rnn_bptt.ipynb) | P1 | `notes` | Character-level clinical notes |
| 01.02 | [LSTM & GRU](01_rnn/02_lstm_gru.ipynb) | P4 | `vitals` | Vitals long-range deterioration; note generation |
| 01.03 | [Bidirectional & Seq2Seq](01_rnn/03_bidirectional_seq2seq.ipynb) | P1 | `notes` | Note classification; code→description |
| 02.01 | [Bahdanau & Luong Attention](02_attention/01_bahdanau_luong_attention.ipynb) | P1 | `notes` | Which words drove the triage decision |
| 03.01 | [TCN & WaveNet](03_convolutional_sequences/01_tcn_wavenet.ipynb) | P4 | `vitals` | Vitals forecasting; waveform |
| 03.02 | [Neural ODEs](03_convolutional_sequences/02_neural_odes.ipynb) | P2 | `synthetic` | Pharmacokinetic trajectories |

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
