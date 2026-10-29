"""실습 04: 2 → 8 → 2 신경망의 순전파를 확인합니다."""
import torch
from torch import nn

torch.manual_seed(42)
# Sequential의 마지막 Linear를 수정해 출력 클래스 수가 2가 되게 하세요.
# 첫 Linear(2, 8)와 ReLU는 그대로 두세요. 모델 정의는 미리 제공했습니다.
# >>> B04
# TODO B04: 위 요구사항을 읽고 이 블록을 완성하세요.
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
"""
nn.Linear(2, 8): 2개의 입력을 받아 8개의 은닉 특성으로 확장
nn.ReLU(): 0보다 작은 값을 0으로 만드는 활성화 함수 
nn.Linear(8, 2): 8개의 은닉 특성을 받아 2개의 최종 클래스 점수(logits) 로 축소
"""
# <<< B04   
#입력 데이터 X의 크기는 (4, 2)입니다. (샘플 데이터 4개, 각각 특성 2개)
X = torch.tensor([[1.0, 2.0], [3.0, 4.0], [0.0, 1.0], [2.0, 0.0]])
logits = model(X)
print("입력:", tuple(X.shape))
print("출력:", tuple(logits.shape))
print("파라미터 수:", sum(p.numel() for p in model.parameters()))
# logits는 원시 점수입니다. 이 시점에는 학습하지 않았습니다.
"""
파라미터 수(42개) 계산 원리
신경망에서 학습되는 파라미터는 가중치(Weight)와 편향(Bias)의 합입니다.

1번째 층 (Linear(2, 8)):

가중치: 2 * 8 = 16개
편향: 8개
1층 소계: 16 + 8 = 24개
2번째 층 (Linear(8, 2)):

가중치: 8 * 2 = 16개
편향: 2개
2층 소계: 16 + 2 = 18개
총 파라미터 수: 24 + 18 = 42개
"""