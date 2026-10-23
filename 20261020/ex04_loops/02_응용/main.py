# -*- coding: utf-8 -*-
# 2026-10-20 Day 2 | 실습 04 | 응용
# 평균 80점 이상 수강생 번호 매기기 | PPT 45쪽
# 실행: python main.py (이 파일이 있는 폴더에서)
# 입력·완료 기준·예상 결과: 같은 폴더의 README.md, sample_input.txt, expected_output.txt
# 수강생용: TODO 부분을 완성한다. 제공된 입출력 형식과 함수 이름은 유지한다.
# NotImplementedError는 미완성 위치를 알리는 표식이다. 해당 줄을 실제 구현으로 교체한다.

students = {
    "민지": [82, 95, 76, 88],
    "준호": [70, 75, 65],
    "서연": [80, 80],
    "지후": [60, 95, 95],
    "하늘": [],
}
qualified = []

# TODO 01: Dict를 순회해 빈 List를 건너뛰고 평균 80 이상인 (이름, 평균)을 qualified에 추가하세요.
for name,score in students.items():
  if not score:
    continue

  average = sum(score)/len(score)
  if average >= 80:
    qualified.append((name,average))

# TODO 02: enumerate(..., start=1)로 선별된 수강생에게 연속 번호를 붙이세요.
for number, i in enumerate(qualified, start = 1):
  print(number, i)

