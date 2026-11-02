T = int(input())
for test_case in range(1, T + 1):
    #a = input("".split(""))
    """
    W는 사용량
    P는 a회사 수도요금
    Q는 b회사의 R리터 이하일때 요금
    R은 b회사의 기준점
    S는 b회사의 R리터 이상일때 초과요금
    """
    P, Q, R, S, W = map(int, input().split()) 
    
    a_cost = W * P #a회사의 수도요금
    b_cost = Q if W<=R else Q+ S*(W-R) #b회사의 수도요금

    #더 적은 회사의 요금을 출력
    if a_cost<b_cost:
        print(f"#{test_case} {a_cost}")
    else:
        print(f"#{test_case} {b_cost}")

"""
b회사의 요금이 R보다 작을 때 리터당 Q를 받는줄 착각해서 좀 오래걸림.
"""

