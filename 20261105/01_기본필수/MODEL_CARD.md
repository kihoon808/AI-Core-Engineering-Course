# Model Card: 기본07 소형 도형 분류

## 데이터·출처
- **class_to_idx**: `{'circle': 0, 'square': 1, 'triangle': 2}`
- **분할 개수**:
  - `train`: 총 21개 (circle 12, square 6, triangle 3 / 4:2:1 불균형)
  - `valid`: 총 9개 (클래스별 각 3개 균등)
  - `test`: 총 6개 (클래스별 각 2개 균등 / 모델 학습·선택에 미사용)
- **source 종류**: 32x32 RGB, [0, 1] 범위 합성 도형으로 사전학습된 TinyShapeCNN
- **누수 방지 정책**: test 셋은 클래스 매핑 감사 외에 일체 미사용 (`test_used: false`)

## 실험 조건
- **전략 및 후보**: Backbone 고정 + 신규 Linear Head 교체 (학습 파라미터 771개)
- **난수 시드**: `torch.manual_seed(14)` 고정
- **최적화 설정**: `AdamW(lr=0.01, weight_decay=0.0)`, `CrossEntropyLoss`
- **에포크 예산**: 총 8 에포크
- **BN 정책**: `model.eval()` 유지 (소량 배치 통계 오염 방지를 위해 사전학습 running 통계 고정)
- **데이터 공급**: 전체 메모리 단일 텐서 스택 (`torch.stack`) 풀배치 처리

## 선택 근거
- **검증 손실 추이**: 1 에포크 0.8207에서 8 에포크 0.0905로 안정적 단조 수렴 (Best Epoch: 8)
- **Macro F1**: 1.0 (100.0%)
- **클래스별 Recall**: circle 1.0, square 1.0, triangle 1.0 (소수 클래스 누락 없음)
- **정확도(Accuracy)**: 1.0 (9/9 정분류)
- **비용**: 771개 파라미터만 갱신하여 CPU 환경에서 1-2초 내 수렴 완료

## 오류와 설명
- **오답 수**: 0건 (에러 이미지 생성 생략 정책 준수)
- **관찰 (사실)**: 전수 정답이나 `square_002`(확신도 0.763)와 `triangle_002`(확신도 0.808)는 다른 샘플(0.93-0.98) 대비 소프트맥스 확신도가 상대적으로 낮음.
- **가설**: 해당 도형의 경계선 두께나 회전 각도가 결정 경계(Decision Boundary) 인근에 위치함.
- **Grad-CAM 확인**: [project_cam.png](file:///c:/Users/kihoo/OneDrive/문서/Workspace/20261105/01_기본필수/project_cam.png) 상에서 모델의 활성화 영역이 배경이 아닌 도형 중심 및 에지에 집중됨을 확인.

## 한계
- **합성 자료**: 배경 잡음, 조명 변화, 모션 블러가 없는 이상적 데이터로 실제 현업 데이터 강건성 미검증.
- **초소형 표본**: 검증 데이터가 9개에 불과하여 통계적 신뢰구간이 매우 넓음 (1개 오분류 시 정확도 11.1%p 변동).
- **Grad-CAM의 비인과성**: 히트맵은 반응 상관관계일 뿐 인과적 판별 근거(왜 해당 도형인가)를 보증하지 않음.
- **공간 해상도**: 4x4 특징 맵을 256x256으로 보간 확대한 것이므로 세밀한 픽셀 단위 분석 한계 존재.

## 재현
- **실행 명령**: `python 07_project.py`
- **실행 환경**: Python 3.11+, PyTorch (CPU), torchvision, OpenCV
- **생성 산출물 검증**:
  - `metrics.json` (`test_used: false`, `accuracy: 1.0`)
  - `metrics.csv`, `history.csv`, `predictions.csv`, `confusion.csv`
  - `project_cam.png` (256x256 오버레이 이미지 정상 저장 확인)
