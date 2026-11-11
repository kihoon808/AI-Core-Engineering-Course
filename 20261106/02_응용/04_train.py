"""
실습 04: YOLO 모델 학습 API 및 동일 CLI 설정 동기화
2 에포크 동안 고정된 하이퍼파라미터(SGD, lr=0.01, seed=42)로 학습을 진행합니다.
파이썬 API 설정과 일치하는 CLI 명령어를 텍스트 파일로 함께 기록합니다.
"""
from pathlib import Path
import yaml
import torch
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent
if __name__ == "__main__":
    torch.set_num_threads(1)
    out = BASE / "outputs"; out.mkdir(exist_ok=True)
    config = {"train": str(BASE / "data/images/train"), "val": str(BASE / "data/images/val"), "names": ["square", "circle", "triangle"]}
    path = out / "dataset_active.yaml"; path.write_text(yaml.safe_dump(config), encoding="utf-8")
    model = YOLO("yolo26n.yaml")
    # >>> A04
    # 동일한 하이퍼파라미터 조건으로 2 에포크 학습을 수행합니다.
    model.train(data=str(path), epochs=2, imgsz=160, batch=4, workers=0, device="cpu", amp=False, pretrained=False, optimizer="SGD", lr0=0.01, seed=42, plots=False, project=str(out), name="smoke", exist_ok=True)
    # <<< A04
    command = f'yolo detect train model=yolo26n.yaml data="{path}" epochs=2 imgsz=160 batch=4 workers=0 device=cpu amp=False pretrained=False optimizer=SGD lr0=0.01 seed=42 plots=False project="{out}" name=cli_smoke exist_ok=True'
    (out / "same_settings_cli.txt").write_text(command, encoding="utf-8")
    print("best/last:", out / "smoke/weights", "CLI 비교는 선택 실행입니다.")
