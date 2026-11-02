import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

x = torch.randn(2,5,16)
attention = nn.MultiheadAttention(16,4,dropout=0.0,batch_first=True)
# embed_dim=16: 전체 입력/출력 특성 차원
# num_heads=4: 헤드 개수 (h=4).
# 각 헤드당 차원은 16/4=4차원씩 나누어 맡게 됩니다.
# batch_first=True: 첫 번째 축을 배치 차원으로 설정.

# TODO B05: 4개 head의 가중치를 평균내지 않고 각각 받는다.
# query/key/value에는 같은 x를 넣는다. average_attn_weights=False를 지정한다.
output, weights = attention(x,x,x,average_attn_weights=False)

print("입력:", tuple(x.shape))
print("출력:", tuple(output.shape))
print("head별 weight:", tuple(weights.shape))
print("각 행의 합:", weights[0,0].sum(dim=-1).detach().round(decimals=4))

"""
멀티헤드(Multi-head):
하나의 거대한 어텐션만 사용하는 대신, 전체 임베딩 차원을 여러 개(h개)의 하위 공간(Head)으로 쪼개어
서로 다른 관점(문법적 관계, 위치적 거리, 의미적 유사성 등)에서 어텐션을 병렬 계산한 뒤 다시 합치는 방식입니다.
"""