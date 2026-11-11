"""
실습 04: YOLO 모델 1 에포크 학습 파이프라인 연결 점검
사전학습 가중치 없이 모델 아키텍처(YAML)를 생성하고 1 에포크 학습을 호출합니다.
학습이 정상적으로 연결되는지 확인하는 용도입니다.
"""
from pathlib import Path
import yaml
import torch
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent
# Windows에서도 읽기 worker가 스크립트를 재실행하지 않도록 진입점을 구분합니다.
if __name__ == "__main__":
    torch.set_num_threads(1)
    config = {"train": str(BASE / "data/images/train"), "val": str(BASE / "data/images/val"),
              "names": ["square", "circle", "triangle"]}
    config_path = BASE / "p04_dataset.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    model = YOLO("yolo26n.yaml")  # 구조만 생성합니다. COCO 사전학습 .pt와 다릅니다.
    # >>> B05
    # 1 에포크, 이미지 크기 160, 배치 4, CPU 환경으로 학습을 수행합니다.
    model.train(data=str(config_path), epochs=1, imgsz=160, batch=4, device="cpu", project=str(BASE / "p04_runs"), name="smoke", workers=0, seed=14)
    # <<< B05
    print("task:", model.task, "names:", model.names, "device:", model.device)
    print("학습 결과:", BASE / "p04_runs/smoke")
