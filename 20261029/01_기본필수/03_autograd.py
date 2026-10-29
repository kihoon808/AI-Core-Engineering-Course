"""실습 03: x=3에서 y=x²+2x+1과 기울기를 계산합니다."""
import torch
x = torch.tensor(3.0, requires_grad=True)
# y = x² + 2x + 1을 Tensor 연산으로 작성하세요.
# x를 Python 숫자로 바꾸지 마세요. 계산 그래프가 이어져 있어야 합니다.
# >>> B03
# TODO B03: 위 요구사항을 읽고 이 블록을 완성하세요.
y = x ** 2 + 2 * x + 1 #Tensor 연산으로 작성
"""
왜 이것이 Tensor 연산인가요?(by gemini)
연산자 오버로딩 (Operator Overloading)
x가 이미 torch.Tensor 객체이기 때문에, 파이썬의 기본 기호(**, *, +)를 사용하면 내부적으로 PyTorch의 텐서 연산 함수가 자동으로 호출됩니다. 
따라서 연산 결과인 y 역시 일반 파이썬 숫자가 아니라 torch.Tensor 객체로 유지됩니다.
"""
# <<< B03
# backward는 y 값을 바꾸지 않고 x.grad에 기울기를 계산합니다.
y.backward()
print("y:", y.item())
print("dy/dx:", x.grad.item())