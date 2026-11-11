-- Day18 | 실습 08: 나만의 AI 도움말 지식 DB | PPT 58~67 | 40분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E8_GUARD expect=00000 capture=- reconnect=false
-- 제공된 안전 확인입니다. 이 블록은 TODO가 아닙니다.
-- 개인 수업용 DB에서만 실행합니다. 이름만 맞다고 운영 DB가 안전해지는 것은 아닙니다.
DO $guard$
BEGIN
  IF current_database() !~ '^knowledge_lab(_[a-z0-9_]+)?$' THEN
    RAISE EXCEPTION '개인 knowledge_lab DB에 다시 접속하세요. 현재 DB: %', current_database();
  END IF;
END;
$guard$;
SET search_path TO public;
-- 이 파일은 앞서 사용한 DB를 이어 씁니다. prepare_S0.sql을 다시 실행하지 않습니다.
-- 시작 N과 기존 전체 지식을 reports/daily_note.md에 기록/내보내기 합니다.
-- A·B·C 생성은 각각 1번만 실행합니다. 실수로 중복 생성하면 실제 ID를 확인하고 강사와 정리하세요.
-- __A_ID__, __B_ID__, __C_ID__는 실제 RETURNING 값으로 모두 바꾼 뒤 사용합니다.
-- 기본필수도 자신의 주제에 맞게 세 제목·본문을 작성합니다. 제공 예문은 가상 예시입니다.

-- @step D8_BASELINE expect=00000 capture=- reconnect=false
SELECT current_database() AS database_name;
SELECT COUNT(*) AS baseline_n FROM public.knowledge;
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT id,name FROM public.categories ORDER BY id;

-- @step D8_CREATE_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_CREATE_A expect=00000 capture=a_ reconnect=false
-- BEGIN TASK B08_01
-- TODO B08_01: 사용자·주제를 정한 뒤 A를 INSERT하세요.
-- 1. [지식 A 생성] "끝까지 안전하게 유지할 첫 번째 지식(가상환경 관리)을 1번 카테고리(learning)에 등록하고, 발급된 실제 번호(id)를 확인합니다."
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('가상환경 관리', '프로젝트별 독립된 가상환경을 활성화하여 종속성을 격리합니다.', 1)
RETURNING id,title,content,category_id;
-- END TASK B08_01

-- @step D8_CREATE_B expect=00000 capture=b_ reconnect=false
-- 2. [지식 B 생성] "나중에 본문 내용을 수정(UPDATE)할 두 번째 지식을 2번 카테고리(environment)에 등록합니다."
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('실습 결과 기록', '가상의 결과는 개인 폴더에 남깁니다.', 2)
RETURNING id,title,content,category_id;

-- @step D8_CREATE_C expect=00000 capture=c_ reconnect=false
-- 3. [지식 C 생성] "나중에 삭제(DELETE) 테스트로 지워볼 세 번째 지식을 1번 카테고리(learning)에 등록합니다."
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('폐기할 임시 안내', '가상의 임시 안내는 확인 후 제거합니다.', 1)
RETURNING id,title,content,category_id;

-- @step D8_CREATE_COMMIT expect=00000 capture=- reconnect=false
-- 4. [A, B, C 생성 확정] 세 지식을 하드디스크에 영구히 저장합니다.
COMMIT;

-- @step D8_LIST expect=00000 capture=- reconnect=false
SELECT k.id, k.title, k.content, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON c.id = k.category_id
ORDER BY k.id;

SELECT COUNT(*) AS after_create_count FROM public.knowledge;

-- @step D8_B_ORIGINAL expect=00000 capture=- reconnect=false
-- 5. [수정 전 지식 B 원문 확인]
-- 수정을 시작하기 전에, 9번(B) 지식의 원래 본문 내용을 먼저 확인합니다.
SELECT id,title,content,category_id FROM public.knowledge WHERE id=9;

-- @step D8_B_CANCEL_BEGIN expect=00000 capture=- reconnect=false
-- 6. 임시 수정을 위해 트랜잭션을 시작합니다.
BEGIN;

-- @step D8_B_TEMP expect=00000 capture=- reconnect=false
-- 9번(B) 지식의 본문을 '취소할 임시 프로젝트 본문입니다.'로 일단 바꿔봅니다.
UPDATE public.knowledge SET content='취소할 임시 프로젝트 본문입니다.' WHERE id=9 RETURNING id,content;

-- @step D8_B_CANCEL expect=00000 capture=- reconnect=false
-- 7. [수정 취소: ROLLBACK]
-- "방금 했던 수정은 테스트였으니 취소(Ctrl + Z)해줘!" 하고 롤백합니다.
ROLLBACK;

-- @step D8_B_RESTORED expect=00000 capture=- reconnect=false
-- 8. [취소 확인] 9번(B) 지식의 본문이 원래대로 잘 복구되었는지 확인합니다.
SELECT id,content FROM public.knowledge WHERE id=9;

-- @step D8_B_SAVE_BEGIN expect=00000 capture=- reconnect=false
-- 9. 이번에는 진짜 영구 반영할 수정을 시작합니다.
BEGIN;

