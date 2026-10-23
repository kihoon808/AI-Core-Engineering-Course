import numpy as np

list_a = [[1,2,3],[4,5,6],[7,8,9]]
a = np.asarray(list_a, dtype = float)
col, row = np.asarray(a, dtype=float), np.asarray(a, dtype=float)
print(f"a = {a}", f"col = {col}", f"row = {row}")  
print(f"a.shape = {a.shape}", f"col.shape = {col.shape}", f"row.shape = {row.shape}")
