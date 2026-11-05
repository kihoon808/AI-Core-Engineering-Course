"""Day14: 제공된 정상 이미지로 학습합니다. test는 읽지 않습니다."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
from torch import nn
from torchvision.datasets import ImageFolder
from torchvision import transforms as tr
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

torch.set_num_threads(1)
torch.manual_seed(14)
BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE

# 여기서는 [0,1] RGB 32×32로 학습한 교육용 source 가중치를 사용합니다.
# ImageNet ResNet18과 입력 변환을 섞지 않습니다.
# 이미지 해상도를 32x32로 조정하고, [0, 255] 정수 픽셀을 [0.0, 1.0] 범위의 3채널 Float32 텐서([3, 32, 32])로 변환합니다.
transform = tr.Compose([tr.Resize((32, 32)), tr.ToTensor()])
import cv2
#폴더명(circle, square, triangle)을 알파벳 순으로 인덱싱(0, 1, 2)하여 데이터셋을 구성합니다.
train = ImageFolder(DATA / "train", transform=transform)
valid = ImageFolder(DATA / "valid", transform=transform)
# 전체 데이터를 단일 배치 텐서로 메모리에 한 번에 적재하여 학습 루프를 고속화합니다.
X_train = torch.stack([train[i][0] for i in range(len(train))])
y_train = torch.tensor(train.targets, dtype=torch.long)
X_valid = torch.stack([valid[i][0] for i in range(len(valid))])
y_valid = torch.tensor(valid.targets, dtype=torch.long)
# 제공 부분: 0~8은 Backbone, 9는 새 3클래스 Head입니다.
model = nn.Sequential(
    nn.Conv2d(3, 8, 3, padding=1, bias=False), nn.BatchNorm2d(8), nn.ReLU(), nn.MaxPool2d(2), # Conv(3->8), BN, ReLU, MaxPool -> 32x32 이미지가 16x16으로 다운샘플링.
    nn.Conv2d(8, 16, 3, padding=1, bias=False), nn.BatchNorm2d(16), nn.ReLU(), # Conv(8->16), BN, ReLU -> 16채널 특징 맵 유지.
    nn.AdaptiveAvgPool2d((4, 4)), nn.Flatten(), nn.Linear(256, 3), # 공간 해상도를 4x4로 강제 풀링, 16채널 * 4 * 4 = 256 차원 1D 벡터로 평탄화, 최종 3개 클래스 로짓을 도출하는 분류기(Head).
)
# 안전한 수치 배열만 읽습니다. Target 이미지로 사전학습한 파일이 아닙니다.
with np.load(DATA / "source_backbone.npz", allow_pickle=False) as saved:
    state = model.state_dict()
    state.update({name: torch.from_numpy(saved[name].copy()) for name in saved.files})
model.load_state_dict(state)
# requires_grad는 가중치 갱신, eval()은 BatchNorm 통계 사용 방식을 제어합니다.
for p in model.parameters():
    p.requires_grad = False
for p in model[9].parameters(): #9번 레이어만 기울기 계산을 허용합니다.
    p.requires_grad = True
model.eval()  # 배치 정규화의 running_mean과 running_var가 소량 데이터로 인해 오염되는 것을 차단하고 사전학습 통계치를 그대로 보존합니다.
optimizer = torch.optim.AdamW(model[9].parameters(), lr=0.01, weight_decay=0.0)
criterion = nn.CrossEntropyLoss()

history = []
best_loss = float("inf")
for epoch in range(1, 9):
    optimizer.zero_grad()
    loss = criterion(model(X_train), y_train)
    # TODO B07: 역전파와 Optimizer 갱신을 수행하세요.
    loss.backward() #기울기 계산
    optimizer.step() #가중치 갱신

    #매 에포크 검증 손실(valid_loss)을 측정하고, 가장 손실이 낮았던 시점의 모델 상태를 딥카피(detach().clone())해 둡니다.
    with torch.no_grad():
        valid_loss = criterion(model(X_valid), y_valid).item()
    history.append({"epoch": epoch, "valid_loss": valid_loss})
    if valid_loss < best_loss:
        best_loss = valid_loss
        best_epoch = epoch
        best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
model.load_state_dict(best_state)
with torch.no_grad():
    logits = model(X_valid)
    probabilities = logits.softmax(1)
    # TODO B08: 각 행의 가장 큰 logit 열을 예측 라벨로 고르세요.
    predictions = logits.argmax(dim=1)  # 클래스 인덱스를 예측합니다.

metrics = {"accuracy": accuracy_score(y_valid, predictions), "macro_f1": f1_score(y_valid, predictions, labels=[0,1,2], average="macro", zero_division=0), "best_epoch": best_epoch, "valid_n": len(valid), "source": "synthetic_source_pretraining", "test_used": False}
pd.DataFrame([metrics]).to_csv(OUT / "metrics.csv", index=False)
pd.DataFrame(history).to_csv(OUT / "history.csv", index=False)
pd.DataFrame({"file": [Path(p).name for p,_ in valid.samples], "actual": y_valid.numpy(), "predicted": predictions.numpy(), "confidence": probabilities.max(1).values.numpy()}).to_csv(OUT / "predictions.csv", index=False)
# TODO B09: metrics를 UTF-8 JSON 문자열로 저장하세요. 아래 제공된 경로를 사용합니다.
(OUT / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8") # metrics.json 파일에 JSON 포맷으로 지표를 기록합니다.

pd.DataFrame(confusion_matrix(y_valid, predictions, labels=[0,1,2]), index=valid.classes, columns=valid.classes).to_csv(OUT / "confusion.csv")

# 이전 실행 흔적을 청소하고, 예측 실패 샘플을 최대 8개까지 디스크에 이미지로 저장합니다.
# 본 모델은 검증 정확도 100%를 달성하므로 errors는 빈 리스트가 되며, 어떠한 오류 파일도 인위적으로 생성하지 않습니다.
for old in OUT.glob("project_error_*.png"):
    old.unlink()
errors = (predictions != y_valid).nonzero().flatten().tolist()
for i in errors[:8]:
    image = (X_valid[i].permute(1,2,0).numpy()*255).astype(np.uint8)
    cv2.imwrite(str(OUT / f"project_error_{i:02d}.png"), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

# === Hook 없는 Grad-CAM 시각화 엔진 ===
# hook 대신 Sequential을 둘로 나눕니다. 관심 클래스의 logit을 미분합니다.
index = errors[0] if errors else 0
image = X_valid[index:index + 1].clone().requires_grad_(True)
#메모리 누수와 구현 복잡도가 높은 Hook 등록 대신, (features, 16채널 16x16)를 기준으로 모델을 물리적으로 나누어 실행합니다.
features = model[:7](image)
logits_one = model[7:](features)
target = int(logits_one.argmax(1).item())
# 예측 타깃 클래스의 로짓 스칼라에 대해 features 텐서의 기울기를 직접 역전파 미분합니다.
gradient = torch.autograd.grad(logits_one[0, target], features)[0]
weights = gradient.mean(dim=(2, 3), keepdim=True)
# 채널 가중 합산 후 ReLU로 타깃 클래스에 긍정적인 영향을 준 영역만 남깁니다.
# 쌍선형 보간(bilinear)으로 원본 32x32 크기로 복원하고 최대값으로 나누어 [0, 1] 범위로 정규화합니다.
cam = (weights * features).sum(dim=1).relu()
cam = torch.nn.functional.interpolate(cam.unsqueeze(1), size=(32, 32), mode="bilinear", align_corners=False)[0, 0]
cam = cam.detach().numpy()
cam = cam / max(float(cam.max()), 1e-8)  # 양의 반응이 없으면 0 지도를 유지
rgb = (X_valid[index].permute(1, 2, 0).numpy() * 255).astype(np.uint8)
#고주파 반응 구역을 붉은색 히트맵으로 렌더링하고, 원본 이미지와 6:4 비율로 합성(cv2.addWeighted)하여 256x256 크기의 project_cam.png로 최종 보관합니다.
heat_bgr = cv2.applyColorMap(np.uint8(cam * 255), cv2.COLORMAP_JET)
overlay = cv2.addWeighted(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), 0.6, heat_bgr, 0.4, 0)

# 상위 호환 대안: cv2.imencode 메모리 버퍼 인코딩 후 파일 저장
success, encoded_img = cv2.imencode(".png", cv2.resize(overlay, (256, 256)))
if success:
    (OUT / "project_cam.png").write_bytes(encoded_img.tobytes())
    
print(json.dumps(metrics,ensure_ascii=False,sort_keys=True))
print("오답 수:",len(errors),"예측 행:",len(valid),"test 사용: False")

"""
전이학습(Transfer Learning) 파이프라인의 전 과정(모델 학습, 최적 체크포인트 복원, 다각도 성능 평가, 메트릭/예측값 영구 저장, Grad-CAM 설명가능성 시각화)을 하나로 통합한 최종 프로젝트 엔드투엔드 파이프라인
"""