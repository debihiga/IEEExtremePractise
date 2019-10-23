#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

DEBUG = False
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


def getPath(tree, path_AB, nodes, A, B):

    # Type 1
    for path_A in tree[A][0]:
        for node in path_A:
            for path_B in tree[B][0]:
                if node in path_B:
                    if DEBUG:
                        print("getPath")
                        print(B)
                        print(node)
                    path_AB += path_B
                    return True

    # Type n.
    for path_A in tree[A][0]:
        for node in path_A:
            if node not in nodes:
                nodes.append(node)
                found = getPath(tree, path_AB, nodes, node, B)
                if found:
                    if DEBUG:
                        print("insert")
                        print(path_AB)
                        print(node)
                    path_AB = path_A + path_AB
                    return True

    return False

def getTree(reader, N):

    tree = {}
    for i in range(N):
        line = readString(reader)
        U, V = line.split(" ")
        if U not in tree:
            tree[U] = [[], 0]
        if V not in tree:
            tree[V] = [[], 0]
        tree[U][0].append([V])
        tree[V][0].append([U])

    return tree

########################################################################################################################
# MAIN
########################################################################################################################

def main(argv):

    reader = io.open(sys.stdin.fileno())

    line = readString(reader).split(" ")

    # N: number of nodes.
    # 1 <= N <= 10^5
    N = int(line[0])

    # M: number of operations.
    # 1 <= M <= 10^5
    M = int(line[1])

    tree = getTree(reader, N-1)
    #print(tree)

    max = 0
    for i in range(M):

        path = []
        nodes = []

        line = readString(reader)
        A, B, k = line.split(" ")
        K = int(k)

        nodes.append(A)
        nodes.append(B)
        getPath(tree, path, nodes, A, B)

        #print(path)
        path_A = path[:]
        path_A.append(B)
        tree[A][0].append(path_A)
        print(path_A)
        path_B = path[:]
        path_B.insert(0, A)
        tree[B][0].append(path_B)
        print(path_B)
        path.insert(0, A)
        path.append(B)

        for node in path:
            tree[node][1] += K
            if max < tree[node][1]:
                max = tree[node][1]

    print(tree)
    print(max)

if __name__ == "__main__":
    main(sys.argv)