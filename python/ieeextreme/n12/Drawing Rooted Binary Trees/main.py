#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io
import numpy as np

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

def getMatrix(h, w):
    matrix = []
    for i in range(h):
        row = []
        for j in range(w):
            row = []
        matrix.append(row)
    return matrix

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



def getSubInfixes(infix, operator):
    """
    Returns Operands between Operator
    """
    i = infix.index(operator)
    subinfix_left = infix[:i]
    subinfix_right = infix[i+1:]
    if DEBUG:
        print("getSubInfixes")
        print(subinfix_left)
        print(subinfix_right)
    return subinfix_left, subinfix_right

def getOperator(prefix):
    operator = prefix.pop(0)
    if DEBUG:
        print("getOperator")
        print(operator)
    return operator

def getSubPrefixes(prefix, n):
    subprefix_left = prefix[:n]
    subprefix_right = prefix[n:]
    if DEBUG:
        print("getSubPrefixes")
        print(subprefix_left)
        print(subprefix_right)
    return subprefix_left, subprefix_right

def getTree(tree, infix, prefix, n_row):

    if len(prefix) == 0:
        return None

    operator = getOperator(prefix)
    #if operator not in tree[n_row]:
    #    tree[n_row].append(operator)

    subinfix_left, subinfix_right = getSubInfixes(infix, operator)
    subprefix_left, subprefix_right = getSubPrefixes(prefix, len(subinfix_left))

    n_row += 1

    matrix_left = getTree(tree, subinfix_left, subprefix_left, n_row)

    matrix_right = getTree(tree, subinfix_right, subprefix_right, n_row)

    if matrix_left is None and matrix_right is None:
        # No childs.
        return np.array([[operator]])

    elif matrix_left is not None and matrix_right is not None:
        # Case 1: both childs.

        # Resize to get same height in both childs.
        h_left = matrix_left.shape[0]
        h_right = matrix_right.shape[0]
        delta = h_left - h_right
        if 0 < delta:
            # left child higher.
            matrix_right = addEmptyRows(matrix_right, delta, str, True)
        elif delta < 0:
            # right child higher.
            matrix_left = addEmptyRows(matrix_left, delta*(-1), str, True)

        # Append empty row.
        matrix_left = prependEmptyRow(matrix_left, str)
        matrix_right = prependEmptyRow(matrix_right, str)

        aux = np.empty((matrix_left.shape[0], 1), dtype=str)
        aux[0][0] = operator
        aux = np.append(matrix_left, aux, axis=1)

        return np.append(aux, matrix_right, axis=1)

    elif matrix_left is None:

        # Case 2: no left child.

        # Append empty row.
        matrix_right = prependEmptyRow(matrix_right, str)

        aux = np.empty((matrix_right.shape[0], 1), dtype=str)
        aux[0][0] = operator
        return np.append(aux, matrix_right, axis=1)

    else:

        # Case 3: no right child.

        # Append empty row.
        matrix_left = prependEmptyRow(matrix_left, str)

        aux = np.empty((matrix_left.shape[0], 1), dtype=str)
        aux[0][0] = operator
        return np.append(matrix_left, aux, axis=1)



def beautifyTree(tree):

    beautified_tree = ""
    for row in tree:
        for node in row:
            beautified_tree += node
        beautified_tree += "\n"

    return beautified_tree
"""
Questions

DarkMasters: what is the number of the nodes
Answer: Nodes are uniquely labeled by lower case letters, which constrains the size of a tree.

"""


"""
https://www.geeksforgeeks.org/expression-tree/
https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
https://www.geeksforgeeks.org/convert-infix-prefix-notation/
"""
def main(argv):

    reader = io.open(sys.stdin.fileno())

    while True:
        infix = readString(reader)
        if infix == "":
            break
        infix = list(infix)
        prefix = readString(reader)
        prefix = list(prefix)

        tree = getMatrix(27, 1)

        tree[0].append(prefix[0])
        tree = getTree(tree, infix, prefix, 0)

        for row in tree:
            line = ""
            for element in row:
                if element == "":
                    line += " "
                else:
                    line += element
            print(line)

if __name__ == "__main__":
    main(sys.argv)