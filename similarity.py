import numpy as np

def cosine_similarity(A, B):
    # 1. Cek jumlah elemen A dan B sama
    if len(A) != len(B):
        print("Panjang vektor A dan B harus sama.")
        return None
    # 2. Validasi tipe setiap elemen A dan B
    for a, b in zip(A, B):
        if type (a) not in [int, float] or type(b) not in [int, float]:
            print("Semua elemen vektor harus berupa angka (int atau float).")
            return None
    # 3. Hitung dot product
    dot = 0
    for a, b in zip(A, B):
        dot = np.dot(A, B)
    # 4. Hitung panjang A dan B
    length_A = np.sqrt(np.dot(A, A))
    length_B = np.sqrt(np.dot(B, B))
    # 5. Tolak kalau salah satu panjang bernilai nol
    if length_A == 0 or length_B == 0:
        print("Salah satu vektor adalah vektor nol.")
        return None
    # 6. Hitung similarity
    similarity = dot / (length_A * length_B)

    return similarity


case1 = cosine_similarity([1, 2, 3], [1, 2, 3])
case2 = cosine_similarity([2, 0], [0, 4])
case3 = cosine_similarity([1, 2, 0], [3, 5])
print(case1)
print(case2)
print(case3)