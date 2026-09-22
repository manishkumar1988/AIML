# Challenge 10 — Transfer learning with a pre-registered win

[Previous: Challenge 9 — Image classification with noisy training labels](09-image-classification-noisy-training-labels.md) · [Next: Challenge 11 — Object detection on Pascal VOC 2007](11-object-detection-pascal-voc-2007.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 10 — Transfer learning with a pre-registered win

- **Goal:** Beat the Challenge 9 model on the same split by a margin you wrote down first, and show one transfer setup that does not help.
- **Why an engineer needs it:** “Use a pretrained backbone” is not a result. Frozen versus fine-tuned, and the learning rate, change the outcome. You need a before/after on a fixed test.
- **What to build:** On the same Food-101 splits, fine-tune a small pretrained backbone (MobileNetV3 or ResNet-18). Compare at least: a linear probe on a frozen backbone, and a fine-tune with a lower learning rate on the backbone than on the head. The margin over Challenge 9’s top-1 must be declared before this run (for example +5 points). Recompute the same 10 worst classes. Keep one augmentation or learning-rate setting that does not improve dev macro-F1, and leave it in the log.
- **Skills practiced:** Transfer learning, differential learning rates, honest comparisons.
- **Stack and data:** PyTorch, torchvision weights. Same [ethz/food101](https://huggingface.co/datasets/ethz/food101) splits as Challenge 9.
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** small GPU. Colab-or-Kaggle fallback.
- **Acceptance criteria:**
  - The log shows Challenge 9’s top-1, the frozen probe, and the fine-tune, same validation split.
  - The pre-registered margin is in the log before the fine-tune result, and you say whether you hit it.
  - The worst-class list is updated. At least one class that stayed bad is discussed.
  - One negative result (a change that did not help) is recorded.
- **Stretch goal:** A learning curve of dev macro-F1 versus hours or steps for frozen versus fine-tune, so the cost of the gain is visible.
- **Builds on:** Challenge 9.
