# Module 18 — Transformers

**Tier** 3 · **Notebooks** 10 · **Prerequisites** 17

> Attention over notes, codes and images.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Query, Key, Value](01_attention/01_query_key_value.ipynb) | P1 | predict | `notes` | `vaswani2017` | 'Patient reports chest pain; it started yesterday' — what does 'it' attend to? |
| 01.02 | [Multi-Head & Positional Encoding](01_attention/02_multi_head_positional_encoding.ipynb) | P1 | predict | `notes` |  | Heads; word order in notes |
| 02.01 | [Full Transformer](02_architectures/01_full_transformer.ipynb) | P1 | predict | `notes` |  | Code→description from scratch |
| 02.02 | [BERT](02_architectures/02_bert.ipynb) | P1 | predict | `notes` | `ClinicalBERT-style fine-tuning` | Masked LM on triage notes; fine-tune for urgency — and what a 'physician-level' benchmark actually measured |
| 02.03 | [GPT](02_architectures/03_gpt.ipynb) | P1 | predict | `notes` | `kaplan2020` | Discharge summary generation; scaling laws |
| 02.04 | [T5 & Vision Transformers](02_architectures/04_t5_vision_transformers.ipynb) | P1 | predict | `imaging` |  | Text-to-text; lesion patches as tokens |
| 03.01 | [Swin, DeiT & CLIP](03_variants/01_swin_deit_clip.ipynb) | P1 | predict | `imaging` |  | Windows; small-data distillation; image–report pairing |
| 03.02 | [Mixture of Experts](03_variants/02_mixture_of_experts.ipynb) | P1 | predict | `notes` |  | Specialty-routed experts |
| 03.03 | [Flash Attention & Efficient Variants](03_variants/03_flash_attention_efficient_variants.ipynb) | P4 | predict | `synthetic` | `lester2021` | Long records |
| 03.04 | [State Space Models — S4, Mamba](03_variants/04_state_space_models_s4_mamba.ipynb) | P4 | predict | `vitals` | `gu2024` | Long vitals sequences |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 18_transformers` gates the module.
