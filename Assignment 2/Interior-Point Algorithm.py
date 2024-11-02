import numpy as np
from numpy.linalg import norm
from numpy.typing import NDArray


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


def simplex(c: NDArray, A: NDArray, b: NDArray, eps: float):
    decision_vars = int(c.nonzero()[0][-1]) + 1
    if (A[:,-A.shape[0]:] != np.eye(A.shape[0])).any() \
        or A.shape[1] - A.shape[0] != decision_vars:
        raise Exception("cannot find basic variables")
    def argmin_mask(a: NDArray, mask: NDArray):
        masked = a[mask]
        if masked.size == 0:
            return -1
        masked_min = masked.argmin()
        return int(np.arange(a.size)[mask.flatten()][masked_min])
    z = np.append(c * (-1), [0])
    table = np.c_[A, b]
    basics = list([decision_vars + i for i in range(A.shape[0])])
    while (z[:-1] < 0 - eps).any():
        enters = argmin_mask(z[:-1], (z[:-1] < 0 - eps))
        ratio = np.divide(table[:,-1], table[:,enters],
                          out=np.zeros_like(table[:,-1]),
                          where=table[:,enters] != 0)
        leaves = argmin_mask(ratio, ratio > 0 + eps)
        if leaves == -1:
            raise Exception("Unbounded")
        basics[leaves] = enters
        table[leaves,:] = table[leaves,:] / table[leaves,enters]
        z -= table[leaves,:] * z[enters]
        for i in range(table.shape[0]):
            if (i == leaves):
                continue
            table[i,:] -= table[leaves,:] * table[i,enters]
    x = np.zeros((decision_vars))
    for row, basic in enumerate(basics):
        if basic < decision_vars:
            x[basic] = table[row,-1]
    return x, z[-1]

for n in range(1, 6):
    data = open(f"tests/input{n}.txt", "r").readlines()

    c = np.array([float(j) for j in data[0].split()], float)
    A = np.array([[float(j) for j in row.split()] for row in data[1:-3]], float)
    x = np.array([float(j) for j in data[-3].split()], float)
    b = np.array([float(j) for j in data[-2].split()], float)
    eps = float(data[-1])
    rounding = len(data[-1]) - 2

    print(f"Input №{n}")
    print()

    try:
        print("Interior-point Algorithm:")
        print("alpha = 0.5:")
        result = interior_point_algorithm(c, A, x, eps, 0.5)
        print(f"\tx = {np.round(result[0], decimals=rounding)}")
        print(f"\tMaximum value f(x) = {np.round(result[1], decimals=rounding)}")
    except Exception:
        print("The method is not applicable!")

    try:
        print("alpha = 0.9:")
        result = interior_point_algorithm(c, A, x, eps, 0.9)
        print(f"\tx = {np.round(result[0], decimals=rounding)}")
        print(f"\tMaximum value f(x) = {np.round(result[1], decimals=rounding)}")
    except Exception:
        print("The method is not applicable!")

    try:
        print()
        print("Simplex Method:")
        result = simplex(c, A, b, eps)
        print(f"\tx = {np.round(result[0], decimals=rounding)}")
        print(f"\tMaximum value f(x) = {np.round(result[1], decimals=rounding)}")
    except Exception:
        print("The method is not applicable!")

    print("\n")
