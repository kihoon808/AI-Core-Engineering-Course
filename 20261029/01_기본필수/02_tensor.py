"""실습 02: 값뿐 아니라 shape·dtype·device를 같이 확인합니다."""
import torch
scalar = torch.tensor(3.0)
vector = torch.tensor([1.0, 2.0, 3.0])
# TODO B02: 위 요구사항을 읽고 이 블록을 완성하세요.
#[[1.0, 2.0], [3.0, 4.0]]을 torch.float32의 2차원 Tensor matrix로 변환
matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32) 

matrix = matrix.to("cpu")
print("스칼라:", tuple(scalar.shape), scalar.dtype, scalar.device)
print("벡터:", tuple(vector.shape), vector.dtype, vector.device)
print("행렬:", tuple(matrix.shape), matrix.dtype, matrix.device)
print("행렬 값:", matrix.tolist())
