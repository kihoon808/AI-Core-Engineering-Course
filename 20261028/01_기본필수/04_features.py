"""실습 04: 다른 행의 통계나 정답을 사용하지 않는 파생 열 하나를 만듭니다."""
from pathlib import Path
import pandas as pd
import numpy as np
raw = pd.read_csv(Path(__file__).resolve().parent / "requests.csv")
# 원본 파일은 덮어쓰지 않습니다. 글자 수만 복사하고 정답·실행시간은 선택하지 않습니다.
features = raw[["input_chars"]].copy()
# TODO B04: np.log1p로 글자 수의 로그 변환 열을 추가하세요. 각 행의 값만 사용합니다.
# 행별 log(1+x) 변환으로 다른 행의 평균 등 통계를 참조하지 않아 누수가 발생하지 않습니다.
features["log_input_chars"] = np.log1p(features["input_chars"])
print(features.head().round(3).to_string(index=False))
print("행/열:", features.shape)
print("원본 열:", raw.columns.tolist())