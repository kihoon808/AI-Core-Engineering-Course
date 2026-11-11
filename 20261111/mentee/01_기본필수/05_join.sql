-- Day18 | 실습 05: JOIN·분류별 집계 | PPT 35~41, 74 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E5_GUARD expect=00000 capture=- reconnect=false
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

-- @step E5_JOIN expect=00000 capture=- reconnect=false
-- BEGIN TASK B05_01
-- TODO B05_01: 분류 PK와 지식 FK를 맞춰 분류명을 붙이세요. 결과 한 행은 지식 한 건이며 S0는 3행입니다.
-- 1. [두 표 합치기: JOIN(INNER)]
-- 지식 표에는 카테고리 번호(1, 2)만 있고 글자 이름이 없습니다.
-- "지식 표(k)의 category_id와 카테고리 표(c)의 id가 일치하는 것끼리 옆으로 이어붙여서, 지식 제목 옆에 카테고리 이름까지 예쁘게 붙여서 보여줘"라는 뜻입니다.
SELECT k.id, k.title, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON c.id = k.category_id
ORDER BY k.id;
-- END TASK B05_01

-- @step E5_GROUP expect=00000 capture=- reconnect=false
-- BEGIN TASK B05_02
-- TODO B05_02: 분류를 왼쪽에 두고 분류별 실제 지식 수를 세세요. 빈 reference 분류는 0이어야 합니다.
-- 2. [카테고리별 지식 개수 세기: LEFT JOIN + GROUP BY]
-- "카테고리 표(c)를 기준으로 삼고, 카테고리별로 묶어서(GROUP BY) 지식이 몇 개씩 연결되어 있는지 세어줘"라는 뜻입니다.
-- 왜 LEFT JOIN일까요? 일반 JOIN을 쓰면 지식이 아직 0개인 'reference' 카테고리가 결과에서 사라져 버리므로, 빈 카테고리도 빠짐없이 보여주기 위해 씁니다.
-- 왜 COUNT(k.id)일까요? COUNT(*)를 쓰면 빈 카테고리도 1개로 잘못 세어지지만, COUNT(k.id)는 비어있는(NULL) 지식을 제외하므로 정확하게 0개로 세어줍니다.
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id = c.id
GROUP BY c.id, c.name
ORDER BY c.id;
-- END TASK B05_02

-- @step E5_LENGTH expect=00000 capture=- reconnect=false
-- 3. [글자 수 통계 집계]
-- 전체 지식 개수(3건)와 본문 글자 수의 총합(64자), 가장 짧은 본문(20자), 가장 긴 본문(24자)을 요약 계산합니다.
SELECT COUNT(*) AS knowledge_count,SUM(char_length(content)) AS total_chars,
MIN(char_length(content)) AS min_chars,MAX(char_length(content)) AS max_chars FROM public.knowledge;
