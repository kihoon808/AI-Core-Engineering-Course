-- Day18 | 실습 04: SQL CRUD·RETURNING | PPT 29~34 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E4_GUARD expect=00000 capture=- reconnect=false
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

-- @step E4_BEFORE expect=00000 capture=- reconnect=false
-- 1. [조회] 본격적인 추가/수정/삭제 연습을 시작하기 전에, 현재 저장되어 있는 3건의 지식을 먼저 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;

-- @step E4_INSERT_BEGIN expect=00000 capture=- reconnect=false
-- 2. "지금부터 하는 생성 작업은 연습장에 임시로 적어둘게요" 하고 트랜잭션을 시작합니다.
BEGIN;

-- @step E4_INSERT expect=00000 capture=new_ reconnect=false
-- BEGIN TASK B04_01
-- TODO B04_01: 지식 한 건을 INSERT하고 생성 결과를 RETURNING으로 받으세요. id는 입력하지 않습니다.
-- 3. [생성: INSERT] "새 지식을 표에 등록해줘. id는 DB가 알아서 번호를 매겨주고, 등록이 끝나면 방금 만들어진 번호와 내용을 화면에 바로 보여줘(RETURNING)"라는 뜻입니다.
INSERT INTO public.knowledge (title, content, category_id)
VALUES ('임시 안내', '취소할 연습 데이터입니다.', 1)
RETURNING id, title, content, category_id;
-- END TASK B04_01

-- @step E4_INSERT_CANCEL expect=00000 capture=- reconnect=false
-- 4. [생성 취소] 방금 넣은 연습 지식을 취소(ROLLBACK)하여 원래 상태로 되돌립니다.
ROLLBACK;

-- @step E4_UPDATE_BEFORE expect=00000 capture=- reconnect=false
-- 5. 수정하기 전에, 2번 지식의 현재 원래 본문이 무엇인지 먼저 확인해 봅니다.
SELECT id,title,content FROM public.knowledge WHERE id=2;

-- @step E4_UPDATE_BEGIN expect=00000 capture=- reconnect=false
-- 6. 수정 작업도 안전하게 임시 트랜잭션으로 시작합니다.
BEGIN;

-- @step E4_UPDATE expect=00000 capture=- reconnect=false
-- BEGIN TASK B04_02
-- TODO B04_02: 지정한 지식 한 건의 content만 수정하세요. 먼저 같은 ID의 현재 행을 SELECT합니다.
-- 7. [수정: UPDATE] "id가 2번인 지식의 본문(content)만 새 내용으로 바꿔줘. 수정이 끝나면 바뀐 내용을 화면에 바로 보여줘(RETURNING)"라는 뜻입니다.
-- 주의: WHERE id = 2 조건을 빠뜨리면 표에 있는 모든 지식의 본문이 한꺼번에 덮어씌워지므로 조건이 필수입니다!
UPDATE public.knowledge
SET content = '수정 연습 안내입니다.'
WHERE id = 2
RETURNING id, title, content;
-- END TASK B04_02

-- @step E4_UPDATE_CANCEL expect=00000 capture=- reconnect=false
-- 8. [수정 취소] 방금 수정한 내용을 취소(ROLLBACK)하여 원래 본문으로 되돌립니다.
ROLLBACK;

-- @step E4_DELETE_BEFORE expect=00000 capture=- reconnect=false
-- 9. 삭제하기 전에, 3번 지식이 잘 있는지 먼저 확인합니다.
SELECT id,title,content FROM public.knowledge WHERE id=3;

-- @step E4_DELETE_BEGIN expect=00000 capture=- reconnect=false
-- 10. 삭제 작업도 안전하게 임시 트랜잭션으로 시작합니다.
BEGIN;

-- @step E4_DELETE expect=00000 capture=- reconnect=false
-- BEGIN TASK B04_03
-- TODO B04_03: 지정된 ID의 지식만 삭제하고 삭제된 id·title을 반환하세요. 표나 분류를 삭제하지 않습니다.
-- 11. [삭제: DELETE] "id가 3번인 지식 딱 1건만 표에서 지워줘. 그리고 방금 지워진 지식의 번호와 제목을 화면에 보여줘(RETURNING)"라는 뜻입니다.
DELETE FROM public.knowledge
WHERE id = 3
RETURNING id, title;
-- END TASK B04_03

-- @step E4_DELETE_CANCEL expect=00000 capture=- reconnect=false
-- 12. [삭제 취소] 삭제했던 작업을 취소(ROLLBACK)하여 지워진 3번 지식을 다시 살려냅니다.
ROLLBACK;

-- @step E4_AFTER expect=00000 capture=- reconnect=false
-- 13. [최종 확인] 모든 연습이 롤백되어 처음 시작했을 때의 3건(id 1, 2, 3)이 온전히 보존되어 있는지 확인합니다.
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
