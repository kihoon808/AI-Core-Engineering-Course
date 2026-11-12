-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_b' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_b, got %', current_database();
    END IF;
END;
$guard$;
-- 파일 전체 실행 금지: 조회는 CASE 단위, 변경은 BEGIN → DML RETURNING → 종료문 → SELECT를 각각 선택합니다.
-- __NEW_ID__는 C01 RETURNING으로 받은 실제 정수로 치환합니다. 구현 TODO와 다릅니다.

-- CASE R01
-- BEGIN B-SQL-01
-- [설명 B-SQL-01]: 초기 S0 상태에서 knowledge 테이블의 id와 title 열을 id 오름차순(ORDER BY)으로 정렬하여 조회합니다.
SELECT id, title FROM public.knowledge
ORDER BY id;
-- END B-SQL-01
-- ENDCASE R01

-- CASE R02
-- BEGIN B-SQL-02
-- [설명 B-SQL-02]: ID가 2인 항목의 id, title, content, category_id 열을 WHERE 절 조건을 통해 조회합니다.
SELECT id, title, content, category_id
FROM public.knowledge
WHERE id = 2;
-- END B-SQL-02
-- ENDCASE R02

-- CASE R03
-- BEGIN B-SQL-03
-- [설명 B-SQL-03]: knowledge와 categories 테이블을 외래키(category_id = c.id)로 연결하여 각 지식의 id, title, 분류명(category)을 id 오름차순으로 조회합니다.
SELECT k.id, k.title, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON c.id = k.category_id
ORDER BY k.id;
-- END B-SQL-03
-- ENDCASE R03

-- CASE R04
-- BEGIN B-SQL-04
-- [설명 B-SQL-04]: categories를 기준(LEFT JOIN)으로 각 카테고리별 지식 개수를 집계합니다. 지식이 없는 reference 분류의 경우 COUNT(k.id)는 NULL을 제외하므로 0이 반환됩니다.
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id = c.id
GROUP BY c.id, c.name ORDER BY c.id;
-- END B-SQL-04
-- ENDCASE R04

-- CASE C01
-- 1. BEGIN만 선택하여 실행합니다.
BEGIN;
-- 2. 아래 INSERT ... RETURNING만 실행하고 실제 ID를 기록합니다.
-- BEGIN B-SQL-05
-- [설명 B-SQL-05]: 주어진 제목, 본문, 카테고리 ID(1)로 새로운 지식 행을 INSERT하고, 생성된 id와 입력값을 RETURNING으로 반환받습니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('보충 학습','복습 자료는 개인 폴더에서 확인합니다.',1)
RETURNING id,title,category_id;
-- END B-SQL-05
-- 3. COMMIT만 실행한 뒤 다음 SELECT를 따로 실행합니다.
COMMIT;
SELECT COUNT(*) AS knowledge_count FROM public.knowledge;
-- ENDCASE C01

-- CASE U01
BEGIN;
-- BEGIN B-SQL-06
-- [설명 B-SQL-06]: C01에서 생성된 행(__NEW_ID__)의 본문을 UPDATE하고 RETURNING으로 확인합니다. 뒤의 ROLLBACK을 통해 수정이 취소되고 원문이 유지됩니다.
UPDATE public.knowledge SET content='복습 자료와 예제 코드를 함께 확인합니다.'
WHERE id=__NEW_ID__ RETURNING id,content;
-- END B-SQL-06
ROLLBACK;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U01

-- CASE U02
BEGIN;
-- BEGIN B-SQL-07
-- [설명 B-SQL-07]: C01에서 생성된 행(__NEW_ID__)에 동일한 본문 수정을 실행하고 COMMIT하여 변경 내용을 영구 확정합니다.
UPDATE public.knowledge SET content='복습 자료와 예제 코드를 함께 확인합니다.'
WHERE id=__NEW_ID__ RETURNING id,content;
-- END B-SQL-07
COMMIT;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U02

-- CASE D01
BEGIN;
-- BEGIN B-SQL-08
-- [설명 B-SQL-08]: C01에서 생성된 행(__NEW_ID__)을 DELETE하고 삭제된 id를 RETURNING합니다. COMMIT 후 원래 지식 3건만 남게 됩니다.
DELETE FROM public.knowledge WHERE id=__NEW_ID__ RETURNING id;
-- END B-SQL-08
COMMIT;
SELECT id FROM public.knowledge WHERE id=__NEW_ID__;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE D01
