import numpy as np
import sys


def read_matrix(size, real_size):
    matrix = np.zeros((size, size), dtype=int)
    matrix[:real_size, :real_size] = np.loadtxt(sys.stdin)
    return matrix


def split(matrix):
    matrix_up, matrix_down = np.hsplit(matrix, 2)
    matrix11, matrix21 = np.vsplit(matrix_up, 2)
    matrix12, matrix22 = np.vsplit(matrix_down, 2)
    return matrix11, matrix12, matrix21, matrix22


def mult(m1, m2):
    if m1.shape[0] == 1:
        return m1 * m2

    a11, a12, a21, a22 = split(m1)
    b11, b12, b21, b22 = split(m2)
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

    return np.hstack((np.vstack((c11, c12)),
                      np.vstack((c21, c22))))


def print_ans(ans):
    for i in ans:
        print(' '.join(map(str, i)))

real_size = int(input())
size = 1
while size < real_size:
    size *= 2
m1 = read_matrix(size, real_size)
m2 = read_matrix(size, real_size)
ans = mult(m1, m2)
print_ans(ans[:real_size, :real_size])
