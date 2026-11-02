import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
OUT.mkdir(exist_ok=True)

from torch.nn.utils.rnn import pad_sequence
sequences=[torch.ones(4,3),torch.ones(2,3)*2,torch.ones(5,3)*3]
lengths=torch.tensor([4,2,5]); padded=pad_sequence(sequences,batch_first=True) # 형상: [3, 5, 3]

mask=torch.arange(padded.size(1)).unsqueeze(0)>=lengths.unsqueeze(1)
"""
torch.arange(padded.size(1)) -> tensor([0, 1, 2, 3, 4]) (시점 인덱스)
.unsqueeze(0) -> 형상 (1, 5)
lengths.unsqueeze(1) -> 형상 (3, 1):

tensor([[4],
        [2],
        [5]])
"""
# TODO A01: Padding이 아닌 실제 시점만 합산하고 각 자료의 실제 길이로 나눈다.
# mask=True는 Padding이다. 0도 정상 관측값일 수 있으므로 값이 0인지로 판정하지 않는다.
mean = padded.sum(dim = 1) / lengths.unsqueeze(1)

print("Padding mask:\n",mask)
print("실제 값 평균:\n",mean)
pd.DataFrame(mask.int().numpy()).to_csv(OUT/"padding_mask.csv",index=False)

"""
왜 마스크(Mask)가 필요한가?

앞서 pad_sequence로 빈자리를 0으로 채웠습니다:

2번째 샘플(원래 길이 2)은 뒤에 3개의 0이 붙어 총 5개의 시점을 갖습니다:
[2, 2, 0, 0, 0]

만약 단순하게 padded.mean(dim=1)(단순 시간축 평균)을 취하면:
실제 값의 평균인 (2 + 2) / 2 = 2.0이 나오는 것이 아니라,
패딩된 0까지 포함되어 (2 + 2 + 0 + 0 + 0) / 5 = 0.8이라는 왜곡된 수치가 계산됩니다.

또한 실제 관측치 중에도 우연히 0이 존재할 수 있으므로, 
padded == 0으로 패딩 여부를 판단하면 안 되고
반드시 원래 길이(lengths)를 바탕으로 불리언 마스크(mask)를 만들어 처리해야 합니다.
"""