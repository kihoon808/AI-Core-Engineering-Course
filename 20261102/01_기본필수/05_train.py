"""실습 05 · 제공된 CNN으로 5 epoch 학습한다. test는 읽지 않는다."""
from pathlib import Path
import copy
import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

root = Path(__file__).resolve().parent
torch.manual_seed(42)
torch.set_num_threads(1)
transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
train = datasets.ImageFolder(root / "data" / "train", transform=transform)
valid = datasets.ImageFolder(root / "data" / "valid", transform=transform)

# 작은 정상 데이터는 한 배치로 읽어 학습 순서를 단순하게 관찰한다.(하나의 배치(Full Batch)로 로드)
x_train, y_train = next(iter(DataLoader(train, batch_size=len(train), shuffle=False)))
x_valid, y_valid = next(iter(DataLoader(valid, batch_size=len(valid), shuffle=False)))

model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 2),
)
"""
1단계 합성곱 블록: 입력 채널 3(RGB) -> 출력 채널 16, 3x3 커널, ReLU 활성화 -> 2x2 MaxPool(해상도 32x32 -> 16x16 축소).
2단계 합성곱 블록: 채널 16 -> 32, 3x3 커널, ReLU -> 2x2 MaxPool(해상도 16x16 -> 8x8 축소).

분류 헤드(Classifier):
    AdaptiveAvgPool2d(1): 공간 해상도를 1x1로 압축하여 채널당 대표값 1개만 추출 (형상: (N, 32, 1, 1)).
    Flatten(): 1차원 벡터로 평탄화 (형상: (N, 32)).
    Linear(32, 2): 32차원을 2개 클래스 로짓(Logits)으로 변환하는 최종 완전연결층.
"""

optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=0.0)
loss_fn = nn.CrossEntropyLoss()
best_loss = float("inf")
for epoch in range(1, 6):
    model.train()           # 1. 모델을 학습 모드로 전환
    optimizer.zero_grad()   # 2. 이전 스텝의 기울기(gradient) 초기화
    logits = model(x_train) # 3. 순전파(Forward Pass): 예측 로짓 계산
    loss = loss_fn(logits, y_train) # 4. 손실(Loss) 계산
    # 해설 B05: backward는 미분값 계산, step은 그 값을 이용한 갱신이다.
    # TODO B05: loss를 역전파하고 optimizer로 한 번 갱신한다.
    loss.backward()         # 5. 역전파(Backpropagation): 각 가중치별 기울기(grad) 계산
    optimizer.step()        # 6. 계산된 기울기를 사용해 가중치 갱신

    model.eval() #모델을 평가 모드로 전환.
    with torch.no_grad():
        train_loss = loss_fn(model(x_train), y_train).item()
        valid_logits = model(x_valid)
        valid_loss = loss_fn(valid_logits, y_valid).item()
        valid_acc = (valid_logits.argmax(1) == y_valid).float().mean().item()
    print(f"epoch={epoch} train_loss={train_loss:.4f} valid_loss={valid_loss:.4f} valid_acc={valid_acc:.2f}")
    if valid_loss < best_loss:
        best_loss, best_epoch = valid_loss, epoch
        best_state = copy.deepcopy(model.state_dict())

#에포크 종료 후 가장 검증 성능이 좋았던 에포크의 가중치로 최종 복원
model.load_state_dict(best_state)
print("선택한 epoch:", best_epoch)
