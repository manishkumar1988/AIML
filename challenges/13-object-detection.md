# 13 — Object detection

**Phase 4 · Computer vision** · ⏱ 1 week · 💻 Laptop or Colab · Level: core

[← 12 Transfer learning](12-transfer-learning.md) · [Index](../README.md) · [Next: 14 Image segmentation →](14-image-segmentation.md)

## The problem

A wildlife reserve has camera traps. They don't just want to know "is there an elephant in this photo?" They want to know **where each animal is and how many there are**. That's object detection: predicting a box and a class for every object.

Dataset: Ultralytics' [African Wildlife](https://docs.ultralytics.com/datasets/detect/african-wildlife/) dataset: buffalo, elephant, rhino and zebra, about 1,500 images with boxes. It downloads automatically when you train with `data="african-wildlife.yaml"`. (If it's unavailable, use `coco8.yaml` for mechanics and any small detection set from the Ultralytics docs.)

## Decide first

1. How is detection different from classification? What does the model output for one image?
2. A predicted box overlaps the true box by half. Is that a correct detection? Who decides?
3. What would you use as a baseline before fine-tuning?
4. Which is worse for the reserve: missing an animal, or a box around a bush?

## Learn

- **Detection output:** for each object, a box (x, y, width, height), a class, and a confidence score.
- **IoU (intersection over union):** overlap of a predicted box with the true box, from 0 to 1. A detection usually counts as correct if IoU ≥ 0.5 *and* the class is right.
- **Precision/recall for detection:** every predicted box is a true positive or false positive; every true box that's missed is a false negative.
- **mAP@0.5:** average precision per class at IoU 0.5, averaged over classes. **mAP@0.5:0.95** averages over stricter IoU thresholds too. It rewards tight boxes.
- **Confidence threshold and NMS:** low-confidence boxes are dropped; overlapping duplicate boxes are merged (non-maximum suppression).
- **YOLO** is a fast one-stage detector family. The `ultralytics` library makes it easy to train. Note: it's licensed AGPL-3.0, which matters for commercial use.

Read: Ultralytics [Quickstart](https://docs.ultralytics.com/quickstart/) and [Performance metrics guide](https://docs.ultralytics.com/guides/yolo-performance-metrics/).

## Build

Work in `work/13-detection/`. `uv add ultralytics`.

1. **Look at the data.** Train once for 1 epoch to trigger the download, then open the dataset folder. Read one label file. Draw the boxes on 6 images yourself with matplotlib.
   ✅ You can explain the label format (class id and normalized `x_center y_center width height`) and your drawn boxes line up with the animals.

2. **IoU by hand.** Write `iou(box_a, box_b)` and test it on 3 cases: identical boxes (1.0), no overlap (0.0), half overlap.
   ✅ All three pass.

3. **Pretrained baseline.** Run a COCO-pretrained small YOLO model (e.g. `yolo11n.pt`) on validation images without training. COCO includes elephants and zebras, but not buffalo or rhino. Count how many animals it finds and with which labels.
   ✅ It finds elephants and zebras reasonably well, and mislabels or misses buffalo and rhino. Write down why.

4. **Fine-tune.** Train the small model on the dataset (`device="mps"`, `imgsz=640`, ~30–50 epochs; use Colab if it's too slow).
   ✅ A results folder with curves; validation mAP@0.5 clearly above what the pretrained model could do on all 4 classes.

5. **Read the metrics.** From the validation report: precision, recall, mAP@0.5 and mAP@0.5:0.95, per class.
   ✅ You can explain why mAP@0.5:0.95 is much lower than mAP@0.5.

6. **Error taxonomy.** Look at 30 validation images with predictions drawn. Put each mistake in one bucket: missed animal, extra box (background), right box wrong class, box too loose/tight (IoU < 0.5), duplicate box.
   ✅ A table with counts per bucket. Which bucket dominates?

7. **Threshold.** Change the confidence threshold (0.1, 0.25, 0.5, 0.75) and record precision and recall. Which would you choose for the reserve, and why?

8. Write `NOTES.md`.

## Hints

<details><summary>Hint 1 — training is slow on the laptop</summary>

Try `imgsz=416` and fewer epochs to debug. For the final run, use Colab: the same `ultralytics` commands work there. Copy `best.pt` back.
</details>

<details><summary>Hint 2 — how to draw predictions</summary>

`results = model.predict(img_path)`; `results[0].boxes.xyxy`, `.cls`, `.conf` give you the boxes. `results[0].plot()` draws them for you, but draw your own at least once.
</details>

## Common mistakes

- Judging a detector by classification accuracy.
- Comparing mAP numbers computed with different IoU thresholds.
- Forgetting the class-mapping problem when using a pretrained model's labels.

## Done when

- [ ] Your own IoU function, tested.
- [ ] A pretrained baseline vs fine-tuned comparison, per class.
- [ ] An error taxonomy table from 30 images.
- [ ] A chosen confidence threshold, with the reason.
- [ ] `NOTES.md` explains mAP in your own words.

## Stretch

Label 30 of your own photos (any objects) with a free labelling tool such as [Label Studio](https://labelstud.io/) or CVAT, and fine-tune on them. Labelling teaches you more about detection than anything else.

## Reflect

- Fill in "classification vs detection vs segmentation" in the **Computer vision** section of your [decision map](../decision-map.md).
