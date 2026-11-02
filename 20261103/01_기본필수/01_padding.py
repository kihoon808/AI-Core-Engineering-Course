import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

from torch.nn.utils.rnn import pad_sequence
# 서로 길이가 다른 3개 자료. 각 시점의 특성 수는 3개이다.
sequences = [torch.ones(4,3), torch.ones(2,3)*2, torch.ones(5,3)*3]
# TODO B01: B가 첫 축인 [3,5,3] Padding Tensor를 만든다.
# batch_first의 기본값은 False이다. 여기서는 True로 바꾼다.
padded = pad_sequence(sequences, batch_first=True)

print("입력 길이:", [len(x) for x in sequences])
print("Padding shape:", tuple(padded.shape))
print("두 번째 자료:\n", padded[1])

"""
왜 패딩(Padding)이 필요한가?

딥러닝 프레임워크(PyTorch 등)의 행렬 곱 연산은 기본적으로 직사각형 형태의 정형 텐서(Tensor)를 요구합니다. 
하지만 문장이나 시계열 데이터는 샘플마다 길이가 제각각입니다:

1번째 샘플: 길이 4
2번째 샘플: 길이 2
3번째 샘플: 길이 5

이를 하나의 배치(Batch) 텐서로 묶으려면 가장 긴 샘플(길이 5)에 맞춰 부족한 시점들을 0(Zero)으로 채워 크기를 통일해야 합니다.
이를 처리해 주는 함수가 바로 pad_sequence입니다.

---

batch_first=False (기본값)일 때:
결과 형상: (최대 길이 L, 배치 크기 B, 특성 수 F) = (5, 3, 3)
과거 레거시 RNN 구현체들이 주로 사용하던 형태입니다.

batch_first=True일 때:
결과 형상: (배치 크기 B, 최대 길이 L, 특성 수 F) = (3, 5, 3)
현대 딥러닝(Transformer, 일반적인 배치 파이프라인)에서 사용하는 표준 축 순서입니다.
"""