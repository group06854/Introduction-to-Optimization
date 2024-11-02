import numpy as np
from numpy.linalg import norm


def interior_point_algorithm(c, A, x, eps, alpha):
    while True:
        v = x
        D = np.diag(x)

        AA = np.dot(A, D)
        cc = np.dot(D, c)

        Identity = np.eye(len(c))

        F = np.dot(AA, np.transpose(AA))
        FI = np.linalg.inv(F)
        H = np.dot(np.transpose(AA), FI)
        P = np.subtract(Identity, np.dot(H, AA))
        cp = np.dot(P, cc)
        nu = np.absolute(np.min(cp))
        y = np.add(np.ones(len(c), float), (alpha / nu) * cp)
        yy = np.dot(D, y)
        x = yy

        if norm(np.subtract(yy, v), ord=2) < eps:
            break
    max_value_f = np.dot(c, x)
    return x[:np.count_nonzero(c)], max_value_f


# def simplex(c, A, b):

for n in range(1, 6):
    data = open(f"tests/input{n}.txt", "r").readlines()

    c = np.array([float(j) for j in data[0].split()], float)
    A = np.array([[float(j) for j in row.split()] for row in data[1:-3]], float)
    x = np.array([float(j) for j in data[-3].split()], float)
    b = np.array([float(j) for j in data[-2].split()], float)
    eps = float(data[-1])
    print(f"Input №{n}")
    print()

    try:
        print("Interior-point Algorithm:")
        print("alpha = 0.5:")
        result = interior_point_algorithm(c, A, x, eps, 0.5)
        print(f"\tx = {result[0]}")
        print(f"\tMaximum value f(x) = {result[1]}")
    except Exception:
        print("The method is not applicable!")

    try:
        print("alpha = 0.9:")
        result = interior_point_algorithm(c, A, x, eps, 0.9)
        print(f"\tx = {result[0]}")
        print(f"\tMaximum value f(x) = {result[1]}")
    except Exception:
        print("The method is not applicable!")

    # try:
    #     print("Simplex Method:")
    #     result = simplex(c, A, b, eps)
    #     print(f"x = {result}")
    # except Exception:
    #     print("The method is not applicable!")
    
    print("\n")
