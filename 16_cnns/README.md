# Module 16 — Convolutional Neural Networks

**Tier** 2 · **Notebooks** 8 · **Prerequisites** 15

> Medical imaging from first principles.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Convolution, Pooling & Feature Maps](01_fundamentals/01_convolution_pooling_feature_maps.ipynb) | P1 | predict | `imaging` |  | Edge detection on lesion patches |
| 01.02 | [Building a First CNN](01_fundamentals/02_building_a_first_cnn.ipynb) | P1 | predict | `imaging` | `rajpurkar2017` | CheXNet in miniature — lesion present/absent end to end, with the class-activation map the paper is known for |
| 02.01 | [LeNet, AlexNet & VGG](02_classic/01_lenet_alexnet_vgg.ipynb) | P1 | predict | `imaging` | `esteva2017` | Esteva-style: transfer learning vs from-scratch at 100 / 1k / 10k patches |
| 02.02 | [Inception & ResNet](02_classic/02_inception_resnet.ipynb) | P1 | predict | `imaging` | `he2016` | Multi-scale lesions; deep training |
| 02.03 | [DenseNet, MobileNet & EfficientNet](02_classic/03_densenet_mobilenet_efficientnet.ipynb) | P5 | decide | `imaging` | `tan2020` | Reuse; a model that runs on a ruggedised handheld; compound scaling |
| 03.01 | [U-Net Segmentation](03_tasks/01_u_net_segmentation.ipynb) | P1 | predict | `imaging` | `U-Net (Ronneberger 2015) on biomedical segmentation` | Lesion boundary pixel labelling |
| 03.02 | [Object Detection — YOLO, R-CNN family, FPN](03_tasks/02_object_detection_yolo_r_cnn_family_fpn.ipynb) | P1 | predict | `synthetic` | `redmon2018` | Boxes around multiple lesions |
| 03.03 | [ConvNeXt](03_tasks/03_convnext.ipynb) | P1 | predict | `imaging` |  | Transformer tricks in a CNN |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 16_cnns` gates the module.
