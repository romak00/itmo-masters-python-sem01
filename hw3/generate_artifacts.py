import os
import numpy as np
from matrix_lib import Matrix, MatrixND

OUT_DIR = "hw3/artifacts"
os.makedirs(OUT_DIR, exist_ok=True)

np.random.seed(0)
A_arr = np.random.randint(0, 10, (10, 10))
B_arr = np.random.randint(0, 10, (10, 10))

A = Matrix(A_arr)
B = Matrix(B_arr)

(A + B).to_file(os.path.join(OUT_DIR, "matrix+.txt"))
(A * B).to_file(os.path.join(OUT_DIR, "matrix*.txt"))
(A @ B).to_file(os.path.join(OUT_DIR, "matrix@.txt"))

print("Task 1 artifacts:",
      os.path.join(OUT_DIR, "matrix+.txt"),
      os.path.join(OUT_DIR, "matrix*.txt"),
      os.path.join(OUT_DIR, "matrix@.txt"))


np.random.seed(0)
A_nd = MatrixND(A_arr)
B_nd = MatrixND(B_arr)

(A_nd + B_nd).to_file(os.path.join(OUT_DIR, "matrix_nd+.txt"))
(A_nd * B_nd).to_file(os.path.join(OUT_DIR, "matrix_nd*.txt"))
(A_nd @ B_nd).to_file(os.path.join(OUT_DIR, "matrix_nd@.txt"))

print("Task 2 artifacts:",
      os.path.join(OUT_DIR, "matrix_nd+.txt"),
      os.path.join(OUT_DIR, "matrix_nd*.txt"),
      os.path.join(OUT_DIR, "matrix_nd@.txt"))


A3 = Matrix(np.zeros((3, 3), dtype=int))
C3 = Matrix([[9, 8, 0], [0, 0, 0], [0, 0, 0]])
B3 = Matrix(np.eye(3, dtype=int))
D3 = Matrix(np.eye(3, dtype=int))

AB_true = (A3._data @ B3._data)
CD_true = (C3._data @ D3._data)

A3.to_file(os.path.join(OUT_DIR, "A.txt"))
B3.to_file(os.path.join(OUT_DIR, "B.txt"))
C3.to_file(os.path.join(OUT_DIR, "C.txt"))
D3.to_file(os.path.join(OUT_DIR, "D.txt"))

Matrix.from_numpy(AB_true).to_file(os.path.join(OUT_DIR, "AB.txt"))
Matrix.from_numpy(CD_true).to_file(os.path.join(OUT_DIR, "CD.txt"))

h_AB = hash(Matrix.from_numpy(AB_true))
h_CD = hash(Matrix.from_numpy(CD_true))
with open(os.path.join(OUT_DIR, "hash.txt"), "w", encoding="utf-8") as f:
    f.write(f"hash(AB) = {h_AB}\n")
    f.write(f"hash(CD) = {h_CD}\n")

print("Task 3 artifacts:",
      os.path.join(OUT_DIR, "A.txt"),
      os.path.join(OUT_DIR, "B.txt"),
      os.path.join(OUT_DIR, "C.txt"),
      os.path.join(OUT_DIR, "D.txt"),
      os.path.join(OUT_DIR, "AB.txt"),
      os.path.join(OUT_DIR, "CD.txt"),
      os.path.join(OUT_DIR, "hash.txt"))

print("hash(A) =", hash(A3), "hash(C) =", hash(C3), "A == C?", np.array_equal(A3._data, C3._data))