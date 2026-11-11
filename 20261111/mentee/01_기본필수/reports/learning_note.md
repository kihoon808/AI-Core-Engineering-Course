# 교시별 실행 기록
비밀번호는 적지 않습니다. 예상값을 실제 관찰값으로 바꿔 적지 않습니다.

| 교시 | 실행 파일/구간 | 예상 | 실제 결과·행 수·ID | 오류와 해결·설명 |
|---|---|---|---|---|
| 01 | 01_connect.sql (전체) | connected=1, DB=knowledge_lab, UTF8 인코딩 | connected 1, database_name knowledge_lab, UTF8 확인 | current_database() 함수로 접속 카탈로그 검증 완료 |
| 02 | 02_select.sql (전체) | 목록 3건, id=2 1건, category=1 2건, id=-1 0건 | S0 기준 3건, id=2 1건, id 1·3 2건, id=-1 0 rows 확인 | ORDER BY id로 결과 집합의 결정론적 정렬 보장 |
| 03 | 03_keys_erd.sql (전체) | 테이블 생성 및 1건 삽입 후 ROLLBACK 시 완전 소멸 | (1, 안내, 1) 조회 후 롤백, to_regclass NULL=t | DDL 트랜잭션 롤백 및 PK/FK 제약조건 검증 완료 |
| 04 | 04_crud.sql (전체) | INSERT 1건, UPDATE 1건, DELETE 1건 각각 롤백 후 원상복구 | INSERT(id=4), UPDATE(id=2), DELETE(id=3) 후 각각 ROLLBACK, 최종 3건 유지 | RETURNING 절을 통한 변경 직후 확인 및 트랜잭션 단위 롤백 확인 |
| 05 | 05_join.sql (전체) | JOIN 3행, 분류별 learning 2/env 1/ref 0, 글자수 64/20/24 | JOIN 3행, learning 2, environment 1, reference 0, 총 64자 확인 | LEFT JOIN과 COUNT(k.id)를 활용하여 지식 0건인 분류 보존 확인 |
| 06 | 06_constraints.sql (전체) | 빈 본문 CHECK(23514), 없는 분류 FK(23503) 거부 후 ROLLBACK | 23514(knowledge_content_length), 23503(knowledge_category_fk) 에러 및 롤백 확인 | 트랜잭션 에러 발생 시 명시적 ROLLBACK을 통한 원래 데이터 100% 보존 확인 |
| 07 | 07_transaction_index.sql (전체) | 임시 수정 ROLLBACK 후 원래값 복원, 확정 수정 COMMIT 후 영구 반영 및 인덱스 생성 | id=2 임시수정 롤백 확인, 가상환경 문구 COMMIT 영구 저장, idx_knowledge_category_id 생성 완료 | 트랜잭션 취소/확정 분리 동작 및 B-Tree 인덱스 생성과 실행 계획(EXPLAIN) 확인 |
| 08 | 08_daily_project.sql (전체) | 시작 N=3, 생성 뒤 N+3=6, B 수정 롤백/커밋, 고의에러 23514/23503 방어, C 삭제 후 최종 N+2=5 | baseline=3, create=6, B 원문복구 및 확정, 에러 방어, C 삭제(1행), 최종 5건 및 통계 일치 확인 | 7단계 지식 라이프사이클(생성-임시수정-취소-확정-에러차단-삭제-통계집계) 전 과정 무결성 검증 완료 |

S0 → S1의 변경 내용과 인덱스 생성 여부도 기록합니다.
롤백 검증은 행의 ID·내용·수를 대조합니다. 다음 ID 숫자의 불변을 요구하지 않습니다.
07 재접속 때 현재 DB와 새 연결 여부를 확인합니다. DB 서버 종료·장애 시험은 하지 않습니다.
