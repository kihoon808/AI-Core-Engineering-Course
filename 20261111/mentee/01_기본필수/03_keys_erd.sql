-- Day18 | 실습 03: 두 테이블·키·ERD | PPT 21~28, 69~70, 73 | 30분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E3_GUARD expect=00000 capture=- reconnect=false
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

-- @step E3_BEGIN expect=00000 capture=- reconnect=false
-- 1. "지금부터 하는 작업은 연습장에 적어두고, 확정하기 전까지는 임시로만 취급해줘"라는 뜻입니다.
BEGIN;

-- @step E3_CREATE expect=00000 capture=- reconnect=false
CREATE TABLE public.categories_try (
-- BEGIN TASK B03_01
-- TODO B03_01: 연습용 분류의 id를 행 식별 키로 선언하세요. IDENTITY 자동 발급은 이 축소 예제에서 사용하지 않습니다.
-- 2. 기본키(PRIMARY KEY): 주민등록번호처럼 한 줄을 유일하게 식별하는 번호입니다. 중복될 수 없고 비어있을 수 없습니다.
id INTEGER PRIMARY KEY,
-- END TASK B03_01
name TEXT NOT NULL
);
CREATE TABLE public.knowledge_try (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
-- BEGIN TASK B03_02
-- TODO B03_02: category_id가 categories_try.id를 참조하게 하세요. 자식이 부모를 가리키는 방향입니다.
-- 3. 외래키(REFERENCES): 부모 표에 없는 번호(예: 999번)를 자식 표에 마음대로 적지 못하게 단단히 연결해 두는 고리입니다.
category_id INTEGER NOT NULL
  REFERENCES public.categories_try(id)
-- END TASK B03_02
);

-- @step E3_SEED expect=00000 capture=- reconnect=false
-- 4. 부모 표(categories_try)에 1번 '연습'을 먼저 넣고, 자식 표(knowledge_try)에서 1번 카테고리를 참조하는 지식을 넣습니다.
INSERT INTO public.categories_try VALUES (1,'연습');
INSERT INTO public.knowledge_try VALUES (1,'안내',1);

-- @step E3_READ expect=00000 capture=- reconnect=false
-- 5. 임시로 만든 지식 표에 데이터가 잘 들어갔는지 조회해 봅니다.
SELECT * FROM public.knowledge_try ORDER BY id;

-- @step E3_CANCEL expect=00000 capture=- reconnect=false
-- 6. "방금 했던 연습 작업 전부 없던 일로 취소(Ctrl + Z)해줘!" 하고 원상 복구합니다.
ROLLBACK;

-- @step E3_GONE expect=00000 capture=- reconnect=false
-- 7. 방금 만든 임시 표들이 깔끔하게 사라졌는지 확인합니다. 결과가 둘 다 true(참)로 나와야 합니다.
SELECT to_regclass('public.categories_try') IS NULL AS parent_gone,
       to_regclass('public.knowledge_try') IS NULL AS child_gone;
