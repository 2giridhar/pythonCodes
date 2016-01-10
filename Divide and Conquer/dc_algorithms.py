# -*- coding: utf-8 -*-
from numpy import *  # analysis:ignore


# STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
STOCK_PRICE_CHANGES2 = [-3, -25, -1, -16, -23, -7, -5, -22, -4]
STOCK_PRICE_CHANGES3 = [3, 25, 1, 16, 23, 7, 5, 22, 4]
STOCK_PRICE_CHANGES4 = [3, -25, 1, -16, 23, -7, 15, -22, 4]

MATRIX_A = [[1, 1], [2, 2]]
MATRIX_B = [[3, 3], [4, 4]]
MATRIX_A2 = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
MATRIX_B2 = [[2, -3, 4, -6], [8, 7, -2, 1], [3, -3, 4, 0], [2, -6, 4, -2]]
MATRIX_A3 = [[2, -5], [6, 4]]
MATRIX_B3 = [[3, 4], [-6, 7]]


# Implement pseudocode from the book
def find_maximum_subarray_brute(a):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)
    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES)
    (7, 10)
    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES2)
    (2, 2)
    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES3)
    (0, 8)
    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES4)
    (4, 6)
    """

    left = 0
    right = 0
    max_sum = - infty
    for i in range(0, len(a)):
        current_sum = 0
        for j in range(i, len(a)):
            current_sum += a[j]
            if max_sum < current_sum:
                max_sum = current_sum
                left = i
                right = j
    return left, right


# Implement pseudocode from the book
def find_maximum_crossing_subarray(a, low, mid, high):
    """
    Find the maximum subarray that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    """

    left_sum = a[mid]
    temp_sum = 0
    max_left = mid
    max_right = mid + 1
    for i in range(mid, low - 1, -1):
        temp_sum = temp_sum + a[i]
        if temp_sum > left_sum:
            left_sum = temp_sum
            max_left = i
    right_sum = a[mid + 1]
    temp_sum = 0
    for j in range(mid + 1, high + 1):
        temp_sum = temp_sum + a[j]
        if temp_sum > right_sum:
            right_sum = temp_sum
            max_right = j
    return max_left, max_right, left_sum + right_sum


def find_maximum_subarray_recursive(a, low, high):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES)-1)
    (7, 10, 43)
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES2, 0, len(STOCK_PRICE_CHANGES2)-1)
    (2, 2, -1)
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES3, 0, len(STOCK_PRICE_CHANGES3)-1)
    (0, 8, 106)
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES4, 0, len(STOCK_PRICE_CHANGES4)-1)
    (4, 6, 31)
    """

    if high == low:
        return low, high, a[low]
    else:
        mid = (low + high) / 2
        (left_low, left_high, left_sum) = find_maximum_subarray_recursive(a, low, mid)
        (right_low, right_high, right_sum) = find_maximum_subarray_recursive(a, mid + 1, high)
        (cross_low, cross_high, cross_sum) = find_maximum_crossing_subarray(a, low, mid, high)
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum


