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

def key2value(key):

    if key == "xrtp":       # zero
        return 0
    elif key == "pmr":      # one
        return 1
    elif key == "yep":      # two
        return 2
    elif key == "yjtrr":    # three
        return 3
    elif key == "gpit":     # four
        return 4
    elif key == "gobr":     # five
        return 5
    elif key == "doc":      # six
        return 6
    elif key == "drbrm":    # seven
        return 7
    elif key == "rohjy":    # eight
        return 8
    elif key == "momr":     # nine
        return 9

########################################################################################################################
# MAIN
########################################################################################################################

def main(argv):

    reader = io.open(sys.stdin.fileno())

    N = readInt(reader)

    n = 1
    for i in range(N):

        numbers = readString(reader).split(" ")
        number_bin = ""
        for number_str in numbers:
            number = key2value(number_str)
            number_bin += "{0:04b}".format(number)
        n = n * int(number_bin, 2)

    print(n)

if __name__ == "__main__":
    main(sys.argv)