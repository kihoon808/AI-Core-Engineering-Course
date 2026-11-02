"""실습 02 · 공간 크기를 유지하고 특징 채널을 8개 만든다."""
import torch
from torch import nn

torch.manual_seed(42)
x = torch.rand(4, 3, 32, 32)
# padding=1은 선택 인자. 3×3, stride=1과 결합하면 높이·너비를 유지한다.
# TODO B02: 3입력·8출력·3×3·padding 1의 합성곱 층을 만든다.
conv = nn.Conv2d(3, 8, 3, padding=1) # 3입력, 8출력, 3×3 커널, padding=1

y = conv(x)
print("입력:", tuple(x.shape))
print("출력:", tuple(y.shape))
print("파라미터:", sum(p.numel() for p in conv.parameters()))

"""
1. 출력 크기 계산 공식
Output = ((Input - Kernel + 2 * Padding) / Stride) + 1
높이 및 너비: ((32 - 3 + 2 * 1) / 1) + 1 = 32
따라서 최종 출력 형태는 (4, 8, 32, 32)가 됩니다.

2. 파라미터 수 계산
가중치(weights): 8(출력채널) * 3(입력채널) * 3 * 3(커널크기) = 216개
편향(bias): 기본값으로 bias=True이므로 출력 채널당 1개씩 = 8개
총 파라미터 수: 216 + 8 = 224개
"""