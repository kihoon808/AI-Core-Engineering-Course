"""실습 07~08: 정상 데이터 20건. train 12건 학습, valid 4건 확인, test 4건 보관."""
from pathlib import Path
import csv
import json
import torch
from torch import nn

# 파일 위치를 기준으로 읽으므로 다른 작업 폴더에서 실행해도 됩니다.
base = Path(__file__).resolve().parent
with (base / "points.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
train_rows = [r for r in rows if r["split"] == "train"]
valid_rows = [r for r in rows if r["split"] == "valid"]
X_train = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in train_rows])
y_train = torch.tensor([int(r["label"]) for r in train_rows], dtype=torch.long)
X_valid = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in valid_rows])
y_valid = torch.tensor([int(r["label"]) for r in valid_rows], dtype=torch.long)

# 기본필수는 CPU 고정, full-batch 80회입니다. test는 Tensor로 만들지 않습니다.
torch.manual_seed(42)
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
history = [[0, loss_fn(model(X_train), y_train).item()]]
model.train()
for epoch in range(1, 81):
    optimizer.zero_grad()
    loss = loss_fn(model(X_train), y_train)
    # 06번에서 배운 역전파와 파라미터 갱신 두 문장을 연결하세요.
    # 이미 위에서 이전 gradient를 비우고 loss를 계산했습니다.
    # >>> B08
    # TODO B08: 위 요구사항을 읽고 이 블록을 완성하세요.
    loss.backward()   # 역전파로 각 파라미터의 기울기 계산
    optimizer.step()  # 옵티마이저로 가중치 갱신
    # <<< B08
    # 갱신 후 같은 train 자료의 loss를 기록합니다. 마지막 batch loss와 구분합니다.
    with torch.no_grad():
        history.append([epoch, loss_fn(model(X_train), y_train).item()])

#모델을 평가 모드로 전환하고 불필요한 기울기 계산을 비활성화합니다.
model.eval()
with torch.no_grad():
    logits = model(X_valid)
    # 각 행에서 가장 큰 logit의 열 번호를 prediction으로 구하세요.
    # argmax의 dim=1은 클래스 방향입니다. 결과 shape는 (4,)입니다.
    # >>> B09
    # TODO B09: 위 요구사항을 읽고 이 블록을 완성하세요.
    #각 행에서 가장 큰 값을 가진 열의 인덱스(0 또는 1)를 추출
    prediction = logits.argmax(dim=1) #logits: 모델이 출력한 검증 데이터 4건에 대한 점수 텐서 (크기: 4 x 2).
    # <<< B09
    #예측과 실제 레이블 비교하여 정확도 계산
    accuracy = (prediction == y_valid).float().mean().item()

#에포크 0부터 80까지의 손실값 변화 추이를 저장합니다.
with (base / "training_history.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["epoch", "train_loss_eval"])
    writer.writerows(history)

"""
final_metrics.json: 모델 파라미터 정보, 최종 정확도, 실제 라벨과 예측 결과를 JSON 파일로 기록합니다.
gpu_check.txt: PyTorch 버전 및 사용된 연산 장치(CPU) 정보를 남깁니다.
콘솔에 학습 전후의 손실값 변화와 검증 데이터 정확도를 요약하여 출력합니다.
"""
metrics = {"device": "cpu", "epochs": 80, "train_rows": 12, "valid_rows": 4,
           "test_used": False, "valid_accuracy": accuracy,
           "initial_train_loss": history[0][1], "final_train_loss": history[-1][1],
           "valid_ids": [r["id"] for r in valid_rows], "actual": y_valid.tolist(),
           "predicted": prediction.tolist()}
(base / "final_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
(base / "gpu_check.txt").write_text(
    f"torch={torch.__version__}\ncuda_build={torch.version.cuda}\n"
    f"cuda_available={torch.cuda.is_available()}\nselected_device=cpu\n", encoding="utf-8")
print("분할: train 12 / valid 4 / test 4(보관)")
print("train loss:", round(history[0][1], 6), "->", round(history[-1][1], 6))
print("valid 정확도:", round(accuracy, 4))
print("valid 예측:", prediction.tolist())
print("생성: gpu_check.txt, training_history.csv, final_metrics.json")
