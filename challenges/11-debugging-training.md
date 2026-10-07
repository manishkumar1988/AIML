# 11 — Debugging and improving training

**Phase 3 · Deep learning foundations** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 10 PyTorch training loop](10-pytorch-training-loop.md) · [Index](../README.md) · [Next: 12 Transfer learning →](12-transfer-learning.md)

## The problem

Real training rarely "just works." Loss goes to `nan`, validation accuracy stalls, the model memorizes the training set. This challenge is a set of controlled experiments that teach you to *read* training curves and know which fix to try.

Dataset: **CIFAR-10** (`torchvision.datasets.CIFAR10`): 60,000 small 32×32 colour images, 10 classes (plane, car, bird, cat…). Hold out 5,000 of the 50,000 training images as validation.

## Decide first

1. Training accuracy is 99%, validation 60%. What's happening, and what would you try?
2. Training and validation accuracy are both 40% and flat. What's happening?
3. The loss becomes `nan` after a few steps. What's the most likely cause?

## Learn

- **Read the curves.** Always plot training *and* validation loss per epoch.
  - Both high and flat → **underfitting** (model too small, learning rate wrong, bug).
  - Train falls, validation rises → **overfitting** (memorizing).
  - Spiky or `nan` → **learning rate too high**, or bad input scaling.
- **The debugging ladder:** (1) overfit a single batch; (2) check the initial loss (≈ ln(classes)); (3) find a good learning rate; (4) then improve generalization.
- **Normalization:** scale inputs using the mean/std of the *training* set. **Batch normalization** layers stabilize training inside the network.
- **Regularization:** **data augmentation** (random crops, flips), **dropout**, **weight decay** (AdamW), **early stopping** (keep the epoch with the best validation score).
- **Learning-rate schedules:** start higher, decrease over time (cosine or step decay). Often a free improvement.

Read: Andrej Karpathy, [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/). Read the whole thing; it's the core of this challenge.

## Build

Work in `work/11-debugging/`. Use the `train_one_epoch` / `evaluate` helpers from Challenge 10. Keep a results table: experiment, best validation accuracy, epoch, notes.

1. **Data + normalization.** Compute the per-channel mean and std on the 45,000 training images only. Plot 16 images with labels.
   ✅ Means are roughly (0.49, 0.48, 0.45). Your images display correctly.

2. **Sanity checks** with a small CNN (3 conv blocks): initial loss ≈ 2.3; then overfit 1 batch of 32 to ~100%.
   ✅ Both pass.

3. **Break it on purpose (learn the symptoms):**
   - (a) Learning rate 1.0 with SGD. Record what the loss does.
   - (b) Forget to normalize inputs (use 0–255 raw pixels). Record the effect.
   - (c) Shuffle the labels randomly and train. What does training accuracy do? Validation?
   ✅ For each, one line: symptom → cause. Keep these lines. They are your debugging cheat sheet.

4. **Baseline run.** No augmentation, no regularization, Adam lr 1e-3, 30 epochs.
   ✅ Clear overfitting: training accuracy far above validation (validation around 70%).

5. **Fix overfitting, one change at a time.** Add, separately: (a) augmentation (`RandomCrop(32, padding=4)` + `RandomHorizontalFlip`); (b) dropout; (c) weight decay with AdamW; (d) batch norm. Then combine the ones that helped.
   ✅ Combined, validation accuracy around 80–85%, and the train/validation gap is much smaller.

6. **Learning-rate schedule.** Add `CosineAnnealingLR` or `OneCycleLR` to your best setup.

7. **Early stopping.** Save the checkpoint with the best validation accuracy, not the last one.

8. **Errors.** Per-class accuracy and a confusion matrix. Which classes are hardest?
   ✅ Cat vs dog is usually the worst pair. Show examples.

9. **Test once** with the best checkpoint. Write `NOTES.md` with your results table and debugging cheat sheet.

## Hints

<details><summary>Hint 1 — augmentation on validation data</summary>

Use two transform pipelines: augmentation + normalization for training; normalization only for validation and test. Augmenting validation data makes your scores noisy and wrong.
</details>

<details><summary>Hint 2 — training is slow</summary>

Set `num_workers=2` or `4` in the `DataLoader` and use `mps`. Run 2–3 epochs to test a change before running 30. Use a smaller model while you're debugging.
</details>

## Common mistakes

- Changing three things at once, so you don't know which one helped.
- Computing normalization statistics on train+test.
- Reporting the final epoch instead of the best validation checkpoint, or picking the epoch using test accuracy.

## Done when

- [ ] A debugging cheat sheet: symptom → cause, from your deliberate breakages.
- [ ] A results table with at least 6 experiments, one change each.
- [ ] Validation accuracy of about 80% or more, with a smaller train/validation gap than the baseline.
- [ ] Training/validation curves plotted for the baseline and the best run.
- [ ] One test score from the best checkpoint.

## Stretch

Add [TensorBoard](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html) or [Weights & Biases](https://wandb.ai/) logging. Compare runs visually.

## Reflect

- Write your own 5-step "my training doesn't work" checklist in the **Neural networks** section of your [decision map](../decision-map.md).
