# -*- coding: cp949 -*-
from matrix_tools import *

"""
Strang ITL p83
"""

"""
square system�� ��� LU ������ ������ �� �ִ�.
    E1*...*En*A = U --> A = InvEn*...*InvE1*U
1) ���⼭ InvEn*...*InvE1 �� lower trangular form�̴�.
2) �� �������� ���� swap�� ����. <-- ���� Swap�� �ʿ��� ���� ���?
3) �밢 ���п� 0�� ������ �ȵȴ�.
"""
def LU(A):
    assert column_size(A) == row_size(A)

    M = copy(A)

    rank = row_size(M)

    L_elements = []

    for pi in range(rank): # p <-- pivot index
        # �밢�� �ִ� ���Ҹ� pivot���� ��´�.
        pivot_value = float(M[pi][pi])

        assert not is_zero(pivot_value)

        # pivot�� ���� ���� �����ϴ� �Ʒ��� ���� ���� ��� 0���� �ٲ۴�.
        for ri in range(pi+1, rank):
            target_value = float(M[ri][pi])
            if not is_zero(target_value):
                # elimination ��� E�� �غ��Ѵ�.
                E = Identity(rank)
                anti_value = -1.0 * target_value / pivot_value
                E[ri][pi] = anti_value

                M = product(E, M)

                # compute inverse of E <-- just negate!
                E[ri][pi] = E[ri][pi] * -1.0

                L_elements.append(E)

    # compute L from L_elements
    L = None
    for E in L_elements:
        if L is None:
            L = E
        else:
            L = product(L, E)

    return L, M


def LDU(A):
    L, U = LU(A)

    rank = column_size(A)

    _D = Identity(rank)

    for i in range(rank):
        assert not is_zero(U[i][i])
        _D[i][i] = U[i][i]
        for j in range(rank):
            U[i][j] = U[i][j] / _D[i][i]

    return L, _D, U

def solver_LU(A, b):
    rank = column_size(A)
    assert len(b) == rank
    L, U = LU(A)

    # Lc = b
    c = [0.0] * rank
    for i in range(rank):
        _p = 0.0
        for j in range(rank):
            if i == j: continue
            _p += c[j] * L[i][j]
        c[i] = (b[i] - _p)/L[i][i]

    # Ux = c
    x = [0.0] * rank
    for i in range(rank-1, -1, -1):
        _p = 0.0
        for j in range(rank):
            if i == j: continue
            _p += x[j] * U[i][j]
        x[i] = (c[i] - _p)/U[i][i]
    return x

def transpose(A):
    AT = Zero(column_size(A), row_size(A))

    for i in range(row_size(A)):
        for j in range(column_size(A)):
            AT[j][i] = A[i][j]

    return AT


def test_pascal_LU():
    A = [
            [1, 1, 1, 1],
            [1, 2, 3, 4],
            [1, 3, 6, 10],
            [1, 4, 10, 20]]

    L, U = LU(A)
    show(L)
    show(U)


def test_solver_LU():
    A = [
            [1, 2],
            [4, 9]]
    x = solver_LU(A, [5, 21])
    print x

def test_LDU():
    A = [
            [2, 1],
            [6, 8]]
    L, D, U = LDU(A)
    assert equals(product(product(L, D), U), A)

def test_LU1():
    A = [
            [2, 1],
            [6, 8]]
    L, U = LU(A)
    show(L)
    show(U)
    assert equals(product(L, U), A)

def test_LU2():
    A = [
            [2, 1, 0],
            [1, 2, 1],
            [0, 1, 2]]
    L, U = LU(A)

    show(A)
    show(L)
    show(U)
    assert equals(product(L, U), A)

test_LU2()

# EOF
