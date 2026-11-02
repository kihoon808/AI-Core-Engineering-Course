"""실습 01 · RGB 이미지의 N,C,H,W를 확인한다. 실제 사진 대신 정상 Tensor 4장."""
import torch

torch.manual_seed(42) #torch.manual_seed(42)는 난수(랜덤 값) 생성기의 시작 기준값(Seed)을 고정하는 코드입니다.
# 필수: 각 차원의 크기. 선택: dtype, device. 기본 float32·CPU를 사용한다.
# TODO B01: RGB 이미지 4장, 높이·너비 32인 Tensor를 만든다.
# N(이미지 수): 4
# C(채널): 3
# H(높이): 32
# W(너비): 32
images = torch.rand(4, 3, 32, 32) # NCHW

print("shape:", tuple(images.shape))
print("dtype:", images.dtype)
print("device:", images.device)
print("첫 이미지:", tuple(images[0].shape))