"""학습 한 epoch와 평가를 분리합니다. 빈 데이터·불량 자료는 이번 단계의 과제가 아닙니다."""
import torch

def train_one_epoch(model, loader, loss_fn, optimizer, device):
    model.train() #학습 모드 전환
    total, count = 0.0, 0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        # loss.backward() 후 optimizer.step()을 호출하세요.
        # 매 batch마다 초기화하고 새로운 gradient로 갱신해야 합니다.
        # >>> H07
        # TODO H07: 위 요구사항을 읽고 이 블록을 완성하세요.
        loss.backward() #역전파
        optimizer.step() #최적화
        # <<< H07
        total += loss.item() * len(yb)
        count += len(yb)
    # 마지막 작은 batch도 실제 샘플 수만큼 반영합니다.
    return total / count


def evaluate(model, X, y, loss_fn, device):
    model.eval()
    with torch.no_grad():
        logits = model(X.to(device))
        loss = loss_fn(logits, y.to(device)).item()
        # logits에서 클래스 인덱스를 구하고 CPU로 옮겨 prediction에 저장하세요.
        # 평가에서는 backward와 optimizer.step을 호출하지 않습니다.
        # >>> H08
        #모델이 출력한 로짓에서 logits.argmax(dim=1)로 가장 점수가 높은 클래스 인덱스를 추출합니다
        #평가 시 Logits에서 예측 클래스 인덱스 추출 (cpu 텐서 변환)
        prediction = logits.argmax(dim=1).cpu() 
        # <<< H08
    return loss, (prediction == y.cpu()).float().mean().item(), prediction
