# Module 21 — Reinforcement Learning

**Tier** 3 · **Notebooks** 15 · **Prerequisites** 00, 15

> Sequential decisions under uncertainty — dosing, evacuation, resource allocation.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Exploration vs Exploitation](01_bandits/01_exploration_vs_exploitation.ipynb) | P3 | decide | `synthetic` |  | Five treatment arms with unknown response rates — adaptive trial design — in the spirit of adaptive / response-adaptive randomisation |
| 02.01 | [MDPs & Dynamic Programming](02_tabular/01_mdps_dynamic_programming.ipynb) | P5 | decide | `evac` |  | Casualty evacuation on a 4×4 grid — point of injury to Role 2 |
| 02.02 | [Monte Carlo & TD Learning](02_tabular/02_monte_carlo_td_learning.ipynb) | P5 | decide | `evac` |  | Same, dynamics unknown |
| 02.03 | [Q-Learning & SARSA](02_tabular/03_q_learning_sarsa.ipynb) | P5 | decide | `evac` |  | A threat lane — safe route vs fastest route |
| 02.04 | [TD(λ) & Eligibility Traces](02_tabular/04_tdλ_eligibility_traces.ipynb) | P5 | decide | `evac` |  | Same |
| 03.01 | [DQN](03_value_based/01_dqn.ipynb) | P4 | predict | `synthetic` | `mnih2015` | Bed allocation under stochastic arrivals |
| 03.02 | [Double, Dueling, PER & Rainbow](03_value_based/02_double_dueling_per_rainbow.ipynb) | P4 | predict | `synthetic` |  | Fixing DQN |
| 04.01 | [REINFORCE & Actor-Critic](04_policy_based/01_reinforce_actor_critic.ipynb) | P2 | decide | `synthetic` |  | Dose titration as a policy |
| 04.02 | [A2C/A3C & PPO](04_policy_based/02_a2c_a3c_ppo.ipynb) | P2 | decide | `synthetic` |  | Continuous dosing |
| 04.03 | [TRPO, SAC, DDPG & TD3](04_policy_based/03_trpo_sac_ddpg_td3.ipynb) | P2 | decide | `synthetic` |  | Infusion control — continuous family |
| 05.01 | [Dyna-Q & World Models](05_model_based/01_dyna_q_world_models.ipynb) | P5 | decide | `evac` |  | Learned evacuation dynamics, imagined rollouts |
| 05.02 | [MuZero & Dreamer](05_model_based/02_muzero_dreamer.ipynb) | P5 | decide | `evac` |  | Planning with learned models |
| 06.01 | [Hierarchical, Inverse & Multi-Agent RL](06_advanced_rl/01_hierarchical_inverse_multi_agent_rl.ipynb) | P5 | decide | `evac` |  | Sub-goals along the chain; recover a commander's reward from demonstrations; two evac teams cooperating |
| 06.02 | [Offline RL](06_advanced_rl/02_offline_rl.ipynb) | P2 | decide | `admissions` |  | Learning a treatment policy from a fixed registry — CQL, IQL — in the spirit of AI Clinician (sepsis) offline-RL debate |
| 06.03 | [RLHF & DPO](06_advanced_rl/03_rlhf_dpo.ipynb) | P1 | predict | `notes` | `chen2025` | Preference learning from clinician rankings of note summaries |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 21_reinforcement_learning` gates the module.
