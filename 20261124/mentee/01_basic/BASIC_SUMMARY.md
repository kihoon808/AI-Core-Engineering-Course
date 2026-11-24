# basic 실습 요약 및 학습 정리 노트 (Day 27)

기본 RAG 파이프라인에 실패 진단, Query Rewrite, Multi-Query, 후보 검색 확장, Cross-Encoder Reranking을 결합하고, 전·후 비교와 FastAPI 서비스 통합까지 완성하는 Enhanced RAG 8단계 핵심 패턴 정리입니다.

---

## 1. 실습별 핵심 요약

| 실습 | 주제 | 핵심 내용 |
| :--- | :--- | :--- |
| **01** | 실패 진단 (`01_failure_diagnosis`) | RAG 실패를 검색 실패(누락·순위 하락)와 생성 실패(근거 무시·환각)로 분리 진단하고 개선 지점을 식별 |
| **02** | Query Rewrite (`02_query_rewrite`) | 대화 이력(`history`)을 반영해 지시어·생략된 문맥을 복원하고, 단독 검색 가능한 명확한 질의로 재작성 |
| **03** | Multi-Query (`03_multi_query`) | 단일 질의를 다각도의 검색 질의로 확장해 다양한 표현·키워드를 포괄하는 검색 재현율(Recall) 확보 |
| **04** | 후보 검색 (`04_candidate_retrieval`) | Reranking 전 단계에서 충분한 후보(`candidate_k`)를 확보하고, 중복 제거·카테고리/권한 필터 경계를 유지 |
| **05** | Cross-Encoder Reranking (`05_cross_encoder_reranking`) | 1차 검색 후보를 Cross-Encoder(GPU 추론)로 정밀 재정렬하여 상위 `context_k` 문서의 정밀도(Precision) 향상 |
| **06** | LangChain 파이프라인 (`06_langchain_pipeline`) | Rewrite → Retrieve → Rerank → Context → Generation·Validation 단계를 단일 LangChain `Runnable` 체인으로 통합 |
| **07** | 전·후 비교 (`07_before_after`) | Baseline RAG와 Enhanced RAG(Rewrite + Rerank 적용)의 검색 순위 및 응답 품질을 동일 조건에서 정량·정성 비교 |
| **08** | Enhanced RAG FastAPI (`08_enhanced_rag_api`) | 완성된 Enhanced RAG 체인을 FastAPI 엔드포인트(`/api/v1/rag/answer`)로 감싸고, 서버 측 `learner` 역할 고정 및 200·422·502 상태 코드 계약 구현 |

---

## 2. 기억해야 할 5가지 핵심 원칙

1. **검색 실패와 생성 실패를 분리해서 진단한다**
   - 답변이 틀렸을 때 검색 단계에서 정답 문서가 누락된 것인지(`Retrieval Failure`), 문서는 찾았으나 LLM이 잘못 해석한 것인지(`Generation Failure`) 구분해야 올바른 개선 수단(Rewrite/Rerank vs 프롬프트/모델)을 선택할 수 있습니다.

2. **`--offline` 고정 Fixture 결과와 실제 모델 실측을 절대 혼동하지 않는다**
   - `--offline` 모드는 외부 API·GPU·DB 없이 파이프라인 연결과 HTTP 오류 계약(200·422·502)을 검증하기 위한 교육용 고정 데이터이므로, 이를 실제 모델 성능 지표로 보고해서는 안 됩니다.

3. **Reranking은 충분한 후보군(`candidate_k`)과 GPU 추론을 전제로 동작한다**
   - 1차 검색에서 `candidate_k`를 넉넉히 확보한 뒤 Cross-Encoder로 재정렬해 `context_k`를 추려야 효과가 있으며, Cross-Encoder는 의도하지 않은 CPU fallback 없이 실제 GPU 환경에서 실행해야 합니다.

4. **API 요청의 권한(`role`) 문자열은 절대 신뢰하지 않는다**
   - 공개 요청 스키마(`RagRequest`)에서 사용자 입력으로 `role`을 받지 않고, 서버 측 인증/미들웨어 계층에서 검증된 역할(`trusted_role='learner'`)을 주입해야 권한 우회를 원천 차단할 수 있습니다.

5. **단위 단계 오류는 숨기지 않고 명확한 HTTP 상태 코드로 분리한다**
   - 입력 파라미터 검증 실패(`candidate_k=0` 등)는 체인 실행 전에 `422`로 차단하고, 파이프라인 내부 단계 실패(`StageError`)는 `502`와 함께 실패 단계(`stage`)·원인 코드(`code`)를 명시해 관측 가능성(Observability)을 확보합니다.
