# Module 15 — Neural Network Foundations

**Tier** 2 · **Notebooks** 9 · **Prerequisites** 00, 05

> From scratch before any framework.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Perceptron](01_neurons/01_perceptron.ipynb) | P1 | predict | `synthetic` |  | Separable, then XOR |
| 01.02 | [MLP — Hidden Layers & Activations](01_neurons/02_mlp_hidden_layers_activations.ipynb) | P1 | predict | `imaging` | `rumelhart1986` | XOR solved; lesion patches |
| 01.03 | [Universal Approximation](01_neurons/03_universal_approximation.ipynb) | P2 | decide | `synthetic` |  | Any dose–response curve with enough neurons |
| 02.01 | [Chain Rule on a Computational Graph](02_backprop/01_chain_rule_on_a_computational_graph.ipynb) | P1 | predict | `synthetic` | `rumelhart1986` | A 2-1-1 network by hand and by autograd |
| 03.01 | [Optimisers — SGD, Momentum, Adam](03_training/01_optimisers_sgd_momentum_adam.ipynb) | P1 | predict | `synthetic` |  | 2D loss surface |
| 03.02 | [Learning Rate Schedules](03_training/02_learning_rate_schedules.ipynb) | P1 | predict | `imaging` |  | Lesion classifier training |
| 03.03 | [Regularisation — Dropout, BatchNorm, Weight Decay](03_training/03_regularisation_dropout_batchnorm_weight_decay.ipynb) | P1 | predict | `imaging` | `gal2016` | Overfitting a small radiology set |
| 03.04 | [Weight Initialisation](03_training/04_weight_initialisation.ipynb) | P1 | predict | `imaging` |  | Deep MLP stability |
| 03.05 | [Loss Functions](03_training/05_loss_functions.ipynb) | P1 | predict | `imaging` | `frankle2019` | CE, focal (rare lesions), triplet, hinge |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 15_neural_foundations` gates the module.
