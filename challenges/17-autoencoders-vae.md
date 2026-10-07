# 17 — Autoencoders and VAEs

**Phase 5 · Advanced deep learning** · ⏱ 1 week · 💻 Laptop · Level: core

[← 16 Attention from scratch](16-attention-from-scratch.md) · [Index](../README.md) · [Next: 18 Tiny diffusion model →](18-diffusion-model.md)

## The problem

Two uses of the same idea:

- **Part A — Defect detection:** a factory has thousands of photos of good products and almost none of defective ones. Train a model on good items only, and flag anything it can't reconstruct well.
- **Part B — Generation:** can a model learn a "space" of images that you can sample *new* images from?

Dataset: **Fashion-MNIST** (`torchvision`). For Part A, pretend "Bag" (class 8) is the defect: train only on the other 9 classes.

## Decide first

1. A network squeezes a 784-pixel image into 2 numbers and then rebuilds it. What has it learned to keep?
2. Part A: why might an unusual item reconstruct badly?
3. Part B: if you pick a random point in a normal autoencoder's code space and decode it, why might you get garbage?

## Learn

- **Autoencoder (AE):** encoder → small **latent code** → decoder. Trained to make the output equal the input. The bottleneck forces it to learn the main structure of the data.
- **Reconstruction error as an anomaly score:** trained on normal data, the AE reconstructs normal items well and unusual ones badly. Compare this with Isolation Forest from Challenge 05.
- **Denoising autoencoder:** add noise to the input but train to output the clean image. Learns more robust features.
- **VAE (variational autoencoder):** the encoder outputs a *distribution* (mean and variance) instead of one point. Training adds a **KL term** that keeps the codes close to a standard normal distribution. Result: you can sample from N(0, 1), decode, and get plausible new images.
- **Reparameterization trick:** `z = μ + σ · ε` with ε ~ N(0, 1), so gradients can flow through the sampling step.
- **Trade-off:** the KL term makes reconstructions blurrier but the latent space smoother.

Read: Lilian Weng, [From Autoencoder to Beta-VAE](https://lilianweng.github.io/posts/2018-08-12-vae/) (sections on autoencoders, denoising AE and VAE). Skim the maths, focus on the pictures.

## Build

Work in `work/17-autoencoders/`.

### Part A — Autoencoder for anomaly detection

1. **Data.** Training set: Fashion-MNIST training images *excluding* class 8. Validation and test: normal images plus bags (keep the real ratio, about 10% bags).
   ✅ No bags in training. Bags present in validation and test.

2. **Autoencoder.** A small conv or MLP autoencoder with a 16-dimensional latent code. MSE loss.
   ✅ Reconstructions of normal validation images look recognizable.

3. **Anomaly score.** Per-image reconstruction error on validation. Plot the error histogram for normal vs bag.
   ✅ Bags have higher error on average, with some overlap.

4. **Evaluate.** ROC-AUC and average precision of the error as a "bag" detector. Pick a threshold on validation for 90% recall of bags; report precision.

5. **Compare.** Isolation Forest on raw pixels (or on PCA features) with the same split.
   ✅ A table: AE vs Isolation Forest. Write which is better and a guess why.

### Part B — VAE

6. **VAE** with a **2-dimensional** latent space on all of Fashion-MNIST. Loss = reconstruction + KL.
   ✅ Both terms are logged separately and both go down (KL may rise first, then settle).

7. **Latent map.** Encode the validation set and plot the 2D means coloured by class.
   ✅ Classes form regions; similar items (shirts, pullovers, coats) are neighbours.

8. **Generate.** Decode a 15×15 grid of points across the latent space.
   ✅ A grid of images that morph smoothly from one item type to another.

9. **Compare with a plain AE.** Decode random N(0, 1) points with your Part A-style autoencoder (2D latent). Compare quality with the VAE.

10. `NOTES.md`: anomaly table, latent plot, generated grid, and your explanation of what the KL term does.

## Hints

<details><summary>Hint 1 — the VAE loss</summary>

`recon = F.binary_cross_entropy(x_hat, x, reduction="sum")` (with a sigmoid output) and `kl = -0.5 * torch.sum(1 + logvar - mu**2 - logvar.exp())`. Divide both by the batch size. If samples are all the same blurry blob, the KL term is winning: try a smaller weight on it (β < 1) for a while.
</details>

## Common mistakes

- Training the anomaly autoencoder on data that includes the anomaly class.
- Choosing the anomaly threshold on the test set.
- Expecting a plain autoencoder to generate good samples from random codes.

## Done when

- [ ] Autoencoder anomaly detector with ROC-AUC, AP and a validation-chosen threshold.
- [ ] Comparison with Isolation Forest.
- [ ] VAE latent map and a generated grid.
- [ ] Plain AE vs VAE sampling comparison.
- [ ] `NOTES.md` explains when you'd use an AE, and when a VAE.

## Stretch

Train a small **GAN** (generator vs discriminator) on Fashion-MNIST and compare sample quality and training stability with your VAE.

## Reflect

- Add autoencoders to the **No labels** section *and* the **Sequence and generative models** section of your [decision map](../decision-map.md).
