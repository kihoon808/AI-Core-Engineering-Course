BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_b' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_b, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.categories (
    -- BEGIN B-DDL-01
    -- [설명 B-DDL-01]: GENERATED ALWAYS AS IDENTITY로 자동 증가 시퀀스를 생성하고 PRIMARY KEY로 고유성과 NOT NULL을 부여합니다.
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- END B-DDL-01
    name VARCHAR(30) NOT NULL UNIQUE,
    -- BEGIN B-DDL-02
    -- [설명 B-DDL-02]: char_length() 함수를 사용하여 카테고리 이름의 길이가 1자 이상 30자 이하인지 검사합니다.
    CONSTRAINT categories_name_length CHECK (char_length(name) BETWEEN 1 AND 30)
    -- END B-DDL-02
);
CREATE TABLE public.knowledge (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    content TEXT NOT NULL,
    category_id BIGINT NOT NULL,
    -- BEGIN B-DDL-03
    -- [설명 B-DDL-03]: title(1~80자)과 content(1~2000자)의 문자열 길이를 char_length()로 검증하는 제약조건입니다.
    CONSTRAINT knowledge_title_length CHECK (char_length(title) BETWEEN 1 AND 80),
    CONSTRAINT knowledge_content_length CHECK (char_length(content) BETWEEN 1 AND 2000),
    -- END B-DDL-03
    CONSTRAINT knowledge_category_fk FOREIGN KEY (category_id)
        -- BEGIN B-DDL-04
        -- [설명 B-DDL-04]: public.categories(id)를 외래키로 참조하며, 자식 데이터가 존재하는 부모 카테고리 삭제를 방지하기 위해 ON DELETE RESTRICT를 적용합니다.
        REFERENCES public.categories(id) ON DELETE RESTRICT
        -- END B-DDL-04
);
COMMIT;
