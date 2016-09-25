import numpy as np


def read_matrix(n):
    m = np.array([], dtype=int)
    for i in range(n):
        m = np.append(m, [int(j) for j in input().split()])
    return np.reshape(m, (n, n))


def add_zeroes(m, size):
    m = np.hstack((m, np.zeros((m.shape[0], size - m.shape[0]), dtype=int)))
    m = np.vstack((m, np.zeros((size - m.shape[0], size), dtype=int)))
    return m


def mult(m1, m2):
    size = m1.shape[1]
    if size == 1:
        return m1 * m2
    else:
        size = size // 2
        a11, a12 = np.hsplit(m1, 2)
        a11, a21 = np.vsplit(a11, 2)
        a12, a22 = np.vsplit(a12, 2)
        b11, b12 = np.hsplit(m2, 2)
        b11, b21 = np.vsplit(b11, 2)
        b12, b22 = np.vsplit(b12, 2)
        p1 = mult(a11 + a22, b11 + b22)
        p2 = mult(a21 + a22, b11)
        p3 = mult(a11, b12 - b22)
        p4 = mult(a22, b21 - b11)
        p5 = mult(a11 + a12, b22)
        p6 = mult(a21 - a11, b11 + b12)
        p7 = mult(a12 - a22, b21 + b22)

        c11 = p1 + p4 + p7 - p5
        c12 = p2 + p4
        c21 = p3 + p5
        c22 = p1 - p2 + p3 + p6

    return np.hstack((np.vstack((c11, c12)), np.vstack((c21, c22))))


def print_ans(ans):
    for i in range(ans.shape[0]):
        print(*[ans[i, j] for j in range(ans.shape[0])])


n = int(input())
size = 1
while size < n:
    size *= 2
m1_zeroes = add_zeroes(read_matrix(n), size)
m2_zeroes = add_zeroes(read_matrix(n), size)
ans = mult(m1_zeroes, m2_zeroes)
print_ans(ans[:n, :n])
