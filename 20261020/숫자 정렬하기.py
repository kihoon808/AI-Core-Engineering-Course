T = int(input(""))
count = 1
while count <= T:
  a = input("")
  a = a.strip().split()
  a = list(map(int, a))

  if len(a)<5:
    continue

  a.sort()
  print(f"#{count}", *a)
  count += 1
  