def find_maximum_subarray_iterative(a, low, high):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES)-1)
    (7, 10)
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES2, 0, len(STOCK_PRICE_CHANGES2)-1)
    (2, 2)
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES3, 0, len(STOCK_PRICE_CHANGES3)-1)
    (0, 8)
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES4, 0, len(STOCK_PRICE_CHANGES4)-1)
    (4, 6)
    """

    temp_sum, final_sum, temp_low, final_low, final_high = 0, 0, 0, 0, 0
    min_sum = temp_sum
    if high == low:
        return low, high
    else:
        for i in range(low, high + 1):
            temp_sum += a[i]
            if temp_sum < min_sum:
                temp_sum = min_sum
                temp_low = i + 1
            elif temp_sum > final_sum:
                final_sum = temp_sum
                final_low = temp_low
                final_high = i
        "If all the numbers are negative in the array then select least negative number"
        if final_sum == 0 & final_high == final_low:
            temp_sum = -infty
            for i in range(low, high + 1):
                if temp_sum < a[i]:
                    temp_sum = a[i]
                    final_low = i
            return final_low, final_low
        else:
            return final_low, final_high


def square_matrix_multiply(a, b):
    """
    Return the product AB of matrix multiplication.
    >>> square_matrix_multiply(MATRIX_A, MATRIX_B)
    array([[ 7,  7],
           [14, 14]])
    >>> square_matrix_multiply(MATRIX_A2, MATRIX_A2)
    array([[4, 4, 4, 4],
           [4, 4, 4, 4],
           [4, 4, 4, 4],
           [4, 4, 4, 4]])
    >>> square_matrix_multiply(MATRIX_A2, MATRIX_B2)
    array([[15, -5, 10, -7],
           [15, -5, 10, -7],
           [15, -5, 10, -7],
           [15, -5, 10, -7]])
    >>> square_matrix_multiply(MATRIX_A3, MATRIX_B3)
    array([[ 36, -27],
           [ -6,  52]])
    """
    a = asarray(a)
    b = asarray(b)
    assert a.shape == b.shape
    assert a.shape == b.T.shape
    c = zeros(a.shape, dtype=int)
    for i in range(len(a)):
        for j in range(len(b)):
            for k in range(len(c)):
                c[i][j] += multiply(a[i][k], b[k][j])
    return c


def square_matrix_multiply_strassens(a, b):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    >>> square_matrix_multiply_strassens(MATRIX_A, MATRIX_B)
    array([[ 7,  7],
           [14, 14]])
    >>> square_matrix_multiply_strassens(MATRIX_A2, MATRIX_A2)
    array([[4, 4, 4, 4],
           [4, 4, 4, 4],
           [4, 4, 4, 4],
           [4, 4, 4, 4]])
    >>> square_matrix_multiply_strassens(MATRIX_A3, MATRIX_B3)
    array([[ 36, -27],
           [ -6,  52]])
    >>> square_matrix_multiply_strassens(MATRIX_A2, MATRIX_B2)
    array([[15, -5, 10, -7],
           [15, -5, 10, -7],
           [15, -5, 10, -7],
           [15, -5, 10, -7]])
    """
    a = asarray(a)
    b = asarray(b)
    assert a.shape == b.shape
    assert a.shape == a.T.shape
    assert (len(a) & (len(a) - 1)) == 0, "A is not a power of 2"

    length = len(a)
    mid = length / 2

    a11 = a[0:mid, 0:mid]
    a12 = a[0:mid, mid:length]
    a21 = a[mid:length, 0:mid]
    a22 = a[mid:length, mid:length]

    b11 = b[0:mid, 0:mid]
    b12 = b[0:mid, mid:length]
    b21 = b[mid:length, 0:mid]
    b22 = b[mid:length, mid:length]

    if length == 1:
        c = multiply(a, b)
    else:
        s1 = asarray(b12 - b22)
        s2 = asarray(a11 + a12)
        s3 = asarray(a21 + a22)
        s4 = asarray(b21 - b11)
        s5 = asarray(a11 + a22)
        s6 = asarray(b11 + b22)
        s7 = asarray(a12 - a22)
        s8 = asarray(b21 + b22)
        s9 = asarray(a11 - a21)
        s10 = asarray(b11 + b12)

        p1 = asarray(square_matrix_multiply_strassens(a11, s1))
        p2 = asarray(square_matrix_multiply_strassens(s2, b22))
        p3 = asarray(square_matrix_multiply_strassens(s3, b11))
        p4 = asarray(square_matrix_multiply_strassens(a22, s4))
        p5 = asarray(square_matrix_multiply_strassens(s5, s6))
        p6 = asarray(square_matrix_multiply_strassens(s7, s8))
        p7 = asarray(square_matrix_multiply_strassens(s9, s10))

        c1 = p5 + p4 - p2 + p6
        c2 = p1 + p2
        c3 = p3 + p4
        c4 = p5 + p1 - p3 - p7

        c = bmat([[c1, c2], [c3, c4]])
        c = asarray(c)
    return c
    pass


def test():
    import doctest
    doctest.testmod()
    pass


if __name__ == '__main__':
    test()
