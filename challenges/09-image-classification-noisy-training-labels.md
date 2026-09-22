# Challenge 9 — Image classification with noisy training labels

[Previous: Challenge 8 — Named entity recognition at span level](08-named-entity-recognition-at-span-level.md) · [Next: Challenge 10 — Transfer learning with a pre-registered win](10-transfer-learning-pre-registered-win.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 9 — Image classification with noisy training labels

- **Goal:** Train a small CNN from scratch on Food-101 and report the classes it cannot tell apart.
- **Why an engineer needs it:** Real image data is noisy and fine-grained. Food-101 leaves the training images dirty on purpose and cleans the evaluation images. That is a normal data condition, not a bug you “fix” by peeking.
- **What to build:** A small convolutional network, trained from random initialization, on [ethz/food101](https://huggingface.co/datasets/ethz/food101) (101 classes, 75,750 train / 25,250 validation images, max side 512). Use the Hub splits as published. Carve a dev subset from train for early stopping and augmentation choices. Headline: top-1 accuracy and macro-F1 on the official validation split, plus the 10 worst classes. A linear probe on frozen random features is not required; a majority-class baseline is. Save the worst-class list for Challenge 10.
- **Skills practiced:** Image splits, augmentation timing, per-class errors, training loops.
- **Stack and data:** PyTorch. Hugging Face dataset [ethz/food101](https://huggingface.co/datasets/ethz/food101).
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** small GPU. Colab-or-Kaggle fallback for the scored run. A two-class CPU debug run does not count.
- **Acceptance criteria:**
  - The log has majority baseline, top-1, and macro-F1 on the official validation split.
  - The 10 worst classes are listed with support and recall.
  - Dev choices (early stopping, augmentation) were not retuned after seeing the validation number you publish.
  - Training images were not “cleaned” using the validation labels.
- **Stretch goal:** A short note on which worst-class errors look like label noise versus genuine visual confusion, with five images you opened.
- **Builds on:** Challenges 1–3 for the log, the split discipline, and the error-slice habit.
