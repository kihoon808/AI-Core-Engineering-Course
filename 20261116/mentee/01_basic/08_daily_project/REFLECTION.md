# 결과를 읽은 뒤 짧게 설명

- 사용한 A/B·Context·Schema 버전: bundle=frozen_bundle.json (BASE_RULE vs BASE_RULE+ADDED_RULE), Context=knowledge_v1, Schema=answer_schema_v1 (strict=True, extra="forbid")
- 실제 실행 / 미실행 / 사람 평가 대기 수: 계획 N=6 (A: 3, B: 3), 실행 0, 미실행 6, 사람 평가 대기 6 (미실행/미평가 상태를 0점이나 오류로 왜곡하지 않고 분모 6 유지)
- 줄어든 오류 또는 차이를 확인하지 못한 항목: 형식 오류(JSON 파싱, Pydantic 검증) 및 컨텍스트 외 ID 참조 차단 흐름은 fixture로 검증 완료했으나, 실제 LLM 추론 환경에서의 A/B 승률 및 응답 차이는 미실행으로 인해 미확인
- 새로 생긴 오류·과도한 정보 부족 응답: 오프라인 파이프라인 검증 상 추가 오류는 없으며, 실제 모델의 과도한 거절(Over-abstain) 여부는 사람 검토 슬롯(human_review.json)에서 관찰 필요
- 다음에 바꿀 요소 하나와 예상 효과(가설): 컨텍스트 윈도우 토큰 예산 내에서 Few-shot 예제 1건(정상/부족 균형)을 추가하여 JSON 스키마 준수율을 유지하면서도 모델의 지시문 이해도를 높인다.
- fixture로 확인한 것과 아직 실제 모델에서 확인하지 못한 것: fixture를 통해 4단계 검증(문법/스키마/참조/규칙)과 Bounded Retry(최대 2회, 2·2·1·1 호출 분기)의 제어 무결성을 확인했으나, 실제 모델의 사실성(Grounding) 및 환각 여부는 검증되지 않음.

예상값을 실제 관찰란에 복사하지 않습니다. 이 문서는 길게 작성하는 보고서가 아니라 결과 설명 메모입니다.
