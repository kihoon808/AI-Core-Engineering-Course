
"""
AI 모델의 엣지 디바이스 배포 파이프라인(PyTorch -> ONNX -> TensorRT)을 설계합니다.
프레임워크 간 변환, 중간 검증, 타깃 하드웨어 전용 최적화 엔진 빌드 단계를 순서대로 정리합니다.
실제 변환을 수행하지 않고 아키텍처 설계를 JSON으로 기록하는 단계입니다.
"""

from pathlib import Path
import json

base = Path(__file__).resolve().parent

# ============================================================
# TODO B07: AI 모델 배포 파이프라인 단계 정의
# ============================================================
# 모델 준비부터 ONNX 변환/검증, 대상 장비 엔진 빌드, 런타임 추론 검증 단계를 순서대로 정의합니다.
stages = [
    'PyTorch model',
    'ONNX export and verify',
    'TensorRT build on target',
    'Runtime inference and verify'
]
# TODO 끝 B07

# 설계 정보 저장 (실제 실행 결과가 아님)
plan = {
    'stages': stages,
    'status': 'DESIGN_ONLY',
    'target_device': None,
    'tensorrt_version': None,
    'engine_sha256': None,
    'latency_ms': None,
    'checked_on_hardware': False
}

# 배포 설계 결과를 JSON 파일로 저장
(base / 'p06_deployment_plan.json').write_text(
    json.dumps(plan, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

# 배포 단계를 순서대로 출력
print(' -> '.join(stages))

print(
    'DESIGN_ONLY: 오늘은 설계 기록. '
    'Tesseract 자체를 ONNX로 변환하는 예제가 아닙니다.'
)
