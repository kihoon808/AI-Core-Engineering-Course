"""
실습 02: IoU 계산 및 예측-정답 1:1 매칭
예측 박스와 정답 박스 간의 겹치는 비율(IoU)을 계산합니다.
IoU가 0.5 이상이고 클래스가 같을 때만 정답(TP)으로 연결하며 한 번만 씁니다.
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
pred = pd.read_csv(BASE / "data/boxes_fixture.csv")  # confidence 내림차순 예시
truth = pd.read_csv(BASE / "data/boxes_gt.csv")
used = set()  # 하나의 정답은 한 번만 TP로 연결합니다.
rows = []

for p in pred.itertuples():
    overlaps = []
    for g in truth.itertuples():
        width = max(0, min(p.x2, g.x2) - max(p.x1, g.x1))
        height = max(0, min(p.y2, g.y2) - max(p.y1, g.y1))
        intersection = width * height
        union = (p.x2 - p.x1) * (p.y2 - p.y1) + (g.x2 - g.x1) * (g.y2 - g.y1) - intersection
        # >>> B02
        # 교집합 면적을 합집합 면적으로 나누어 IoU를 구합니다.
        iou = intersection / union
        # <<< B02
        overlaps.append(iou)
    matched = False
    for j in np.argsort(-np.asarray(overlaps)):
        if truth.iloc[j].class_id != p.class_id or j in used:
            continue
        # >>> B03
        # IoU가 0.5 이상이면 정답과 연결하고 사용 목록에 추가합니다.
        if overlaps[j] >= 0.5:
            matched = True
            used.add(j)
            break
        # <<< B03
    rows.append([p.class_id, p.confidence, round(max(overlaps), 4), "TP" if matched else "FP"])

table = pd.DataFrame(rows, columns=["class", "confidence", "max_iou", "result"])
print(table.to_string(index=False))
tp = len(used); fp = len(pred) - tp; fn = len(truth) - tp
print("TP/FP/FN:", tp, fp, fn)
print("Precision/Recall:", round(tp / len(pred), 4), round(tp / len(truth), 4))
table.to_csv(BASE / "p02_matching.csv", index=False, encoding="utf-8-sig")
