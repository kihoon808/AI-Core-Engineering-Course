"""실습 02: reshape와 broadcasting을 확인합니다."""
import torch

a = torch.arange(6, dtype=torch.float32)
# 원소 6개를 2행 3열로 바꾸어 matrix에 저장하세요.
# 아래 bias는 각 열에 더해집니다.
# >>> A02
# TODO A02: 위 요구사항을 읽고 이 블록을 완성하세요.
matrix = a.reshape(2, 3) #reshape로 2행 3열로 변환
# <<< A02
bias = torch.tensor([10., 20., 30.]) #bias는 열에 더해진다.
result = matrix + bias #broadcasting으로 각 열에 더해짐
print("변환 전:", tuple(a.shape)) # (6,) -> 6개짜리 1차원 텐서
print("행렬:", tuple(matrix.shape), matrix.tolist()) # (2, 3) -> 2행 3열 텐서
print("보정 후:", tuple(result.shape), result.tolist()) # (2, 3) -> 2행 3열 텐서
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # CUDA가 사용 가능하면 cuda:0, 아니면 cpu로 설정
moved = result.to(device) # 텐서를 device로 이동
print("이동 장치:", moved.device) # 이동한 텐서의 장치 확인
print("CPU에서 확인:", moved.cpu().tolist()) # CPU에서 확인
