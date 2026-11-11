"""
실습 05: YOLO 검증(Validation) 및 클래스별 평가 지표 산출
학습된 모델 가중치로 검증 데이터셋(val)을 평가합니다.
mAP50, mAP50-95 및 클래스별 정밀도/재현율을 JSON과 CSV로 저장합니다.
"""
from pathlib import Path
import json, yaml, torch
import pandas as pd
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent
if __name__ == "__main__":
    torch.set_num_threads(1)
    out = BASE / "outputs"; out.mkdir(exist_ok=True)
    config = {"train": str(BASE / "data/images/train"), "val": str(BASE / "data/images/val"), "names": ["square", "circle", "triangle"]}
    path = out / "dataset_active.yaml"; path.write_text(yaml.safe_dump(config), encoding="utf-8")
    model = YOLO(str(BASE / "data/demo.pt"))
    # >>> A05
    # 검증 데이터셋에 대해 모델 평가(val)를 수행합니다.
    metrics = model.val(data=str(path), split="val", imgsz=160, batch=4, device="cpu", workers=0)
    # <<< A05
    summary = {"map50": float(metrics.box.map50), "map50_95": float(metrics.box.map), "split": "val"}
    (out / "validation_metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    rows = []
    for i, cls in enumerate(metrics.box.ap_class_index):
        pr, rc, ap50, ap = metrics.box.class_result(i)
        rows.append([int(cls), model.names[int(cls)], float(pr), float(rc), float(ap50), float(ap)])
    pd.DataFrame(rows, columns=["class_id", "name", "precision", "recall", "ap50", "ap50_95"]).to_csv(out / "class_metrics.csv", index=False)
    print(summary)
