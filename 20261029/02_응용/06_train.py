"""실습 06: 80 epoch 학습하고 10 epoch마다 같은 시점의 지표를 기록합니다."""

from pathlib import Path
import csv
import json
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

#데이터 불러오기 및 텐서 변환
base = Path(__file__).resolve().parent
out = base / "outputs"
out.mkdir(exist_ok=True)
with (base / "data" / "points.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
#CSV 데이터 분할: split 컬럼의 값에 따라 학습용(train)과 검증용(valid) 행을 나눕니다. 
train_rows = [r for r in rows if r["split"] == "train"]
valid_rows = [r for r in rows if r["split"] == "valid"]
#라벨(label)은 교차 엔트로피 손실 함수 계산을 위해 정수형 롱 텐서(torch.long)로 구성합니다.
X_train = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in train_rows])
y_train = torch.tensor([int(r["label"]) for r in train_rows], dtype=torch.long)
X_valid = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in valid_rows])
y_valid = torch.tensor([int(r["label"]) for r in valid_rows], dtype=torch.long)

# test 40건은 모델에 전달하지 않습니다. 순서를 바꾸거나 다시 분할하지 않습니다.
torch.manual_seed(42) #난수 시드 고정
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#DataLoader: 학습 데이터를 배치 크기 32 단위로 묶어 제공하며, 매 에포크마다 순서를 무작위로 섞습니다(shuffle=True).
loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(43), num_workers=0)
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2)).to(device)
#손실 함수 및 옵티마이저: nn.CrossEntropyLoss()를 사용하고, 학습률이 0.1인 확률적 경사하강법(SGD)을 사용합니다.
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
Xv, yv = X_valid.to(device), y_valid.to(device)
Xt, yt = X_train.to(device), y_train.to(device)
history = []

for epoch in range(81):
    if epoch > 0:
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(xb), yb)
            # 현재 batch의 loss로 역전파하고 optimizer를 한 번 갱신하세요.
            # zero_grad와 순전파·손실 계산은 위에 제공되어 있습니다.
            # >>> A06
            # TODO A06: 위 요구사항을 읽고 이 블록을 완성하세요.
            loss.backward()   # 역전파로 각 파라미터의 기울기(gradient) 계산
            optimizer.step()  # 계산된 기울기를 적용하여 가중치 파라미터 업데이트
            # <<< A06
    # epoch=0은 학습 전입니다. 로그는 갱신이 끝난 동일 모델로 측정합니다.
    if epoch % 10 == 0:
        model.eval()
        with torch.no_grad():
            train_loss = loss_fn(model(Xt), yt).item()
            logits = model(Xv)
            valid_loss = loss_fn(logits, yv).item()
            accuracy = (logits.argmax(dim=1) == yv).float().mean().item()
        history.append([epoch, train_loss, valid_loss, accuracy])
        print(epoch, round(train_loss, 6), round(valid_loss, 6), round(accuracy, 4))

with (out / "training_history.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["epoch", "train_loss_eval", "valid_loss", "valid_accuracy"])
    writer.writerows(history)