-- @step D8_B_SAVE expect=00000 capture=- reconnect=false
-- 9번(B) 지식의 본문을 '결과에는 실행 명령과 실제 SQL 결과를 함께 적습니다.'로 수정합니다.
UPDATE public.knowledge SET content='결과에는 실행 명령과 실제 SQL 결과를 함께 적습니다.'
WHERE id=9 RETURNING id,content;

-- @step D8_B_COMMIT expect=00000 capture=- reconnect=false
-- BEGIN TASK B08_02
-- TODO B08_02: 앞서 ROLLBACK한 B를 다시 수정한 뒤 이번에는 확정하세요.
-- 10. [수정 확정: COMMIT]
-- "수정된 새 본문을 디스크에 영구적으로 확실하게 저장해줘!" 하고 확정합니다.
COMMIT;
-- END TASK B08_02

-- @step D8_B_RECONNECT expect=00000 capture=- reconnect=true
-- 11. [영구 반영 확인] 다른 세션에서 조회하더라도 9번(B) 지식의 수정문이 잘 남아있는지 확인합니다.
SELECT current_database() AS database_name;
SELECT id,content FROM public.knowledge WHERE id=9;

-- @step D8_ERRORS_BEFORE expect=00000 capture=- reconnect=false
-- 12. 에러 방어 테스트 전 상태를 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT id FROM public.categories WHERE id=-1;

-- @step D8_CHECK_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_CHECK_FAIL expect=23514 capture=- reconnect=false
-- [고의 에러 1: 빈 본문 등록 차단]
-- 본문이 빈칸('')인 지식을 등록 시도하면 CHECK 제약조건(23514)에 의해 거부됩니다.
INSERT INTO public.knowledge(title,content,category_id) VALUES ('실패 확인','',1);

-- @step D8_CHECK_CANCEL expect=00000 capture=- reconnect=false
-- 에러 후 롤백으로 빠져나옵니다.
ROLLBACK;

-- @step D8_FK_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_FK_FAIL expect=23503 capture=- reconnect=false
-- [고의 에러 2: 없는 카테고리 참조 차단]
-- 존재하지 않는 -1번 카테고리로 등록 시도하면 외래키 제약조건(23503)에 의해 거부됩니다.
INSERT INTO public.knowledge(title,content,category_id) VALUES ('실패 확인','정상 본문',-1);

-- @step D8_FK_CANCEL expect=00000 capture=- reconnect=false
-- 에러 후 롤백으로 빠져나옵니다.
ROLLBACK;

-- @step D8_ERRORS_AFTER expect=00000 capture=- reconnect=false
-- 13. [에러 방어 확인] 두 번의 에러 시도 후에도 데이터가 전혀 훼손되지 않았는지 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;

-- @step D8_C_BEFORE expect=00000 capture=- reconnect=false
-- 14. 삭제하기 전에, 삭제 대상인 10번(C) 지식이 잘 있는지 확인합니다.
SELECT id,title FROM public.knowledge WHERE id=10;

-- @step D8_C_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_C_DELETE expect=00000 capture=- reconnect=false
-- BEGIN TASK B08_03
-- TODO B08_03: 실제 C ID만 조건으로 삭제하세요. 제목을 삭제 키로 사용하지 않습니다.
-- 15. [지식 C 영구 삭제: DELETE]
-- "10번(C) 지식만 표에서 깔끔하게 지워줘" 하고 삭제를 수행합니다.
DELETE FROM public.knowledge
WHERE id = 10
RETURNING id,title;
-- END TASK B08_03

-- @step D8_C_COMMIT expect=00000 capture=- reconnect=false
-- 16. [삭제 확정: COMMIT]
-- 10번 지식 삭제를 하드디스크에 영구 확정합니다.
COMMIT;

-- @step D8_FINAL_RECONNECT expect=00000 capture=- reconnect=true
-- 17. [최종 상태 확인]
-- A(8번), B(9번)는 살아있고, C(10번)는 삭제되어 0행이며, 전체 개수는 5건(시작 3건 + 신규 2건)인지 확인합니다.
SELECT current_database() AS database_name;
SELECT id,title,content,category_id FROM public.knowledge WHERE id IN (8,9) ORDER BY id;
SELECT id,title FROM public.knowledge WHERE id=10;
SELECT COUNT(*) AS final_count FROM public.knowledge;

-- @step D8_GROUP expect=00000 capture=- reconnect=false
-- BEGIN TASK B08_04
-- TODO B08_04: 최종 분류별 실제 지식 수를 세세요. 합계는 현재 knowledge 총 행 수와 같아야 합니다.
-- 18. [분류별 지식 수 최종 통계]
-- 카테고리별로 몇 개씩 남았는지 세어봅니다 (learning 3개, environment 2개, reference 0개 = 총 5개).
SELECT c.name, COUNT(k.id) AS knowledge_count
FROM public.categories c
LEFT JOIN public.knowledge k ON k.category_id=c.id
GROUP BY c.id,c.name ORDER BY c.id;
-- END TASK B08_04

-- @step D8_EXISTING expect=00000 capture=- reconnect=false
-- 19. [초기 지식 보존 검증]
-- 프로젝트 시작 전에 있던 원래 1, 2, 3번 지식이 하나도 다치지 않고 온전히 보존되어 있는지 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
