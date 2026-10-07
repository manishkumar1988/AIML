# 14 — Image segmentation

**Phase 4 · Computer vision** · ⏱ 1 week · 💻 Laptop · Level: core

[← 13 Object detection](13-object-detection.md) · [Index](../README.md) · [Next: 15 Sequence models →](15-sequence-models.md)

## The problem

A photo app wants to cut pets out of photos (remove the background) automatically. A box isn't enough. They need to know, **for every pixel**, whether it belongs to the pet.

Dataset: **Oxford-IIIT Pet** again, this time with `target_types="segmentation"`. Each image comes with a "trimap": 1 = pet, 2 = background, 3 = border region. Convert it into a binary mask: pet vs not-pet (treat the border as pet, or ignore it in the loss — write down your choice).

## Decide first

1. What's the output shape for one 128×128 image?
2. What's a dumb baseline for "which pixels are the pet"?
3. Why might pixel accuracy be misleading? (Think of a small pet in a big photo.)

## Learn

- **Semantic segmentation:** classify every pixel. Output is a mask the same size as the image.
- **Encoder–decoder:** the encoder shrinks the image into features (like a classifier); the decoder grows it back to full size.
- **U-Net** adds **skip connections** from encoder to decoder, so fine detail (edges) isn't lost. It's the standard starting point.
- **Losses:** pixel-wise binary cross-entropy, often combined with **Dice loss**, which cares about overlap and handles small objects better.
- **Metrics:** **IoU** (intersection over union of the predicted and true masks) and **Dice**. Avoid pixel accuracy as the headline.
- **Pretrained encoders** help here just as in Challenge 12. The [`segmentation_models_pytorch`](https://smp.readthedocs.io/) library builds a U-Net around a pretrained backbone in one line.
- **Augmentation:** if you flip the image, you must flip the mask the same way.

Read: the original [U-Net paper](https://arxiv.org/abs/1505.04597) — figure 1 and section 2 only, it's short.

## Build

Work in `work/14-segmentation/`. Resize images and masks to 128×128 to keep it fast. Use the same train/validation split approach as Challenge 12 (from `trainval`), and the official `test` split.

1. **Data.** Load images and trimaps. Convert to binary masks. Plot 6 images with masks overlaid.
   ✅ Masks line up with the pets. Write the fraction of pixels that are "pet" on average.

2. **Mask resizing.** Make sure masks are resized with **nearest-neighbour** interpolation, not bilinear.
   ✅ Mask values are only 0 and 1 after resizing (`torch.unique(mask)`).

3. **Baselines.** (a) Predict "all background." (b) Predict a centered ellipse covering the middle of the image (pets are often centered). Compute pixel accuracy and IoU for both.
   ✅ Baseline (a) has decent pixel accuracy but IoU = 0. That's why IoU is the headline.

4. **IoU and Dice functions.** Write them yourself and test on tiny hand-made masks.

5. **U-Net from scratch.** A small U-Net (3 down blocks, 3 up blocks, skip connections). BCE + Dice loss. Train ~20 epochs on `mps`.
   ✅ Validation IoU clearly above the ellipse baseline (roughly 0.7–0.8).

6. **Pretrained encoder.** `uv add segmentation-models-pytorch`. `smp.Unet(encoder_name="resnet18", encoder_weights="imagenet", classes=1)`. Same training.
   ✅ Higher IoU (roughly 0.8–0.85+), and it converges faster.

7. **Errors.** Show the 6 validation images with the lowest IoU: image, true mask, predicted mask. What goes wrong? (Fur edges, dark pets on dark backgrounds, multiple pets…)

8. **Test once.** Write `NOTES.md` with baselines vs scratch U-Net vs pretrained U-Net (IoU, Dice, training time).

## Hints

<details><summary>Hint 1 — applying the same augmentation to image and mask</summary>

Use `torchvision.transforms.v2`, which can transform an image and a mask together (wrap the mask with `tv_tensors.Mask`). Or flip both manually with the same random decision.
</details>

<details><summary>Hint 2 — U-Net output size doesn't match</summary>

Use input sizes divisible by 2^(number of down blocks), e.g. 128. Print shapes after every block.
</details>

## Common mistakes

- Bilinear resizing of masks (creates fake in-between labels).
- Flipping the image but not the mask.
- Reporting pixel accuracy as the headline.

## Done when

- [ ] Two baselines with pixel accuracy and IoU, and a sentence on why they differ.
- [ ] Your own IoU/Dice functions, tested.
- [ ] Scratch U-Net vs pretrained-encoder U-Net comparison.
- [ ] A gallery of the worst predictions, with your diagnosis.
- [ ] One test score.

## Stretch

Try [Segment Anything (SAM)](https://huggingface.co/docs/transformers/model_doc/sam) with a single click point on the pet, with no training. How close does it get to your trained model? When would you use each?

## Reflect

- Complete the **Computer vision** section of your [decision map](../decision-map.md): classification vs detection vs segmentation, and the metric for each.
