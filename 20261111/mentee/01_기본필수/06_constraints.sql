-- Day18 | 실습 06: 제약조건·실패·회복 | PPT 42~47 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E6_GUARD expect=00000 capture=- reconnect=false
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

-- @step E6_BEFORE expect=00000 capture=- reconnect=false
-- 1. [시작 전 확인] 제약조건 실험을 하기 전에, 현재 지식 3건과 카테고리 3건이 정상적으로 있는지 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;

-- @step E6_PARENT expect=00000 capture=- reconnect=false
-- 카테고리 표(1, 2, 3)를 확인하고, -1번 카테고리는 실제로 없다는 것(0 rows)을 확인합니다.
SELECT id,name FROM public.categories ORDER BY id;
SELECT id FROM public.categories WHERE id=-1;

-- @step E6_CHECK_BEGIN expect=00000 capture=- reconnect=false
-- 2. 첫 번째 고의 실패 실험을 임시 트랜잭션으로 시작합니다.
BEGIN;

-- @step E6_BAD_CONTENT expect=23514 capture=- reconnect=false
-- [실험 1: 본문 길이 제약조건(CHECK) 위반 테스트]
-- 본문(content)을 빈 문자열('')로 등록하려고 시도합니다.
-- DB 반응: "본문은 최소 1자 이상 2000자 이하여야 합니다!"라며 체크 제약조건 위반 에러(23514)를 발생시키고 저장을 거부합니다.
INSERT INTO public.knowledge(title,content,category_id) VALUES ('오류 확인','',1);

-- @step E6_CHECK_CANCEL expect=00000 capture=- reconnect=false
-- BEGIN TASK B06_01
-- TODO B06_01: 앞의 빈 본문 INSERT가 CHECK 오류로 거부된 뒤 이 구간만 따로 실행해 미확정 거래를 취소하세요.
-- [에러 후 정리: ROLLBACK]
-- 중요: PostgreSQL은 트랜잭션 안에서 한 번이라도 에러가 발생하면, 취소(ROLLBACK)하기 전까지 이후 모든 쿼리를 거부합니다.
-- 따라서 에러가 발생한 뒤에는 반드시 ROLLBACK을 실행해 안전하게 원상태로 빠져나와야 합니다.
ROLLBACK;
-- END TASK B06_01

-- @step E6_FK_BEGIN expect=00000 capture=- reconnect=false
-- 3. 두 번째 고의 실패 실험을 임시 트랜잭션으로 시작합니다.
BEGIN;

-- @step E6_BAD_FK expect=23503 capture=- reconnect=false
-- [실험 2: 존재하지 않는 카테고리 외래키(FK) 위반 테스트]
-- category_id에 존재하지 않는 번호인 -1을 넣고 등록하려고 시도합니다.
-- DB 반응: "카테고리 표(categories)에 -1번은 존재하지 않습니다!"라며 외래키 위반 에러(23503)를 내뿜고 저장을 차단합니다.
INSERT INTO public.knowledge(title,content,category_id) VALUES ('오류 확인','정상 본문',-1);

-- @step E6_FK_CANCEL expect=00000 capture=- reconnect=false
-- [에러 후 정리: ROLLBACK]
-- 실패한 트랜잭션을 롤백하여 깨끗하게 취소합니다.
ROLLBACK;

-- @step E6_AFTER expect=00000 capture=- reconnect=false
-- 4. [최종 확인] 두 번의 고의적인 에러 실험 후에도, 기존 데이터(지식 3건, 카테고리 3건)가 일절 오염되지 않고 그대로 살아있는지 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT id,name FROM public.categories ORDER BY id;
