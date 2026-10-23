T = int(input())
for test_case in range(1, T + 1):
    num = input("").strip().split()
    num = list(map(int, num))
    sum = 0
    for i in num:
        if i<0 or i>10000:
            continue
        elif i % 2 != 0:
            sum += i
    print(f"#{test_case} {sum}")