#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io


"""
Topology is a branch of mathematics that examines the shapes and structures of objects. 
The Euler characteristic is a topological label that we can determine for an item or collection of items. 
For a group of two dimensional objects, 
one way to define the Euler characteristic is the number of connected objects minus the number of holes in the objects.

The Euler characteristic has useful applications in 2D image recognition and classification.

Your task is to compute the Euler characteristic (connected regions minus holes) 
for a black and white image.
"""

DEBUG = False

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
        line = reader.readline().replace("\n","")
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

"""
1) n: height of the image. 1 <= n <= 1,000
2) m: width of the image. 1 <= m <= 1,000
Store matrix 1000x1000=1Mb
3) n lines of text. 
These n lines of text contain m characters, 
each of which is either the letter 'X' or the letter 'O'. 
An 'X' represents a black pixel, and 
an 'O' represents a white pixel.
"""
def getEulerCharacteristic(reader):
    h = readInt(reader)
    w = readInt(reader)
    matrix = readMatrix(reader, h)
    n_connections, n_holes = getConnectionsNHoles(matrix, h, w)
    return n_connections-n_holes

"""
In this problem, we consider 
filled-in regions that touch diagonally to be part of the same connected region; however, 
holes that only touch diagonally are considered to be separate.
"""
def getConnectionsNHoles(matrix, h, w):

    #print(matrix)
    map = getMatrix(h, w, None)

    mapBorders(matrix, map, h, w)
    #print(map)

    n_connections = 0
    for row in range(1, h, 2):
        for col in range(1, w, 2):
            pixel = matrix[row][col]
            #print(pixel)
            kernel_matrix = getKernel(matrix, row, col, h, w)
            #print(kernel)
            if pixel == "O":
                # Border
                # Hole
                value = getMaxNegativeInKernel(kernel_matrix)
                if value is None:
                    # New hole
                    #value = getMinNegativeInMatrix(matrix)
                    value = -5
                    if value is None:
                        map[row][col] = -1
                    else:
                        map[row][col] = value - 1
                    #if DEBUG:
                    #    print("New hole in: ("+str(i)+", "+str(j)+")")
                    #    print("Value: "+str(matrix[i][j]))
                else:
                    setNonPositiveInKernel(map, row, col, h, w, value)
            else:
                # Filled
                kernel_map = getKernel(map, row, col, h, w)
                value = getMinPositiveInKernel(kernel_map)
                #print(value)
                if value is None:
                    # New connection.
                    #print("New connection in: ("+str(i)+", "+str(j)+")")
                    #value = getMaxPositiveInMatrix(matrix)
                    n_connections += 1
                    value = n_connections
                mapX(matrix, map, row, col, h, w, value)
            print(map)
    if DEBUG:
        print(map)
    n_holes = getMinNegativeInMatrix(map)
    if n_holes is None:
        n_holes = 0
    n_holes = n_holes*(-1) - 1
    n_connections = getMaxPositiveInMatrix(map)
    if n_connections is None:
        n_connections = 0
    return n_connections, n_holes

"""
(i-1, j-1)   (i-1, j)   (i-1, j+1)
(i  , j-1)   (i  , j)   (i  , j+1)
(i+1, j-1)   (i+1, j)   (i+1, j+1)
"""
def getKernel(matrix, i, j, h, w):

    kernel = getMatrix(3, 3, None)

    row_min = i - 1 if 0 <= (i - 1) else i
    row_max = i + 1 if (i + 1) < h else i
    col_min = j - 1 if 0 <= (j - 1) else j
    col_max = j + 1 if (j + 1) < w else j
    for row in range(row_min, row_max + 1):
        for col in range(col_min, col_max + 1):
            kernel[row - (i - 1)][col - (j - 1)] = matrix[row][col]
    return kernel



########################################################################################################################
# BORDERS
########################################################################################################################

def mapBorders(matrix, map, h, w):
    # Rows
    for col in range(w):
        changeOto0(matrix, map, 0, col)
        changeOto0(matrix, map, h - 1, col)
    # Cols
    for row in range(h):
        changeOto0(matrix, map, row, 0)
        changeOto0(matrix, map, row, w - 1)

def changeOto0(matrix, map, row, col):
    c = matrix[row][col]
    if c == "O":
        map[row][col] = 0

########################################################################################################################
# NEGATIVE (HOLES)
########################################################################################################################

