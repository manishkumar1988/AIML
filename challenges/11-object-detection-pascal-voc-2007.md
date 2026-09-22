# Challenge 11 — Object detection on Pascal VOC 2007

[Previous: Challenge 10 — Transfer learning with a pre-registered win](10-transfer-learning-pre-registered-win.md) · [Next: Challenge 12 — Datasets, splits, and a dataset card](12-datasets-splits-dataset-card.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 11 — Object detection on Pascal VOC 2007

- **Goal:** Fine-tune a small detector and separate localization errors from classification errors.
- **Why an engineer needs it:** Detection is the step from “what is in the image” to “where is it.” mAP is the contract. Classification accuracy on crops is a different product.
- **What to build:** Fine-tune a small detector on Pascal VOC 2007 (`torchvision.datasets.VOCDetection`, year `2007`). Use the official train and val for training choices, and the official 2007 test set once for the published mAP. Headline: mAP at IoU 0.50. Before fine-tuning, score the pretrained COCO checkpoint on VOC test as a zero-shot-style baseline (label-space mismatch included: write how you mapped or skipped classes). Then fine-tune. From 50 errors, label each as missed box, extra box, right box wrong class, or poor localization (IoU with the right class below 0.50).
- **Skills practiced:** Bounding boxes, IoU, mAP, localization versus classification.
- **Stack and data:** PyTorch and torchvision. Pascal VOC 2007 via `VOCDetection`. If the official download host fails, use a public mirror and record the URL in the data note.
- **Difficulty:** stretch
- **Rough time:** 1–2 weeks
- **GPU:** small GPU. Colab-or-Kaggle fallback.
- **Acceptance criteria:**
  - mAP@0.50 for the pretrained baseline and the fine-tune are in the log, with the class mapping written down.
  - The 50-error taxonomy has counts in the four buckets above.
  - You did not use a private evaluation server. VOC 2007 test labels are local.
  - The README states the GPU and the wall-clock time.
- **Stretch goal:** Semantic segmentation on the [Carvana Image Masking Challenge](https://www.kaggle.com/competitions/carvana-image-masking-challenge) images you can fit locally, scored by mean IoU, with a per-image failure note. A pixel-accuracy headline does not count.
- **Builds on:** Challenges 9–10.
