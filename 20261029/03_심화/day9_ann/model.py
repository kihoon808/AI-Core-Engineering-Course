"""모델 구조만 정의합니다. 이 파일을 실행해도 학습하지 않습니다."""
from torch import nn

"""
 torch.nn.Module을 상속한 2계층 신경망.
입력층 -> 은닉층: nn.Linear(2, 8) (2차원 입력을 8차원으로 변환)
활성화 함수: nn.ReLU()
은닉층 -> 출력층: nn.Linear(8, 2) (2개 클래스에 대한 로짓 Logits 반환)
"""
class SimpleANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2,8), nn.ReLU(), nn.Linear(8,2))

    def forward(self, x):
        return self.net(x)
