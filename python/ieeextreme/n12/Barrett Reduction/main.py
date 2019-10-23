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

import math

def main(argv):

    reader = io.open(sys.stdin.fileno())

    line = readString(reader).split(" ")
    # 0 <= A <= 2^32
    A = int(line[0])
    # 0 <= B <= 63
    B = int(line[1])

    y = math.floor(A / pow(2, B))

    for D in range(1, int(math.pow(2,31))):
        ok = True
        for X in range(1, int(math.pow(2, 31))):
            x = math.floor(X/D)
            if x != (y*X):
                ok = False
                break
        if ok is True:
            break

    print(D)

if __name__ == "__main__":
    main(sys.argv)