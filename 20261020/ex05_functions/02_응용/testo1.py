def is_valid_score(score):
    """입력 계약: score는 int 또는 float인 점수이며 bool·문자열은 입력하지 않는다."""
    # TODO 01: 점수가 0~100 범위인지 bool로 반환하세요.
    if score == int or float:
        if score<=100 and score>=0:
            return bool

print(is_valid_score(100), is_valid_score(-100))
