
"""
TensorRT 10.x 환경에서 ONNX 모델을 엔진 파일(.plan)로 빌드하기 위한 CLI 명령어를 설계합니다.
동적 배치(Dynamic Shape: 1, 4, 8) 및 FP16 반정밀도 가속 옵션을 trtexec 인자로 구성합니다.
버전 호환성(TRT 10.x의 --fp16과 TRT 11.x의 변경점)을 주석 및 매니페스트로 명시합니다.
"""

from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
import cv2

base = Path(__file__).resolve().parent
data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)

lesson = json.loads(
    (data / 'lesson.json').read_text(encoding='utf-8')
)

# ============================================================
# 1. TensorRT 엔진 생성 설정
# ============================================================
manifest = {
    'status': 'DESIGN_ONLY',
    'tensorrt_major': 10,
    'input_name': 'images',
    'dtype': 'float32',
    'min': [1, 3, 224, 224],
    'opt': [4, 3, 224, 224],
    'max': [8, 3, 224, 224],
    'hardware_verified': False,
    'engine_sha256': None
}

# ============================================================
# TODO A06: TensorRT 10.x용 trtexec 명령어 구성
# ============================================================
# TensorRT 10.x trtexec 명령 도구에 전달할 변환 인자(ONNX 경로, 저장 경로, 동적 크기, FP16)를 정의합니다.
command = [
    'trtexec',
    '--onnx=model.onnx',
    '--saveEngine=model.plan',
    '--minShapes=images:1x3x224x224',
    '--optShapes=images:4x3x224x224',
    '--maxShapes=images:8x3x224x224',
    '--fp16'
]
# TODO 끝 A06


# ============================================================
# 2. TensorRT 버전별 주의사항 기록
# ============================================================

# TensorRT 10.x를 기준으로 작성한 명령어 저장
manifest['example_for_trt10_only'] = command

# TensorRT 11.x의 정밀도 옵션 차이 기록
manifest['trt11_note'] = (
    '11.x는 --fp16 제거. '
    'ONNX 정밀도 변환을 사전에 하고 설치 버전의 help를 확인.'
)


# ============================================================
# 3. 엔진 생성 설계 정보 JSON 저장
# ============================================================

# 실제 엔진이 아니라 생성 명령어와 설정만 저장
(out / 'p06_engine_manifest.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

# 작성한 명령어를 문자열로 연결하여 출력
print('설계만:', ' '.join(command))

# TensorRT 11.x 관련 주의사항 출력
print(manifest['trt11_note'])
