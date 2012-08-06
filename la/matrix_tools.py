# -*- coding: cp949 -*-
"""
linear algebra practices
한글 주석!!
"""
EPSILON = 0.000001

def is_zero(x):
    return abs(x) < EPSILON

def column_size(A):
    return len(A[0])

def row_size(A):
    return len(A)

def show(A):
    print row_size(A), 'x', column_size(A)
    for i in range(len(A)):
        print A[i]
    print ''

def ensure_zero(A):
    for i in range(row_size(A)):
        for j in range(column_size(A)):
            if abs(A[i][j]) < EPSILON:
                A[i][j] = 0.0

    return A

def equals(A, B):
    def _equals(A, B):
        for i in range(column_size(A)):
            for j in range(row_size(A)):
                if abs(A[i][j] - B[i][j]) > EPSILON:
                    print 'equals failed at:', i, j
                    return False
        return True
    return column_size(A) == column_size(B) and row_size(A) == row_size(B) and _equals(A, B)

def deter2x2(M):
    a = M[0][0]
    b = M[0][1]
    c = M[1][0]
    d = M[1][1]
    return a*d - b*c

def Zero(r, c):
    _r = [0] * c
    A = []
    for i in range(r):
        A.append(_r[:])

    return A

def Identity(rank):
    A = Zero(rank, rank)
    for i in range(rank):
        A[i][i] = 1.0

    return A

def sum(A, B):
    # make sure both are of the same size
    r = row_size(A)
    assert r == row_size(B)
    c = column_size(B)
    assert c == column_size(B)
    C = Zero(r, c)

    for i in range(r):
        for j in range(c):
            C[i][j] = A[i][j] + B[i][j]

    ensure_zero(C)
    return C

def post_apply(A, x):
    k = column_size(A)
    assert k == len(x)
    c = [0.0] * k

    for i in range(row_size(A)):
        p = 0.0
        for j in range(k):
            p += A[i][j]*x[j]
        c[i] = p

    return c

def product(A, B):
    r = row_size(A)
    k = column_size(A)
    assert k == row_size(B)
    c = column_size(B)
    C = Zero(r, c)

    for i in range(r):
        for j in range(c):
            p = 0.0
            for _k in range(k):
                p += A[i][_k]*B[_k][j]
            C[i][j] = p

    ensure_zero(C)
    return C


def copy(A):
    B = []
    for i in range(len(A)):
        B.append(A[i][:])
    return B


# EOF
