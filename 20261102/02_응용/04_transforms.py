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

from PIL import Image, ImageDraw

#data/train/horizontal 디렉터리에 있는 PNG 파일 중 첫 번째 이미지를 찾아 PIL 라이브러리로 열고 표준 RGB 3채널 포맷으로 변환합니다.
path = sorted((root / "data" / "train" / "horizontal").glob("*.png"))[0]
image = Image.open(path).convert("RGB")

# 좌우반전은 가로·세로 줄무늬 라벨을 보존한다. 90도 회전은 라벨을 바꾸므로 사용하지 않는다.
train_transform = transforms.Compose([
    transforms.Resize((64, 64)), #이미지 크기를 64x64로 조정합니다.
    transforms.RandomHorizontalFlip(), #이미지를 좌우 반전합니다.
    transforms.RandomRotation(10), #이미지를 10도 이내로 랜덤하게 회전시킵니다.
    transforms.ColorJitter(brightness=0.15), #이미지의 밝기를 15% 이내로 랜덤하게 조정합니다.
    transforms.ToTensor(),
])

# TODO A04: valid에는 Resize와 ToTensor만 적용한다.
valid_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

augmented = [train_transform(image) for _ in range(3)]
v1, v2 = valid_transform(image), valid_transform(image)
canvas = Image.new("RGB", (4*128, 150), "white")
draw = ImageDraw.Draw(canvas)
for i, tensor in enumerate([v1]+augmented):
    canvas.paste(transforms.ToPILImage()(tensor).resize((128,128)), (128*i,22))
    draw.text((128*i+5,4), "valid" if i==0 else f"train {i}", fill="black")
canvas.save(out / "augmentation_preview.png")

print("valid 동일:", torch.equal(v1, v2))
print("shape:", tuple(v1.shape))
print("train 3개 동일 여부:", torch.equal(augmented[0], augmented[1]))
