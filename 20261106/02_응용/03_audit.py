"""
실습 03: 라벨 데이터셋 무결성 및 통계 감사(Audit)
라벨별 정규화 면적(w*h)과 픽셀 가로세로비를 계산합니다.
분할(split) 간 그룹 중복 및 파일 해시 중복 여부를 전수 검사합니다.
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
out = BASE / "outputs"; out.mkdir(exist_ok=True)
manifest = pd.read_csv(BASE / "data/manifest.csv")
rows = []

for image in manifest.itertuples():
    for line in (BASE / "data" / image.label).read_text(encoding="utf-8").splitlines():
        cls, cx, cy, w, h = map(float, line.split())
        # >>> A03
        # 정규화 면적과 픽셀 기준 가로세로비를 계산하여 기록합니다.
        area = w * h
        aspect_ratio = (w * image.width) / (h * image.height)
        rows.append({"split": image.split, "class_id": int(cls), "area": area, "aspect_ratio": aspect_ratio})
        # <<< A03

r = pd.DataFrame(rows); r.to_csv(out / "label_audit.csv", index=False)
print(r.groupby(["split", "class_id"]).size().unstack(fill_value=0).to_string())
print("split 간 그룹 중복:", int((manifest.groupby("group_id").split.nunique() > 1).sum()))
print("정확히 같은 파일:", int(manifest.sha256.duplicated().sum()))
print("빈 라벨은 정상 negative 이미지이며 누락 라벨과 다릅니다.")
