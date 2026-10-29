"""실습 07: 120건 학습, 40건 검증. test 40건은 다음 독립 평가용으로 보관합니다.

data/points.csv
총 200개의 데이터 샘플로 구성된 2차원 좌표 분류 데이터셋입니다.

id (문자열): 표본 고유 식별자 (예: P001, P002 등)
x1, x2 (실수형, float): 2차원 평면 위의 좌표 입력 특성(Features)
label (정수형, int): 클래스 레이블 (0 또는 1, 이진 분류)
split (문자열): 데이터셋 분할 기준
train: 학습용 데이터 (120건)
valid: 검증용 데이터 (40건)
"""

from pathlib import Path
import csv
import json
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from check_gpu import choose_device
from model import SimpleANN
from train import train_one_epoch, evaluate

base = Path(__file__).resolve().parent
out = base / "outputs"
out.mkdir(exist_ok=True)
with (base / "data" / "points.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
train_rows = [r for r in rows if r["split"] == "train"]
valid_rows = [r for r in rows if r["split"] == "valid"]
X_train = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in train_rows])
y_train = torch.tensor([int(r["label"]) for r in train_rows], dtype=torch.long)
X_valid = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in valid_rows])
y_valid = torch.tensor([int(r["label"]) for r in valid_rows], dtype=torch.long)
torch.manual_seed(42)
device, info = choose_device()
model = SimpleANN().to(device)
loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(43), num_workers=0)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
initial = evaluate(model, X_train, y_train, loss_fn, device)[0]
history = []
for epoch in range(1, 81):
    online_loss = train_one_epoch(model, loader, loss_fn, optimizer, device)
    valid_loss, accuracy, prediction = evaluate(model, X_valid, y_valid, loss_fn, device)
    history.append([epoch, online_loss, valid_loss, accuracy])
    if epoch % 10 == 0:
        print(epoch, round(online_loss, 6), round(valid_loss, 6), round(accuracy, 4))

# 아래는 저장 과정입니다. 전체 Module 대신 직접 학습한 파라미터 사전만 저장합니다.
# model의 state_dict를 outputs/model_state.pt로 저장하세요.
# 배포 파일에는 미리 학습한 모델이 없습니다. 실행한 본인이 만든 파일만 복원합니다.
torch.save(model.state_dict(), out / "model_state.pt") #모델 전체 객체 대신 학습된 파라미터 사전(state_dict)만 저장
with (out / "training_history.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w=csv.writer(f);w.writerow(["epoch","train_loss_online","valid_loss","valid_accuracy"]);w.writerows(history)
metrics = {"epochs":80,"device":str(device),"train_rows":120,"valid_rows":40,"test_used":False,
           "initial_train_loss":initial,"final_train_loss":evaluate(model,X_train,y_train,loss_fn,device)[0],
           "valid_loss":valid_loss,"valid_accuracy":accuracy}
(out / "final_metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding="utf-8")
(out / "gpu_check.txt").write_text("\n".join(f"{k}: {v}" for k,v in info.items()),encoding="utf-8")
with (out / "validation_predictions.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f);w.writerow(["id","actual","predicted"])
    w.writerows((r["id"],int(y),int(p)) for r,y,p in zip(valid_rows,y_valid,prediction))
print("저장 완료. 다음 순서: python restore.py")
