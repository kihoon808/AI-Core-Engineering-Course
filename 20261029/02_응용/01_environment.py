"""실습 01: CUDA가 있으면 사용하고 없으면 CPU로 진행합니다."""
from pathlib import Path
import torch

out = Path(__file__).resolve().parent / "outputs"
out.mkdir(exist_ok=True)
# TODO A01: 위 요구사항을 읽고 이 블록을 완성하세요.
if torch.cuda.is_available():
    device = torch.device("cuda:0") # CUDA가 사용 가능하면 cuda:0으로 설정
else:
    device = torch.device("cpu") # CUDA가 사용 불가능하면 cpu로 설정

x = torch.tensor([1., 2.]).to(device)
info = {"torch": str(torch.__version__), "cuda_build": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(), "selected_device": str(device)}
if device.type == "cuda":
    info["gpu_name"] = torch.cuda.get_device_name(device)
    info["vram_gib"] = round(torch.cuda.get_device_properties(device).total_memory / 1024**3, 2)
for key, value in info.items():
    print(f"{key}: {value}")
print("연산:", (x + 1).cpu().tolist())
(out / "gpu_check.txt").write_text("\n".join(f"{k}: {v}" for k, v in info.items()), encoding="utf-8")
