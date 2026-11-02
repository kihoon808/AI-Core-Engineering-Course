"""실습 06 · 실제 ImageNet 사전학습 가중치로 Head만 학습한다.
최초 1회 공식 가중치 다운로드/캐시가 필요하다. 인터넷 없으면 교사에게 요청한다.
weights=None으로 바꾼 실험은 전이학습 결과가 아니다. 자동 대체하지 않는다.
"""
from pathlib import Path
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.models import resnet18, ResNet18_Weights

torch.manual_seed(42)
torch.set_num_threads(1)
root = Path(__file__).resolve().parent

weights = ResNet18_Weights.IMAGENET1K_V1 #약 140만 장의 ImageNet 데이터로 학습된 공식 가중치를 지정합니다.
transform = weights.transforms()  # 이 가중치의 Resize·Crop·Normalize를 그대로 사용한다.
train = datasets.ImageFolder(root / "data" / "train", transform=transform)
valid = datasets.ImageFolder(root / "data" / "valid", transform=transform)
loader = DataLoader(train, batch_size=4, shuffle=False, num_workers=0)
model = resnet18(weights=weights) #공식 PyTorch 가중치가 다운로드되어 모델의 파라미터로 적재됩니다.

# 해설 B06: 모든 기존 가중치의 미분을 끄고 새 Head를 붙인다.
# TODO B06: 기존 parameter의 requires_grad를 False로 설정한다.
for parameter in model.parameters():
    parameter.requires_grad = False
#전이학습의 핵심은 이미 잘 훈련된 합성곱 계층(Backbone)의 가중치를 망가뜨리지 않도록 잠그는 것입니다.
#requires_grad = False로 설정해야 역전파 시 미분값(Gradient)이 계산되지 않고 파라미터가 고정됩니다.

model.fc = nn.Linear(model.fc.in_features, 2)
optimizer = torch.optim.AdamW(model.fc.parameters(), lr=0.001, weight_decay=0.0)
loss_fn = nn.CrossEntropyLoss()
"""
model.fc: ResNet-18의 마지막 완전연결층(Fully Connected Layer)입니다. 
본래 1,000개 클래스 출력이던 것을 현재 실습 목적에 맞게 2개 클래스 출력으로 교체합니다.

새로 선언된 model.fc의 가중치들은 기본적으로 requires_grad = True 상태가 됩니다.
optimizer: 모델 전체(model.parameters())가 아니라, 새로 교체한 분류기 model.fc.parameters()만 전달하여 연산량과 메모리를 극적으로 절약합니다.
"""

# eval은 역전파를 끄지 않는다. Backbone의 BN 통계까지 고정한다.
model.eval()
model.fc.train()
for epoch in range(3):
    for images, labels in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(images), labels)
        loss.backward()
        optimizer.step()
model.eval()
with torch.no_grad():
    images, labels = next(iter(DataLoader(valid, batch_size=len(valid))))
    accuracy = (model(images).argmax(1) == labels).float().mean().item()
    
print("실제 사전학습:", weights.name)
print("학습 파라미터:", sum(p.numel() for p in model.parameters() if p.requires_grad))
print("입력 크기:", tuple(images.shape))
print("valid 정확도:", round(accuracy, 4))
print("SmallCNN은 32×32 / ResNet은 224×224이므로 조건 차이를 기록한다.")
