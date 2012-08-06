# -*- coding: cp949 -*-
from matrix_tools import *

"""
Strang ITL p127
http://stattrek.com/matrix-algebra/echelon-transform.aspx
"""

def reduced_row_echelon(A):
    M = copy(A)

    def find_pivot(row_cursor, ci):
        for ri in range(row_cursor, row_size(M)):
            if not is_zero(M[ri][ci]):
                return ri
        return None

    row_cursor = -1
    for ci in range(column_size(M)):
        #1) find a row which has a pivot column
        pivot_row_index = find_pivot(row_cursor+1, ci)

        if pivot_row_index is None:
            continue
        else:
            row_cursor += 1
            #2) make the matrix in echelon form
            #   row_cursor stores the history
            if row_cursor != pivot_row_index:
                tmp = M[row_cursor]
                M[row_cursor] = M[pivot_row_index]
                M[pivot_row_index] = tmp
        
        #3) divide every value in the pivot row with pivot value
        pv = M[row_cursor][ci]
        for cci in range(column_size(M)):
            M[row_cursor][cci] /= pv

        #4) make reduced row form
        for ri in range(row_size(M)):
            if ri == row_cursor:
                continue
            if M[ri][ci] != 0:
                k = M[ri][ci]
                for cci in range(column_size(M)):
                    M[ri][cci] -= (M[row_cursor][cci] * k)

    return M

def compute_rank(A):
    M = copy(A)
    M_rre = reduced_row_echelon(M)

    rank = 0
    for ri in range(row_size(M_rre)):
        for ci in range(column_size(M_rre)):
           if not is_zero(M_rre[ri][ci]):
                rank += 1
                break

    return rank

def test():
    A = [
            [0, 1, 2],
            [1, 2, 1],
            [2, 7, 8]]
    show(A)
    show(reduced_row_echelon(A))

    A = [
            [0, 1],
            [1, 2],
            [0, 5]]
    show(A)
    A_rre = reduced_row_echelon(A)
    show(A_rre)

    assert compute_rank(A_rre) == 2

    A = [
            [1, 3, 0, 2, -1],
            [0, 0, 1, 4, -3],
            [1, 3, 1, 6, -4]]
    show(A)
    A_rre = reduced_row_echelon(A)
    show(A_rre)

test()
