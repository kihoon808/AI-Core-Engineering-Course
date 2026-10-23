T = int(input())
for test_case in range(1, T + 1):
  num = input()
  num = list(map(int, num.strip().split()))
  for i in range(len(num)):
    if num[i] <0 or num[i]>10000:
      num.remove(num[i])

  num.remove(min(num))
  num.remove(max(num))

  total = 0
  for i in range(len(num)):
    total += num[i]
  print(f"#{test_case} {round(total / len(num))}")
