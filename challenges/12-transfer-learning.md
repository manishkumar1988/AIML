# 12 — Transfer learning

**Phase 4 · Computer vision** · ⏱ 1 week · 💻 Laptop · Level: core

[← 11 Debugging training](11-debugging-training.md) · [Index](../README.md) · [Next: 13 Object detection →](13-object-detection.md)

## The problem

A pet-insurance app wants to identify a pet's breed from a photo. There are 37 breeds and only about 100 training photos per breed. Training a CNN from scratch on that little data won't go far. Instead, you'll start from a network that has already learned to see, from millions of images.

Dataset: **Oxford-IIIT Pet** (`torchvision.datasets.OxfordIIITPet`): 37 cat and dog breeds, about 7,400 photos. Official split: `trainval` (3,680) and `test` (3,669). Carve 20% of `trainval` off as validation.

## Decide first

1. With ~100 photos per class, what do you expect from a CNN trained from scratch?
2. A model pretrained on ImageNet has never seen the "Abyssinian cat" label. Why would it still help?
3. Two options: freeze the pretrained network and train only a new final layer, or fine-tune everything. Which is faster? Which is likely more accurate? When would you pick each?

## Learn

- **Transfer learning:** reuse a **backbone** pretrained on a big dataset (ImageNet, 1.2M images). Its early layers detect edges and textures; later layers detect parts. Those features are useful for almost any image task.
- **Feature extraction / linear probe:** freeze the backbone, replace and train only the final layer. Fast, works with very little data.
- **Fine-tuning:** unfreeze some or all layers and train with a *small* learning rate, often smaller for the backbone than for the new head. Usually more accurate, slower, and easier to overfit.
- **Use the pretrained model's preprocessing:** same input size and normalization the backbone was trained with.
- **[`timm`](https://huggingface.co/docs/timm/index)** has hundreds of pretrained vision models with a one-line API.

Read: PyTorch [Transfer Learning for Computer Vision tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html).

## Build

Work in `work/12-transfer/`. `uv add timm`.

1. **Data.** Load `trainval` and `test` with `target_types="category"`. Make a stratified 80/20 split of `trainval` into train/validation. Resize to 224×224 and use ImageNet normalization. Augment training data only.
   ✅ About 2,944 train / 736 validation images, 37 classes in each.

2. **Baseline.** Majority class accuracy on validation.
   ✅ About 3% (1 in 37).

3. **From scratch.** Your Challenge 11 CNN (adapted to 224×224 or resized to 64×64), trained from random weights for ~20 epochs.
   ✅ Low accuracy (roughly 15–35%). This is the number transfer learning has to beat.

4. **Linear probe.** `timm.create_model("resnet18", pretrained=True, num_classes=37)`. Freeze everything except the final classifier. Train 5–10 epochs.
   ✅ Big jump, roughly 80–88% validation accuracy, in a few minutes.

5. **Fine-tune.** Unfreeze the whole network. Use AdamW with a lower learning rate for the backbone (e.g. 1e-4) than the head (e.g. 1e-3). Train with early stopping.
   ✅ A few points better than the linear probe (roughly 88–92%).

6. **A stronger backbone.** Try one more model, e.g. `efficientnet_b0` or `convnext_tiny`. Record accuracy, parameter count, and time per epoch.

7. **Errors.** Per-class accuracy. Show the 5 worst breeds and their most common confusions.
   ✅ Confusions are mostly between similar-looking breeds, or cats vs cats and dogs vs dogs, rarely a cat vs a dog. Check that.

8. **Test once** with your best model. Write `NOTES.md` with a table: scratch vs probe vs fine-tune vs stronger backbone (accuracy, training time, parameters).

## Hints

<details><summary>Hint 1 — freezing layers</summary>

`for p in model.parameters(): p.requires_grad = False`, then unfreeze the head: `for p in model.get_classifier().parameters(): p.requires_grad = True`. Only pass parameters with `requires_grad=True` to the optimizer.
</details>

<details><summary>Hint 2 — using two learning rates</summary>

Pass parameter groups to the optimizer: `AdamW([{"params": backbone_params, "lr": 1e-4}, {"params": head_params, "lr": 1e-3}])`.
</details>

<details><summary>Hint 3 — getting the model's expected preprocessing</summary>

`timm.data.resolve_data_config({}, model=model)` and `timm.data.create_transform(**config)` give you the right resize and normalization.
</details>

## Common mistakes

- Using a high learning rate when fine-tuning, which destroys the pretrained features in the first epoch.
- Different preprocessing from what the backbone expects.
- Comparing models trained for very different numbers of epochs without saying so.

## Done when

- [ ] Four rows in your table: baseline, scratch, linear probe, fine-tune (+ the stronger backbone).
- [ ] Training time and parameter count recorded for each.
- [ ] The worst-breed analysis with example images.
- [ ] One test score.
- [ ] `NOTES.md` answers: when would you use a linear probe instead of full fine-tuning?

## Stretch

Train the linear probe with only 10 images per class. How much accuracy remains? This is how you'd judge "how much data do we need to label?"

## Reflect

- Fill in "train from scratch vs transfer learning" in the **Computer vision** section of your [decision map](../decision-map.md).
