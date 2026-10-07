# 18 — A tiny diffusion model

**Phase 5 · Advanced deep learning** · ⏱ 1–2 weeks · 💻 Laptop (or Colab for faster training) · Level: stretch

[← 17 Autoencoders and VAEs](17-autoencoders-vae.md) · [Index](../README.md) · [Next: 19 Hugging Face tour →](19-hugging-face-tour.md)

## The problem

Image generators like Stable Diffusion are built on a simple idea: add noise to images step by step until they're pure static, then train a network to undo one step at a time. You'll build a small one that generates handwritten digits, and you'll see why it produces sharper images than your VAE.

Dataset: **MNIST** (28×28; pad to 32×32 to make the U-Net simpler).

## Decide first

1. Your VAE produced blurry images. Why might "remove a little noise, many times" work better than "decode in one shot"?
2. Generating one image takes hundreds of network calls. What's the cost of that, compared with a VAE?
3. How would you judge whether generated digits are "good" without a human looking at each one?

## Learn

- **Forward process (fixed, no learning):** take an image x₀ and add Gaussian noise over T steps (e.g. T = 300–1000) using a schedule βₜ. There's a closed form to jump straight to any step: `xₜ = √ᾱₜ · x₀ + √(1 − ᾱₜ) · ε`.
- **Training:** pick a random image and a random step t, add noise ε, and train a network to **predict the noise**: loss = MSE(ε, ε̂(xₜ, t)). That's the whole training loop.
- **Sampling (reverse process):** start from pure noise x_T and repeatedly subtract the predicted noise (plus a bit of fresh noise) from t = T down to 1.
- **The network:** a small U-Net (you built one in Challenge 14) that also receives the timestep t, as a sinusoidal embedding added to its features.
- **Evaluation:** look at samples, but also use a classifier: run your Challenge 10 MNIST CNN on 1,000 generated digits. Confident, varied predictions across all 10 digits mean good, diverse samples.

Read: the Hugging Face blog post [The Annotated Diffusion Model](https://huggingface.co/blog/annotated-diffusion) and Lilian Weng's [What are Diffusion Models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) (first two sections).

## Build

Work in `work/18-diffusion/`.

1. **Noise schedule.** Linear β from 1e-4 to 0.02 with T = 300. Compute αₜ and ᾱₜ. Write `q_sample(x0, t, noise)`.
   ✅ Plot one digit at t = 0, 50, 100, 200, 299. It turns gradually into static.

2. **Time-conditioned U-Net.** Adapt your Challenge 14 U-Net: 1 input channel, 1 output channel, plus a timestep embedding added in each block.
   ✅ A forward pass with input `(B, 1, 32, 32)` and `t` of shape `(B,)` returns `(B, 1, 32, 32)`.

3. **Training loop.** Random t per image, MSE between true and predicted noise. Train on `mps`, ~20–40 epochs (Colab if too slow).
   ✅ Loss decreases steadily. Save checkpoints.

4. **Sampling.** Implement the reverse loop. Generate 64 digits and show them in a grid.
   ✅ Most samples look like real digits. Early checkpoints give blobs; later ones give sharp digits. Save a grid per checkpoint.

5. **Evaluate with a classifier.** Classify 1,000 generated samples with your Challenge 10 CNN. Report: average max-probability (confidence) and the histogram of predicted digits.
   ✅ High average confidence, and all 10 digits appear in roughly similar numbers. A lopsided histogram means the model collapsed to a few digits.

6. **Compare with the VAE.** Same evaluation for 1,000 VAE samples (retrain your Challenge 17 VAE on MNIST if needed). Also time how long each takes to generate 1,000 images.
   ✅ Diffusion is sharper and more confidently classified, and much slower to sample.

7. **Fewer steps.** Sample by skipping steps (e.g. use only every 10th) and see how quality drops.

8. `NOTES.md`: sample grids over training, the classifier evaluation, the VAE comparison, and the speed trade-off.

## Hints

<details><summary>Hint 1 — samples are pure noise or saturated</summary>

Check that images are scaled to [−1, 1] (not [0, 1]) for training, and that the sampling formula uses the same α/β arrays and indexing as training. Off-by-one errors in t are the most common bug. Clip the final output to [−1, 1].
</details>

<details><summary>Hint 2 — training is too slow</summary>

Use a smaller U-Net (channels 32/64/128), T = 300, batch size 128. Or train on Colab and copy the checkpoint back.
</details>

## Common mistakes

- Mismatched t indexing between training and sampling.
- Judging the model from 8 hand-picked samples.
- Forgetting to put the model in `eval()` mode and `no_grad()` for sampling.

## Done when

- [ ] Forward-noising visualization.
- [ ] A trained model that generates recognizable digits.
- [ ] Classifier-based evaluation of 1,000 samples, for both diffusion and VAE.
- [ ] Sampling speed comparison.
- [ ] You can explain diffusion in three sentences.

## Stretch

Make it **class-conditional**: pass the digit label as an extra embedding, so you can ask for a "7." Then add classifier-free guidance.

## Reflect

- Complete the **Sequence and generative models** section of your [decision map](../decision-map.md): AE vs VAE vs GAN vs diffusion.
- **Milestone:** redo [Challenge 01](01-problem-framing.md) from memory and compare with your first attempt.
