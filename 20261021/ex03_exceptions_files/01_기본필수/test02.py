T = int(input())
for test_case in range(1, T + 1):
    rep = int(input(""))#명령어의 개수
    
    speed = 0
    total_distance = 0

    for i in range(rep):
        #첫번째 숫자: 명령어 입력. 0은 속도 유지 1은 가속 2는 감속 
        #두번째 숫자: 가속력 또는 감속력
        numbers = list(map(int, input().split()))
        c1 = numbers[0]
        c2 = numbers[1]

        if c1 == 1:
            speed += c2
        elif c1 == 2:
            speed = max(0, speed - c2)
        elif c1 == 0:
            speed = speed

        total_distance += speed
        
    print(f"#{test_case} {total_distance}")

    

