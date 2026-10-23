# -*- coding: utf-8 -*-
# 2026-10-20 Day 2 | 실습 04 | 기본필수
# 1부터 N까지 누적하기 | PPT 45쪽
# 실행: python main.py (이 파일이 있는 폴더에서)
# 입력·완료 기준·예상 결과: 같은 폴더의 README.md, sample_input.txt, expected_output.txt
# 수강생용: TODO 부분을 완성한다. 제공된 입출력 형식과 함수 이름은 유지한다.
# NotImplementedError는 미완성 위치를 알리는 표식이다. 해당 줄을 실제 구현으로 교체한다.

n = int(input("N(0 이상의 정수): "))
if n < 0:
    print("N은 0 이상이어야 합니다.")
else:
    total = 0
    even_total = 0
    # TODO 01: for·range를 사용해 전체 합과 짝수 합을 각각 누적하세요. sum()이나 공식으로 대체하지 마세요.
    for i in range(0, n+1):
        if i % 2 == 0:
            even_total += i
        total += i
    print(f"전체 합: {total}")
    print(f"짝수 합: {even_total}")
