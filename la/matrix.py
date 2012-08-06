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




def gauss_jordan(A):
    M = copy(A)
    rank = len(M)
    I    = Identity(rank)

    for p in range(rank): # p <-- pivot row
        pivot = M[p][p] # FIXME what if pivot is zero???
        for t in range(rank): # t <-- target row
            if p == t: continue # compare this with that of LU
            if not is_zero(M[t][p]):
                coeff = -1.0 * M[t][p] / pivot
                for _c in range(rank):
                    M[t][_c] = coeff * M[p][_c] + M[t][_c] # coeff*pivot_row + target_row
                    I[t][_c] = coeff * I[p][_c] + I[t][_c]

    determ = 1.0 # determ is product of pivots
    for i in range(rank):
        determ *= M[i][i]
        for j in range(rank):
            I[i][j] /= M[i][i]

    ensure_zero(I)
    return determ, I


def LU(A):
    M = copy(A)
    rank = len(M)
    I    = Identity(rank)

    L_elements = []

    for p in range(rank): # p <-- pivot row
        pivot = M[p][p]
        for t in range(rank): # t <-- target row

            if p >= t: continue # assert p < t

            if not is_zero(M[t][p]):
                coeff = -1.0 * M[t][p] / pivot
                E_target_pivot = Identity(rank)
                E_target_pivot[t][p] = coeff

                # update M
                M = product(E_target_pivot, M)

                # compute inverse of E_target_pivot <-- just negate!
                E_target_pivot[t][p] = E_target_pivot[t][p] * -1.0

                L_elements.append(E_target_pivot)

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


"""
Strang ITL p127
http://stattrek.com/matrix-algebra/echelon-transform.aspx
"""

def echelon(A):
    M = copy(A)

    pivot_row = -1

    for c in range(column_size(M)):
        # fine pivot

        pivot = None
        for i in range(pivot_row +1, row_size(M), 1):
            if not is_zero(M[i][c]):
                pivot_row = i
                pivot = M[i][c]
                break

        assert pivot_row is not None


        for target_row in range(pivot_row+1, row_size(M), 1):
            if not is_zero(M[target_row][c]):
                coeff = -1.0 * M[target_row][c] / pivot

                for _c in range(column_size(M)):
                    M[target_row][_c] = coeff * M[pivot_row][_c] + M[target_row][_c]

    return M

def solve_echelon(A):
    U = echelon(A)
    X = []

    # make U as a square matrix
    pivots = []
    for i in range(row_size(U)):
        for j in range(column_size(U)):
            if not is_zero(U[i][j]):
                pivots.append((j, i))
                break

    SquareU = []
    _next = 0 # inclusive last
    for pivot_idx, pivot_src in pivots:
        for i in range(_next, pivot_idx):
            SquareU.append(None)
        SquareU.append(U[pivot_src])
        _next = pivot_idx + 1
    for i in range(_next, column_size(U)):
        SquareU.append(None)


    # solve Ux = 0
    rank = column_size(SquareU)
    x = [0.0] * rank
    for i in range(column_size(U)-1, -1, -1):
        if SquareU[i] is None:
            x[i] = 1
            continue
        _p = 0.0
        for j in range(rank):
            if i == j: continue
            _p += x[j] * SquareU[i][j]
        x[i] = ( 0.0 - _p)/SquareU[i][i]
    return x



# # # # # # # # # # # # # # # # # # CURRENT

def test_solve_echelon():
    print 'test_solve_echelon'
    A = [
            [1, 1, 2, 3],
            [2, 2, 8, 10],
            [3, 3, 10, 13]]
    x = solve_echelon(A)
    print post_apply(A, x)


def test_echelon():
    A = [
            [1, 1, 2, 3],
            [2, 2, 8, 10],
            [3, 3, 10, 13]]
    show(echelon(A))

    A = [
            [1, 2, 2, 4],
            [3, 8, 6, 16]]
    U = echelon(A)

    show(U)

    A = [
            [1, 1, 2, 3],
            [0, 0, 4, 4],
            [0, 0, 0, 0]]
    U = echelon(A)
    show(U)
test_echelon()

def test_symmetric():
    A = [
            [1, 2, 30],
            [2, 5, 60],
            [30, 60, 9]]

    L, D, U = LDU(A)

    assert equals(transpose(L), U)

def test_transpose():
    A = [
            [1, 2, 30],
            [4, 5, 60],
            [7, 80, 9]]

    B = [
            [7, 13, 30],
            [8, 5, 60],
            [70, 8, 9]]

    assert equals( transpose(sum(A, B)), sum(transpose(A), transpose(B)))
    assert equals( transpose(product(A, B)), product(transpose(B), transpose(A)))

    determA, InvA = gauss_jordan(A)
    TrA = transpose(A)
    _d, InvTransA = gauss_jordan(TrA)

    assert equals( transpose(InvA), InvTransA )

    L, D, U = LDU(A)

    assert equals( TrA, product(product(transpose(U), transpose(D)), transpose(L)) )


def test_pascal_LU():
    A = [
            [1, 1, 1, 1],
            [1, 2, 3, 4],
            [1, 3, 6, 10],
            [1, 4, 10, 20]]

    L, U = LU(A)
    show(L)
    show(U)

def test_pascal_inverse():
    A = [
            [1, 1, 1, 1],
            [1, 2, 3, 4],
            [1, 3, 6, 10],
            [1, 4, 10, 20]]

    determ, Inv = gauss_jordan(A)

    print determ
    show(Inv)

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
    assert equals(product(L, U), A)

def test_gauss_jordan1():
    M = [
            [2, -1, 0],
            [-1, 2, -1],
            [0, -1, 2]]

    M1 = copy(M)

    determ, I = gauss_jordan(M1)

    print determ

    print product(M, I)


def test_gauss_jordan2():
    M = [
            [2, 3],
            [4, 7]]

    M1 = copy(M)
    determ, Inv = gauss_jordan(M1)
    print determ, Inv
    print product(M, Inv)

def test_gauss_jordan3():
    A = [
            [1, 0, 0],
            [3, 1, 0],
            [4, 5, 1]]
    A1 = copy(A)
    show(A1)

    determ, Inv = gauss_jordan(A1)

    print determ
    show(Inv)
    show(product(Inv, A))

def test_triangular_pascal_matrix():
    print 'Triangular Pascal matrix'
    A = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 2, 1, 0],
            [1, 3, 2, 1]]
    A1 = copy(A)
    show(A1)

    determ, Inv = gauss_jordan(A1)

    print determ
    show(Inv)
    show(product(Inv, A))


# EOF
