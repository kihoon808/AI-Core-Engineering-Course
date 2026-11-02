"""실습 04 · 필요한 하위 폴더는 ImageFolder의 이미지 저장 구조뿐이다."""
from pathlib import Path
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

root = Path(__file__).resolve().parent
# Resize(size)는 목표 크기가 필수. ToTensor()에는 필수 인자가 없다.
#transforms.Compose: 여러 전처리 단계를 순서대로 연결하는 컨테이너입니다.
transform = transforms.Compose([
    transforms.Resize((32, 32)), #원본 이미지 크기와 관계없이 가로 32, 세로 32 픽셀로 강제 리사이징합니다.
    transforms.ToTensor() 
    #0에서 255 범위의 정수 픽셀(PIL Image)을 0.0에서 1.0 사이의 32비트 실수 텐서로 변환합니다.
    #이미지의 차원 축을 (높이 H, 너비 W, 채널 C)에서 PyTorch 표준 포맷인 (채널 C, 높이 H, 너비 W) 형태로 자동 재배열합니다.
])
# ImageFolder(root, transform=None): root는 필수, transform은 선택이다.
# TODO B04: data/train을 주어진 transform으로 읽는다.
train = datasets.ImageFolder(root / "data" / "train", transform=transform)

loader = DataLoader(train, batch_size=4, shuffle=False, num_workers=0)
images, labels = next(iter(loader))
print("학습 이미지:", len(train))
print("클래스:", train.class_to_idx)
print("배치:", tuple(images.shape), tuple(labels.shape))
print("라벨:", labels.tolist())
