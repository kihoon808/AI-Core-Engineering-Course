"""실습 05: 정답 인덱스와 logits로 손실을 계산합니다."""
import torch
from torch import nn

logits = torch.tensor([[2.0, 0.0], [0.0, 2.0]]) #모델이 출력한 가공되지 않은 예측 점수(raw score)입니다
target = torch.tensor([0, 1], dtype=torch.long) #각 데이터의 실제 정답 클래스 번호(인덱스)입니다
loss_fn = nn.CrossEntropyLoss()
"""
nn.CrossEntropyLoss의 특징(by gemini):
내부적으로 LogSoftmax와 NLLLoss(Negative Log Likelihood Loss)가 하나로 합쳐져 있습니다.
따라서 모델 출력값(logits)에 사용자가 별도로 softmax를 취해서 넘기면 확률값에 다시 소프트맥스가 적용되어 잘못된 손실값이 계산됩니다.
모델의 선형 계층(Linear layer)에서 나온 점수 그대로를 전달해야 합니다.
"""
# loss_fn에 logits와 target을 순서대로 넣어 loss를 계산하세요.
# logits에 softmax를 먼저 적용하지 마세요.
# >>> B05
# TODO B05: 위 요구사항을 읽고 이 블록을 완성하세요.
loss = loss_fn(logits, target)
# <<< B05
print("logits:", tuple(logits.shape))
print("target:", tuple(target.shape), target.dtype)
print("loss:", round(loss.item(), 6))
