#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

DEBUG = True
n_iterations = 0
MAX_ITERATIONS = 10000 # Segmentation fault with 100000
sys.setrecursionlimit(100000)

def readString(reader):
    return reader.readline().replace("\n","")

def readInt(reader):
    line = reader.readline().replace("\n","")
    if line=="":
        return None
    else:
        return int(line)

def readMatrix(reader, n_rows):
    matrix = []
    for i in range(n_rows):
        row = []
        line = reader.readline().replace("\n", "")
        for j in line:
            row.append(j)
        matrix.append(row)
    return matrix

# https://stackoverflow.com/questions/24101524/finding-median-of-list-in-python
def median(list):
    n = len(list)
    if n<1:
        return None
    if n%2==1:
        return sorted(list)[n//2]
    else:
        return sum(sorted(list)[n//2-1:n//2+1])/2.0

def getMatrix(h, w, value):
    matrix = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append(value)
        matrix.append(row)
    return matrix

########################################################################################################################
# NUMPY
########################################################################################################################

import numpy as np

def appendEmptyRow(matrix, type):
    return addEmptyRows(matrix, 1, type, True)

def prependEmptyRow(matrix, type):
    return addEmptyRows(matrix, 1, type, False)

def addEmptyRows(matrix, n_rows, type, append):
    aux = np.empty((n_rows, matrix.shape[1]), dtype=type)
    if append:
        matrix = np.append(matrix, aux, axis=0)
    else:
        matrix = np.append(aux, matrix, axis=0)
    return matrix


########################################################################################################################
# MAIN
########################################################################################################################

def main(argv):

    reader = io.open(sys.stdin.fileno())

    line = readString(reader).split(" ")
    N = int(line[0])
    M = int(line[1])

    # print(N)
    # print(M)

    A = readString(reader).split(" ")
    A = [int(i) for i in A]
    A = np.array(A)[np.newaxis]
    A = A.T
    #print(A)

    B = readString(reader).split(" ")
    B = [int(i) for i in B]
    B = np.array(B)[np.newaxis]
    #print(B)

    C = A*B
    #print(C)

    maxSum = 0
    for starti in range(N):
        for startj in range(M):
            for endi in range(starti+1, N+1):
                for endj in range(startj+1, M+1):
                    newMat = C[starti:endi, startj: endj]
                    newSum = np.sum(newMat)
                    if maxSum < newSum:
                        maxSum = newSum

    print(maxSum)

if __name__ == "__main__":
    main(sys.argv)