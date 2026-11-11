"""
실습 05: 학습 기록(Metrics) 해석 및 최적 에포크 선택
에포크별 위치·분류 평가 지표(mAP50, mAP50-95)를 비교합니다.
mAP50-95가 가장 높은 에포크의 행을 최적 모델 기록으로 선택합니다.
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
history = pd.read_csv(BASE / "data/metrics_example.csv")

# >>> B06
# mAP50-95 값이 가장 큰 행을 찾아 최적 기록으로 선택합니다.
best = history.loc[history["map50_95"].idxmax()]
# <<< B06

print("자료 종류: 읽기 연습용 가상 기록 — 실제 YOLO 성능 아님")
print("선택 epoch:", int(best["epoch"]))
print("mAP50:", best["map50"], "mAP50-95:", best["map50_95"])
print("mAP는 accuracy가 아닙니다. train이 아니라 valid의 위치·분류 평가 기록입니다.")
