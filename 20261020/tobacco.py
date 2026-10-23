'''
숫자를 정렬하려면 작은게 앞으로 와야함.
1 5 3 7 9 이렇게 있으면 일단
1을 나머지 애들이랑 전부 비교함 -> 그리고 제일 작으면 첫번째로 ㄱㄱ
5를 나머지 애들이랑 전부 비교함 ->
어떤 애를 검사시킬 때 비교하는 값보다 작으면 그 값 전 인덱스로 보내고 그 전 인덱스랑 비교해서 또 작으면 그 전 인덱스로 보내고 이걸 반복하면 됨...
'''
while True:
  num = input("")
  num = num.strip().split()
  if len(num)>50 or len(num)<5:
    continue
  else:
    num_int = []
    for i in num:
      num_int.append(int(num[i]))
    new_list = []
    for i in range(len(num_int)):
      if num_int[i] < num_int[i+1] or num_int[i] == num_int[i+1]:
        continue
      elif num_int[i] > num_int[i+1]:
        im = num_int[i+1]
        num_int[i+1] = num_int[i]
        num_int[i] = im
    for i in range(len(num_int)):
      print(i, end=" ")

