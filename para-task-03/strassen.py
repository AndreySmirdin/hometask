import numpy as np
def read_matrix(n, size):
    a = []
    for i in range(n):
        a.append([int(j) for j in input().split()])
    m = np.array(a)
    m = np.hstack((m, np.zeros((n, size - n), dtype = int)))
    m = np.vstack((m, np.zeros((size - n, size), dtype = int)))
    return m

def mult(m1, m2, size):
    if size == 1:
        return m1*m2
    else:
        size = size//2
        a11 = m1[:size, :size]
        a12 = m1[:size, size:]
        a21 = m1[size:, :size]
        a22 = m1[size:, size:]
        b11 = m2[:size, :size]
        b12 = m2[:size, size:]
        b21 = m2[size:, :size]
        b22 = m2[size:, size:]
        p1 = mult(a11 + a22, b11 + b22, size)
        p2 = mult(a21 + a22, b11, size)
        p3 = mult(a11, b12 - b22, size)
        p4 = mult(a22, b21 - b11, size)
        p5 = mult(a11 + a12, b22, size)
        p6 = mult(a21 - a11, b11 + b12, size)
        p7 = mult(a12 - a22, b21 + b22, size)
						
        c11 = p1 + p4 + p7 - p5
        c12 = p2 + p4
        c21 = p3 + p5
        c22 = p1 - p2 + p3 + p6

    return np.hstack((np.vstack((c11,c12)), np.vstack((c21,c22)))) 

def print_ans(ans,n):
    #ans = np.delete(ans, np.s_[n:], axis=0)
    #ans = np.delete(ans, np.s_[n:], axis=1)
    for i in range(n):
        print(*[ans[i,j] for j in range(n)])
        


n = int(input())
size = 1
while size < n:
    size *= 2
ans = mult(read_matrix(n,size), read_matrix(n,size), size)
print_ans(ans,n)
