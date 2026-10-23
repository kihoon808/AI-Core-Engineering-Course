set_a = (1, 2, 3, 4, 5)
set_b = (4, 5, 6, 7, 8)

set_common = set(set_a) & set(set_b)
set_all = set(set_a) | set(set_b)
set_only_a = set(set_a) - set(set_b)
set_only_b = set(set_b) - set(set_a)

print(f'''공통 요소: {sorted(set_common)}\n전체 요소: {sorted(set_all)}\nA만의 요소: {sorted(set_only_a)}\nB만의 요소: {sorted(set_only_b)}''')
