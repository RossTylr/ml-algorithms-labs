# Module 19 — Generative Models

**Tier** 3 · **Notebooks** 12 · **Prerequisites** 15, 16, 18

> Synthetic patients, augmented images, privacy-preserving data.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [AE, Denoising & Sparse](01_autoencoders/01_ae_denoising_sparse.ipynb) | P1 | predict | `imaging` |  | Lesion patches |
| 01.02 | [VAE](01_autoencoders/02_vae.ipynb) | P1 | predict | `imaging` |  | A latent space of lesions |
| 01.03 | [β-VAE & VQ-VAE](01_autoencoders/03_β_vae_vq_vae.ipynb) | P1 | predict | `imaging` |  | Disentangle size from intensity; discretise |
| 02.01 | [GAN — The Adversarial Game](02_gans/01_gan_the_adversarial_game.ipynb) | P1 | predict | `imaging` | `goodfellow2014` | Synthetic lesion patches |
| 02.02 | [DCGAN, WGAN & Conditional GAN](02_gans/02_dcgan_wgan_conditional_gan.ipynb) | P1 | predict | `imaging` |  | 'Generate a malignant-looking patch' |
| 02.03 | [StyleGAN, CycleGAN & Pix2Pix](02_gans/03_stylegan_cyclegan_pix2pix.ipynb) | P1 | predict | `synthetic` |  | Style mixing; modality translation |
| 03.01 | [DDPM](03_diffusion/01_ddpm.ipynb) | P1 | predict | `imaging` |  | Patches by denoising |
| 03.02 | [DDIM, Latent Diffusion & Guidance](03_diffusion/02_ddim_latent_diffusion_guidance.ipynb) | P1 | predict | `imaging` |  | Faster; latent; classifier-free |
| 03.03 | [Score-Based & Flow Matching](03_diffusion/03_score_based_flow_matching.ipynb) | P1 | predict | `synthetic` | `song2021` | Score fields; rectified flows |
| 04.01 | [Normalising Flows](04_energy_flows/01_normalising_flows.ipynb) | P2 | decide | `admissions` |  | Synthetic tabular patients with exact likelihood |
| 04.02 | [Boltzmann, RBM & DBN](04_energy_flows/02_boltzmann_rbm_dbn.ipynb) | P1 | predict | `imaging` |  | Energy landscapes |
| 05.01 | [I-JEPA & V-JEPA](05_jepa/01_i_jepa_v_jepa.ipynb) | P1 | predict | `imaging` |  | Predict in embedding space |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 19_generative` checks all of it.
