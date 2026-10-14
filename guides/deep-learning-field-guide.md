# Deep learning field guide

Which architecture to use, sensible starting settings, how to read training curves, and what to do when training doesn't work.

**First question:** do you need deep learning at all? For **tables**, gradient boosting usually wins with far less effort. Deep learning earns its place on **images, text, audio, sequences**, very large data, and anywhere a **pretrained model** exists.

---

## 1. Which architecture?

| Architecture | Built for | Key idea | Today |
| --- | --- | --- | --- |
| **MLP** (fully connected) | Fixed-size vectors (tabular features, embeddings) | Layers of weighted sums + nonlinearity | Heads on top of other models; simple tabular nets |
| **CNN** | Images, also audio spectrograms | Small filters slide over the input; detects local patterns, builds up to shapes | Still strong for vision, especially small/medium data and edge devices |
| **RNN / LSTM / GRU** | Sequences read in order | A hidden state carries memory step by step | Mostly replaced by transformers; still used in some small/streaming tasks |
| **Transformer** | Text, and now images (ViT), audio, everything | **Attention**: every token looks at every other token | The default for text and LLMs; very common in vision |
| **Autoencoder / VAE** | Compression, anomaly detection, generation | Encode to a small code, decode back | Anomaly detection; VAEs are parts of image generators |
| **GAN** | Image generation | Generator vs discriminator game | Largely replaced by diffusion |
| **Diffusion** | Image/audio/video generation | Learn to remove noise step by step | The default for image generation |
| **U-Net** | Segmentation; also inside diffusion models | Encoder–decoder with skip connections | The default segmentation starting point |

### Pretrained first

| Task | Start from |
| --- | --- |
| Image classification | A pretrained CNN/ViT from `timm` (ResNet, EfficientNet, ConvNeXt, ViT) |
| Object detection | A pretrained detector (YOLO, DETR-family) |
| Segmentation | U-Net with a pretrained encoder; SAM for prompt-based masks |
| Text classification / NER | A pretrained encoder (DistilBERT, BERT, RoBERTa, DeBERTa) |
| Text generation, chat | A pretrained decoder LLM (Qwen, Llama, Mistral, Gemma…) |
| Sentence similarity / search | A sentence-embedding model (MiniLM, BGE, E5…) |
| Speech-to-text | Whisper-family models |

Training from scratch makes sense only with a lot of data, or when learning how things work (as in Challenges 09, 23, 24).

---

## 2. Sensible starting settings

These aren't optimal. They're places to start that usually work.

| Setting | Starting point | Notes |
| --- | --- | --- |
| **Optimizer** | **AdamW** | SGD + momentum can do better for CNNs from scratch, with more tuning |
| **Learning rate (from scratch)** | 1e-3 (Adam/AdamW) | The single most important setting |
| **Learning rate (fine-tuning pretrained)** | 1e-5 to 5e-5 (transformers); 1e-4 (CNN backbones) | Too high destroys pretrained knowledge |
| **Learning rate (LoRA)** | 1e-4 to 2e-4 | |
| **Schedule** | Warmup (a few % of steps) + cosine decay | Usually a free improvement |
| **Batch size** | 32–128 (images/tabular); as large as memory allows for LLMs | If you change it a lot, re-tune the learning rate |
| **Weight decay** | 0.01–0.1 (AdamW) | Mild regularization |
| **Epochs** | Until validation stops improving | Use early stopping; keep the best checkpoint |
| **Gradient clipping** | max norm 1.0 | Essential for RNNs and transformers |
| **Initialization** | Library defaults | PyTorch defaults are fine for standard layers |

---

## 3. Reading training curves

Always plot **training loss and validation loss** (and validation metric) per epoch.

