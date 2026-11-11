-- Day18 | 실습 01: 접속과 첫 SQL | PPT 7~13, 68, 78~80 | 30분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E1_GUARD expect=00000 capture=- reconnect=false
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

-- @step E1_PING expect=00000 capture=- reconnect=false
-- 1. "DB 서버와 내 컴퓨터가 잘 연결되었나요?" 하고 신호를 찔러보는 핑(Ping) 테스트입니다. 1이 나오면 연결 성공입니다.
SELECT 1 AS connected;

-- @step E1_DB expect=00000 capture=- reconnect=false
-- BEGIN TASK B01_01
-- TODO B01_01: 현재 연결한 DB 이름을 반환하는 함수를 넣으세요. 기대 이름은 knowledge_lab입니다.
-- 2. "내가 지금 작업 중인 데이터베이스(엑셀 파일) 이름이 뭐죠?"를 확인합니다. 엉뚱한 DB를 건드리지 않도록 knowledge_lab인지 검사합니다.
SELECT current_database() AS database_name;
-- END TASK B01_01

-- @step E1_INFO expect=00000 capture=- reconnect=false
-- 3. "현재 로그인한 계정은 누구이고, PostgreSQL 엔진 버전은 몇 번인가요?"를 확인합니다.
SELECT current_user AS user_name, version() AS server_version;

-- @step E1_ENCODING expect=00000 capture=- reconnect=false
-- 4. "한글 텍스트가 깨지지 않고 제대로 입출력되는가?"를 확인하기 위해 UTF-8 문자셋 인코딩을 검사합니다.
SHOW client_encoding;
SELECT '한글 연결 확인' AS korean_text;
