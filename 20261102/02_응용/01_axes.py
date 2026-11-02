from pathlib import Path
import copy
import csv
import json
import time
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import pandas as pd

torch.manual_seed(42)
torch.set_num_threads(1)
root = Path(__file__).resolve().parent
out = root / "outputs"
out.mkdir(exist_ok=True)

import matplotlib
matplotlib.use("Agg") # "Agg" 백엔드는 그래프를 파일로 저장할 때 사용합니다.
import matplotlib.pyplot as plt
from PIL import Image

path = sorted((root / "data" / "train" / "horizontal").glob("*.png"))[0]
chw = transforms.ToTensor()(Image.open(path).convert("RGB"))
# BEGIN A01
# TODO A01: 채널 축을 마지막으로 보내 HWC를 만든다.
hwc = chw.permute(1, 2, 0) # (C, H, W) -> (H, W, C)
# END A01
nchw = hwc.permute(2, 0, 1).unsqueeze(0) # (H, W, C) -> (C, H, W) -> (1, C, H, W)
plt.figure(figsize=(4, 4)) # 그래프의 크기를 설정합니다.
plt.imshow(hwc.numpy()) # HWC 이미지를 NumPy 배열로 변환하여 표시합니다.
plt.title("HWC view: horizontal stripes") # 그래프의 제목을 설정합니다.
plt.axis("off") # 축을 표시하지 않습니다.
plt.tight_layout() # 그래프 레이아웃을 조정합니다.
plt.savefig(out / "image_axes.png", dpi=120) # 그래프를 파일로 저장합니다.
plt.close()
print("CHW / HWC / NCHW:", tuple(chw.shape), tuple(hwc.shape), tuple(nchw.shape))
print("왕복 값 일치:", torch.equal(chw, nchw[0]))
