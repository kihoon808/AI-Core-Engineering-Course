-- Day18 | 실습 07: 취소·확정·인덱스·실행계획 | PPT 48~54, 76 | 30분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E7_GUARD expect=00000 capture=- reconnect=false
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

-- @step E7_BEFORE expect=00000 capture=- reconnect=false
-- 1. [변경 전 원래 본문 확인]
-- 수정을 시작하기 전에, 2번 지식의 현재 원래 본문이 무엇인지 확인합니다.
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_CANCEL_BEGIN expect=00000 capture=- reconnect=false
-- 2. 임시 수정을 위해 트랜잭션을 시작합니다.
BEGIN;

-- @step E7_TEMP expect=00000 capture=- reconnect=false
-- 2번 지식의 본문을 '취소할 임시 안내입니다.'로 일단 바꿔봅니다.
UPDATE public.knowledge SET content='취소할 임시 안내입니다.' WHERE id=2 RETURNING id,content;

-- @step E7_CANCEL expect=00000 capture=- reconnect=false
-- BEGIN TASK B07_01
-- TODO B07_01: 임시 본문 수정을 확정하지 않고 취소하는 명령을 넣으세요. 다음 SELECT에서 시작 본문이 보여야 합니다.
-- 3. [취소: ROLLBACK]
-- "방금 했던 수정 작업은 테스트였으니 취소(Ctrl + Z)해줘!" 하고 원래대로 되돌립니다.
ROLLBACK;
-- END TASK B07_01

-- @step E7_CANCEL_READ expect=00000 capture=- reconnect=false
-- 4. [취소 확인] 2번 지식이 원래 본문('프로젝트 폴더에서 서버를 실행합니다.')으로 안전하게 되돌아왔는지 확인합니다.
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_SAVE_BEGIN expect=00000 capture=- reconnect=false
-- 5. 이번에는 진짜로 영구 저장할 수정을 시작합니다.
BEGIN;

-- @step E7_SAVE expect=00000 capture=- reconnect=false
-- 2번 지식의 본문을 '실행 전에 가상환경을 확인합니다.'로 변경합니다.
UPDATE public.knowledge SET content='실행 전에 가상환경을 확인합니다.' WHERE id=2 RETURNING id,content;

-- @step E7_COMMIT expect=00000 capture=- reconnect=false
-- BEGIN TASK B07_02
-- TODO B07_02: 가상환경 확인 안내를 확정하세요. 이 명령 후 새 연결에서 조회해도 같은 본문이 나와야 합니다.
-- 6. [확정: COMMIT]
-- "이 수정 내용은 최종 확정이야! 하드디스크에 영구적으로 안전하게 저장해줘!" 하고 확정 도장을 찍습니다.
COMMIT;
-- END TASK B07_02

-- @step E7_RECONNECT expect=00000 capture=- reconnect=true
-- 7. [영구 반영 확인] 다른 연결(세션)에서 보더라도 방금 COMMIT된 내용이 영구적으로 남아있는지 확인합니다.
SELECT current_database() AS database_name;
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_INDEX_INSPECT expect=00000 capture=- reconnect=false
-- 8. [현재 인덱스 목록 확인]
-- 인덱스(Index)는 책 맨 뒤의 '색인(찾아보기)' 같은 것입니다. 현재 어떤 인덱스가 있는지 확인합니다.
SELECT indexname,indexdef FROM pg_indexes WHERE schemaname='public' AND tablename='knowledge' ORDER BY indexname;

-- @step E7_PLAN_BEFORE expect=00000 capture=- reconnect=false
-- 9. [실행 계획: EXPLAIN]
-- DB 엔진에게 "너 카테고리 1번 찾을 때 어떤 방법으로 찾아갈 거야?" 하고 내부 계획서를 미리 물어봅니다.
EXPLAIN SELECT id,title FROM public.knowledge WHERE category_id=1;

-- @step E7_INDEX_CREATE expect=00000 capture=- reconnect=false
-- 10. [인덱스 생성: CREATE INDEX]
-- 카테고리 번호(category_id)로 지식을 검색할 때 초고속으로 찾을 수 있도록 전용 색인(목차)을 만듭니다.
CREATE INDEX idx_knowledge_category_id ON public.knowledge(category_id);

-- @step E7_PLAN_AFTER expect=00000 capture=- reconnect=false
-- 11. [인덱스 생성 후 계획 및 실제 시간 측정: EXPLAIN ANALYZE]
-- 실제 쿼리를 돌려보며 어떻게 찾았는지 분석합니다. (데이터가 3건으로 너무 적을 때는 목차를 뒤지는 것보다 처음부터 읽는 Seq Scan이 더 빠르므로 DB가 알아서 최적화합니다.)
EXPLAIN (ANALYZE, BUFFERS) SELECT id,title FROM public.knowledge WHERE category_id=1;

-- @step E7_FINAL expect=00000 capture=- reconnect=false
-- 12. [최종 상태 확인: S1 상태]
-- 1, 3번 지식은 그대로이고, 2번 지식만 가상환경 확인 문구로 영구 갱신된 최종 상태를 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
