# 10 — PyTorch training loop

**Phase 3 · Deep learning foundations** · ⏱ 1 week · 💻 Laptop (Apple GPU via `mps`) · Level: core

[← 09 Neural net in NumPy](09-neural-net-from-scratch.md) · [Index](../README.md) · [Next: 11 Debugging training →](11-debugging-training.md)

## The problem

You now understand what happens inside a network. Time to use the tool professionals use. You'll rebuild your MNIST network in PyTorch, then build a convolutional network (CNN) for a harder image dataset.

Datasets: **MNIST**, then **Fashion-MNIST** (clothing items, same 28×28 format, harder). Both come with `torchvision.datasets`.

## Decide first

1. Your NumPy network treated an image as a flat list of 784 numbers. What information does that throw away?
2. Why might a CNN beat a plain fully-connected network on images?
3. What steps in your NumPy code will PyTorch do for you?

## Learn

- **Tensors** are NumPy arrays that can live on a GPU and track gradients.
- **Autograd:** `loss.backward()` computes every gradient for you. You did this by hand in Challenge 09.
- **`nn.Module`:** a class with layers in `__init__` and the computation in `forward`.
- **The training loop** (memorize it):
  ```
  for each epoch:
      model.train()
      for X, y in train_loader:
          optimizer.zero_grad()
          loss = loss_fn(model(X), y)
          loss.backward()
          optimizer.step()
      model.eval(); with torch.no_grad(): evaluate on validation
  ```
- **`Dataset` / `DataLoader`** handle batching and shuffling.
- **Convolution:** a small filter slides over the image, detecting local patterns (edges, textures). Stacking conv layers + pooling builds up from edges to shapes. Far fewer weights than a fully-connected layer.
- **Device:** on your Mac, `device = "mps" if torch.backends.mps.is_available() else "cpu"`. Move the model and every batch to it.
- **Adam** is a good default optimizer; it adapts the step size per weight.

Read: PyTorch [Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html) (all short sections) and the [CNN Explainer](https://poloclub.github.io/cnn-explainer/), which is interactive.

## Build

Work in `work/10-pytorch/`. `uv add torch torchvision`. Add `torch.manual_seed(seed)` to your `set_seed` helper.

1. **Device check.** Print `torch.backends.mps.is_available()`.
   ✅ `True`.

2. **MNIST MLP.** Rebuild Challenge 09's 784 → 128 → 10 network as an `nn.Module`. Same split, same learning rate, plain SGD.
   ✅ Validation accuracy about the same as your NumPy version (~97%). If it matches, you understand both.

3. **Switch to Adam** (lr 1e-3). Compare learning curves with SGD.

4. **Fashion-MNIST MLP.** Same MLP on Fashion-MNIST (hold out 10,000 of the 60,000 training images as validation).
   ✅ Noticeably lower accuracy than on MNIST (roughly 87–89%). The task is harder.

5. **CNN.** Two conv blocks (`Conv2d → ReLU → MaxPool2d`), then a small fully-connected head. Count parameters and compare with the MLP.
   ✅ Validation accuracy around 90–92%, with fewer parameters than you might expect.

6. **Timing.** Time one epoch on `cpu` and on `mps`.
   ✅ You know how much faster the GPU is for this model. (For tiny models the difference can be small. Write down what you saw.)

7. **Save and load.** Save `model.state_dict()` to `models/`, load it in a fresh script, and re-evaluate.
   ✅ Same validation accuracy after reloading.

8. **Errors.** Confusion matrix on validation. Which clothing classes get confused? Show examples.
   ✅ You can name the most-confused pair (shirt vs T-shirt/top is typical).

9. **Test once.** Write `NOTES.md` with MLP vs CNN, accuracy and parameter count.

## Hints

<details><summary>Hint 1 — "Expected all tensors to be on the same device"</summary>

You moved the model but not the batch, or vice versa. Inside the loop: `X, y = X.to(device), y.to(device)`.
</details>

<details><summary>Hint 2 — validation accuracy jumps around or is lower than expected</summary>

Did you call `model.eval()` and use `torch.no_grad()` during validation? It doesn't matter much yet, but it will once you add dropout and batch norm in Challenge 11.
</details>

<details><summary>Hint 3 — computing the size after conv layers</summary>

Pass a dummy tensor `torch.zeros(1, 1, 28, 28)` through the conv part and print `.shape`. Or use `nn.LazyLinear`, which infers the input size.
</details>

## Common mistakes

- Forgetting `optimizer.zero_grad()`, so gradients add up across steps.
- Applying softmax before `nn.CrossEntropyLoss`. It already includes it, and expects raw scores (logits).
- Evaluating in `train()` mode.

## Done when

- [ ] PyTorch MLP matches your NumPy result on MNIST.
- [ ] An MLP vs CNN comparison on Fashion-MNIST, with parameter counts.
- [ ] CPU vs MPS timing written down.
- [ ] Save → reload → same score.
- [ ] A confusion matrix with the most-confused pair explained.

## Stretch

Write a reusable `train_one_epoch` and `evaluate` function in `work/common/`. You'll use them for the rest of the path.

## Reflect

- When would you use a CNN instead of gradient boosting? When would gradient boosting win?
- Update **Neural networks** in your [decision map](../decision-map.md).
