# 09 — A neural network in NumPy

**Phase 3 · Deep learning foundations** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 08 Kaggle playground](08-kaggle-playground.md) · [Index](../README.md) · [Next: 10 PyTorch training loop →](10-pytorch-training-loop.md)

## The problem

Every deep learning library hides the same few ideas: a forward pass, a loss, gradients by the chain rule, and an update step. If you understand them once, without a framework, PyTorch stops being magic and debugging becomes much easier.

You'll build a small neural network in pure NumPy and train it to recognise handwritten digits.

Dataset: **MNIST**, 70,000 grayscale 28×28 digit images. Load it with `sklearn.datasets.fetch_openml("mnist_784", as_frame=False)`. Use the first 60,000 for train/validation and the last 10,000 as test.

## Decide first

1. A 28×28 image has 784 pixels. What's the input to your network, and what's the output?
2. What should the output layer produce for 10 classes, and which loss fits it?
3. What do you expect a logistic regression to score on MNIST? Will a 2-layer network do better?
4. If your loss doesn't go down at all, list three things that might be wrong.

## Learn

- **Forward pass:** `z1 = X @ W1 + b1`, `a1 = relu(z1)`, `z2 = a1 @ W2 + b2`, `p = softmax(z2)`.
- **Loss:** cross-entropy, `-mean(log p[correct class])`.
- **Backward pass (backpropagation):** apply the chain rule from the loss back to each weight. For softmax + cross-entropy, the gradient at `z2` is neat: `(p - y_onehot) / batch_size`.
- **Gradient descent:** `W -= learning_rate * dW`. Mini-batches (e.g. 64 examples) make each step cheap and a bit noisy, which helps.
- **Initialization:** small random weights (He initialization: `randn * sqrt(2 / fan_in)` for ReLU). All zeros means every neuron learns the same thing.
- **Gradient check:** compare your analytic gradient with a numerical one `(L(w+ε) − L(w−ε)) / 2ε` on a tiny network. If they match, your backprop is right.

Watch: 3Blue1Brown, [Neural Networks](https://www.3blue1brown.com/topics/neural-networks), chapters 1–4. Then Andrej Karpathy, [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html), lecture 1 ("micrograd"). Both are excellent.

## Build

Work in `work/09-numpy-net/`. No PyTorch, no scikit-learn models. NumPy only (scikit-learn is fine for loading data and computing accuracy).

1. **Data.** Load, scale pixels to 0–1, split 50,000 train / 10,000 validation / 10,000 test. One-hot encode the labels.
   ✅ `X_train.shape == (50000, 784)`, `y_onehot.shape == (50000, 10)`.

2. **Baseline.** Logistic regression in scikit-learn on the same split, for comparison.
   ✅ Validation accuracy around 92%.

3. **Forward pass and loss.** Write `forward(X, params)` and `cross_entropy(p, y)`. With random weights, compute the loss on one batch.
   ✅ The initial loss is about `ln(10) ≈ 2.3`. (Why? Write the reason.)

4. **Backward pass.** Write `backward(...)` returning `dW1, db1, dW2, db2`.

5. **Gradient check.** On a tiny network (e.g. 5 inputs, 3 hidden, 2 classes, 4 examples), compare analytic and numerical gradients.
   ✅ Relative difference below about 1e-6. **Don't move on until this passes.**

6. **Overfit one batch.** Train on 64 examples only, for a few hundred steps.
   ✅ Loss goes close to 0 and accuracy on those 64 is 100%. If not, you have a bug.

7. **Train for real.** 784 → 128 → 10, mini-batch 64, learning rate ~0.1, 10 epochs. Each epoch, record training loss and validation accuracy.
   ✅ Validation accuracy around 97%, clearly above logistic regression.

8. **Learning-rate experiment.** Try 0.001, 0.01, 0.1, 1.0. Plot validation accuracy per epoch for each.
   ✅ You can describe what "too small" and "too large" look like.

9. **Errors.** Show 16 misclassified validation images with true and predicted labels. Are they hard for a human too?

10. **Test once.** Report test accuracy. Write `NOTES.md`.

## Understanding check

AI can write this network for you. This challenge is about what you understand, so do these without AI help:

- [ ] **Predict before running:** before step 3, write down the initial loss you expect, and why.
- [ ] **Break it on purpose:** (a) remove the ReLU, (b) initialize all weights to zero, (c) forget to divide the gradient by batch size. Predict what each does, then run it. Write prediction vs result.
- [ ] **Shapes on paper:** write the shape of every array in the forward and backward pass for a batch of 64.
- [ ] **Explain it:** walk through backprop for your 2-layer network on paper or a whiteboard, from the loss to `dW1`.

## Hints

<details><summary>Hint 1 — stable softmax</summary>

Subtract the row max before exponentiating: `e = np.exp(z - z.max(axis=1, keepdims=True))`. Otherwise large values overflow to `inf`, and the loss becomes `nan`.
</details>

<details><summary>Hint 2 — ReLU gradient</summary>

`da/dz = (z > 0)`. So `dz1 = (dZ2 @ W2.T) * (z1 > 0)`. Keep `z1` from the forward pass, because you need it here.
</details>

<details><summary>Hint 3 — shapes</summary>

`dW2 = a1.T @ dz2` has the same shape as `W2`. `db2 = dz2.sum(axis=0)`. Every gradient has the same shape as the thing it updates. Print shapes when stuck.
</details>

## Common mistakes

- Skipping the gradient check and debugging a wrong gradient for days.
- Forgetting to divide by batch size, so the effective learning rate changes with batch size.
- Not shuffling training data each epoch.

## Done when

- [ ] Every item in the Understanding check is done, without AI help.
- [ ] Gradient check passes.
- [ ] One batch can be overfitted to 100%.
- [ ] About 97% validation accuracy, beating logistic regression.
- [ ] A learning-rate plot and your explanation of it.
- [ ] You can explain backprop for your network on a whiteboard, without notes.

## Stretch

Add a second hidden layer, or momentum (`v = 0.9*v + dW; W -= lr*v`). Does either help?

## Reflect

- Which part of training does PyTorch's `loss.backward()` replace? Which parts does it *not* replace?
- Start the **Neural networks** section of your [decision map](../decision-map.md).
