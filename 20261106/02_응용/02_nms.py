"""
실습 02: 비최대 억제(NMS, Non-Maximum Suppression) 원리 비교
동일한 클래스 내에서 겹치는 중복 예측 박스를 신뢰도 순으로 걸러냅니다.
신뢰도 임계값과 IoU 임계값에 따라 남는 박스(kept)와 정밀도/재현율을 대조합니다.
"""
from pathlib import Path
import torch
import pandas as pd
from torchvision.ops import box_iou, batched_nms

BASE = Path(__file__).resolve().parent
out = BASE / "outputs"; out.mkdir(exist_ok=True)
p = pd.read_csv(BASE / "data/boxes_fixture.csv"); g = pd.read_csv(BASE / "data/boxes_gt.csv")
boxes = torch.tensor(p[["x1", "y1", "x2", "y2"]].to_numpy(), dtype=torch.float32)
scores = torch.tensor(p.confidence.to_numpy(), dtype=torch.float32)
classes = torch.tensor(p.class_id.to_numpy(), dtype=torch.int64)
gb = torch.tensor(g[["x1", "y1", "x2", "y2"]].to_numpy(), dtype=torch.float32)

rows = []
for conf, nms_iou in [(0.25, 0.5), (0.5, 0.5), (0.25, 0.95)]:
    ids = torch.where(scores >= conf)[0]
    # >>> A02
    # 클래스별로 중복 박스를 제거하고 원래 인덱스로 매핑합니다.
    keep_sub = batched_nms(boxes[ids], scores[ids], classes[ids], nms_iou)
    keep = ids[keep_sub]
    # <<< A02
    used = set(); tp = 0
    for i in keep.tolist():
        ovs = box_iou(boxes[[i]], gb)[0]
        eligible = [j for j in range(len(g)) if int(classes[i]) == int(g.iloc[j].class_id) and j not in used]
        for j in sorted(eligible, key=lambda j: -float(ovs[j])):
            if ovs[j] >= 0.5: used.add(j); tp += 1; break
    n = len(keep); fp = n - tp; fn = len(g) - tp
    rows.append(dict(conf=conf, nms_iou=nms_iou, kept=n, tp=tp, fp=fp, fn=fn, precision=tp / n if n else 0, recall=tp / len(g)))

r = pd.DataFrame(rows); r.to_csv(out / "nms_comparison.csv", index=False); print(r.round(4).to_string(index=False))
