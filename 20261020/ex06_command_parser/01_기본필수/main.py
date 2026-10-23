# -*- coding: utf-8 -*-
# 2026-10-20 Day 2 | 실습 06 | 기본필수
# add·list·quit 명령 루프 | PPT 61쪽
# 실행: python main.py (이 파일이 있는 폴더에서)
# 입력·완료 기준·예상 결과: 같은 폴더의 README.md, sample_input.txt, expected_output.txt
# 수강생용: TODO 부분을 완성한다. 제공된 입출력 형식과 함수 이름은 유지한다.
# NotImplementedError는 미완성 위치를 알리는 표식이다. 해당 줄을 실제 구현으로 교체한다.

def main():
    items = []
    while True:
        raw = input("명령> ")
        # TODO 01: 명령만 소문자로 표준화하고 명령 뒤의 전체 문자열을 value로 추출하세요.
        parts = raw.strip().split(maxsplit=1)
        if not parts:
            print("명령을 입력하세요.")
            continue
        command = parts[0].lower()  # TODO: 대소문자를 표준화하세요.
        parts
        if command == "quit":
            if value:
                print("quit에는 인수를 붙이지 않습니다.")
                continue
            print("종료합니다.")
            break
        elif command == "add":
            # TODO 02: 빈 값은 거부하고 유효 항목만 저장하세요.
            for i in parts:
                total_list.append(i)
            print("추가되었습니다.")
        elif command == "list":
            # TODO 03: list의 불필요한 인수를 거부하고 전체 항목을 번호와 함께 출력하세요.
            count = 0
            for i in total_list:
                print(f"{count}: {i} ")
                count += 1

        else:
            print("알 수 없는 명령입니다.")


if __name__ == "__main__":
    main()
