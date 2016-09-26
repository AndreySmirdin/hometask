import numpy as np
import sys


def read_matrix(m, n):
    m[:n, :n] = np.loadtxt(sys.stdin)
    return m


def add_zeros(size):
    m = np.zeros((size, size), dtype=int)
    return m


def mult(m1, m2):
    if m1.shape[0] == 1:
        return m1 * m2
    a_up, a_down = np.hsplit(m1, 2)
    a11, a21 = np.vsplit(a_up, 2)
    a12, a22 = np.vsplit(a_down, 2)
    b_up, b_down = np.hsplit(m2, 2)
    b11, b21 = np.vsplit(b_up, 2)
    b12, b22 = np.vsplit(b_down, 2)
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
    for i in ans:
        print(' '.join(map(str, i)))

n = int(input())
size = 1
while size < n:
    size *= 2
m1 = read_matrix(add_zeros(size), n)
m2 = read_matrix(add_zeros(size), n)
ans = mult(m1, m2)
print_ans(ans[:n, :n])