"""
Kernel:
             (i-1, j)
(i  , j-1)   (i  , j)   (i  , j+1)
             (i+1, j) 
             
Values:
values = [-1, -2, -3]
Must return -1.
"""
def getMaxNegativeInKernel(kernel):
    values = []
    if kernel[1][1] < 0:
        values.append(kernel[1][1])
    # Row
    if kernel[1][0] < 0:
        values.append(kernel[1][0])
    if kernel[1][2] < 0:
        values.append(kernel[1][2])
    # Column
    if kernel[0][1] < 0:
        values.append(kernel[0][1])
    if kernel[2][1] < 0:
        values.append((kernel[2][1]))
    #print("getMaxNonPositiveInKernel")
    #print(values)
    if 0<len(values):
        return max(values)
    return None

def getMinNegativeInMatrix(matrix):
    return getValueInMatrix(matrix, False, False)

"""
             (i-1, j)
(i  , j-1)   (i  , j)   (i  , j+1)
             (i+1, j) 
"""
def setNonPositiveInKernel(matrix, i, j, h, w, value):
    matrix[i][j] = value
    # Row
    if 0 <= (j - 1) and matrix[i][j - 1] < 0:
        matrix[i][j - 1] = value
    if (j + 1) < w and matrix[i][j + 1] < 0:
        matrix[i][j + 1] = value
    # Column
    if 0 <= (i - 1) and matrix[i - 1][j] < 0:
        matrix[i - 1][j] = value
    if (i + 1) < h and matrix[i + 1][j] < 0:
        matrix[i + 1][j] = value

########################################################################################################################
# POSITIVE (FILLED)
########################################################################################################################

"""
(i-1, j-1)   (i-1, j)   (i-1, j+1)
(i  , j-1)   (i  , j)   (i  , j+1)
(i+1, j-1)   (i+1, j)   (i+1, j+1)
"""

def getMinPositiveInKernel(kernel):
    return getValueInMatrix(kernel, True, False)

def getMaxPositiveInMatrix(matrix):
    return getValueInMatrix(matrix, True, True)

def getValueInMatrix(matrix, get_positive, get_max):
    values = []
    for row in matrix:
        for element in row:
            if element is not None:
                if (get_positive and 0 < element) or (not get_positive and element < 0):
                    values.append(element)
    #print(values)
    if 0<len(values):
        if get_max:
            return max(values)
        else:
            return min(values)
    return None

"""
(i-1, j-1)   (i-1, j)   (i-1, j+1)
(i  , j-1)   (i  , j)   (i  , j+1)
(i+1, j-1)   (i+1, j)   (i+1, j+1)
"""
def setPositiveInMatrix(matrix, i, j, h, w, value):
    row_min = i - 1 if 0 <= (i - 1) else i
    row_max = i + 1 if (i + 1) < h else i
    col_min = j - 1 if 0 <= (j - 1) else j
    col_max = j + 1 if (j + 1) < w else j
    # print("setPositiveInMatrix")
    # print(row_min)
    # print(row_max)
    # print(col_min)
    # print(col_max)
    matrix[i][j] = value
    for row in range(row_min, row_max + 1):
        for col in range(col_min, col_max + 1):
            element = matrix[row][col]
            if 0 < element:
                #print("matrix["+str(row)+"]["+str(col)+"]="+str(value))
                matrix[row][col] = value

def mapX(matrix, map, i, j, h, w, value):
    row_min = i - 1 if 0 <= (i - 1) else i
    row_max = i + 1 if (i + 1) < h else i
    col_min = j - 1 if 0 <= (j - 1) else j
    col_max = j + 1 if (j + 1) < w else j
    # print("setPositiveInMatrix")
    # print(row_min)
    # print(row_max)
    # print(col_min)
    # print(col_max)
    map[i][j] = value
    for row in range(row_min, row_max + 1):
        for col in range(col_min, col_max + 1):
            element = matrix[row][col]
            if element == "X":
                #print("matrix["+str(row)+"]["+str(col)+"]="+str(value))
                map[row][col] = value


def main(argv):

    reader = io.open(sys.stdin.fileno())

    """
    t: number of testcases
    1 <= t <= 10.
    """
    t = readInt(reader)

    for i in range(t):
        print(getEulerCharacteristic(reader))

if __name__ == "__main__":
    main(sys.argv)