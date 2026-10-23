raw = input("명령> ")
parts = raw.strip().split(maxsplit=1)
command = parts[0].lower()
value = parts.remove("add")

print(command)
print(parts)
print(value)