| What you see | What it means | What to try |
| --- | --- | --- |
| Both losses high and flat | **Underfitting**, or a bug, or the learning rate is far off | Overfit one batch first; bigger model; check the learning rate; check the data/labels |
| Training falls, validation falls, then validation rises | **Overfitting** after the turning point | Early stopping at the best epoch; augmentation; dropout; weight decay; more data; smaller model |
| Training loss falls very slowly | Learning rate too low | Raise it (×3–×10) |
| Loss jumps around or becomes `NaN` | Learning rate too high, bad inputs, or numerical issues | Lower the learning rate; clip gradients; normalize inputs; check for `NaN`/`inf` in data |
| Validation is better than training | Usually dropout/augmentation are on during training only; fine | Or validation is too easy / leaking — check |
| Validation metric noisy epoch to epoch | Small validation set | Average over more batches; larger validation set |
| Great validation, bad on new data | Leakage or distribution shift | Check the split (see the [leakage guide](splits-validation-leakage.md)) |

---

## 4. "My training doesn't work" checklist

Go in order. Don't skip to tuning.

1. **Look at the data going in.** Plot a batch of images with their labels; decode a batch of tokens back to text. Wrong labels, wrong channel order and blank images are common.
2. **Check the initial loss.** For C classes with cross-entropy, it should be about `ln(C)` (2.3 for 10 classes). Much higher means a bug in the output layer or labels.
3. **Overfit one small batch** (e.g. 32 examples) to ~100% training accuracy. If it can't, there's a bug: wrong loss, labels misaligned, gradients not flowing, `zero_grad()` missing.
4. **Check shapes** at every layer for one batch.
5. **Find a working learning rate** (try 1e-4, 3e-4, 1e-3, 3e-3 for a few hundred steps).
6. **Only then** train fully, and then **regularize** if it overfits.
7. **Change one thing at a time,** and log every run.

### Classic PyTorch bugs

| Bug | Symptom |
| --- | --- |
| Missing `optimizer.zero_grad()` | Gradients accumulate; training unstable |
| Softmax before `CrossEntropyLoss` | Training slow or stuck (the loss already applies softmax) |
| No `model.eval()` / `torch.no_grad()` in validation | Noisy validation; dropout/batch norm in training mode; extra memory |
| Model and data on different devices | "Expected all tensors to be on the same device" |
| Labels with wrong dtype or shape | Errors, or the wrong loss being computed |
| Augmentation applied to validation | Noisy and wrong validation scores |
| Shuffling off for training | Slower, worse training |

---

## 5. Regularization toolbox

| Technique | What it does | When |
| --- | --- | --- |
| **Early stopping** | Keep the checkpoint with the best validation score | Always |
| **Data augmentation** | Random flips, crops, colour changes (images); noise, masking (other data) | Images especially; the strongest regularizer for vision |
| **Weight decay** | Penalizes large weights | Default with AdamW |
| **Dropout** | Randomly zeroes activations in training | MLPs and transformers; less needed in CNNs with batch norm |
| **Smaller model** | Fewer parameters | When data is small |
| **More data / pretraining** | The most powerful fix | Always the first thing to consider |
| **Label smoothing** | Softens one-hot targets | Classification with many classes |

**Normalization layers** (BatchNorm in CNNs, LayerNorm in transformers) make training more stable rather than regularizing much. Keep them.

---

## 6. Memory and speed on your Mac

- **Device:** `device = "mps" if torch.backends.mps.is_available() else "cpu"`. Move the model *and* every batch.
- **Out of memory:** smaller batch size → shorter sequences/smaller images → smaller model → gradient accumulation (several small batches before one optimizer step).
- **Mixed precision** (`float16`/`bfloat16`) halves memory and speeds things up on CUDA. On MPS, support is improving but less complete: if you hit errors, use fp32.
- **DataLoader:** `num_workers=2–4` keeps the GPU fed; profile before tuning.
- **Rough memory for training with Adam:** about 16 bytes per parameter (weights + gradients + optimizer state) plus activations. A 100M-parameter model needs ~1.6 GB before activations. For LLM sizes, see [Transformers and LLM concepts](transformers-and-llms.md#5-memory-math).
- **When to use Colab:** CUDA-only libraries (`bitsandbytes`), or runs that would tie up your laptop for many hours.

---

## 7. Logging and checkpoints

- Log every run: config (all settings), training/validation loss and metrics per epoch, time per epoch, seed.
- Save checkpoints with model **and** optimizer state, step number and config, so you can resume.
- Keep the **best** checkpoint (by validation), not just the last.
- Simple CSV/JSON logs are enough. TensorBoard or Weights & Biases make comparing runs easier.
