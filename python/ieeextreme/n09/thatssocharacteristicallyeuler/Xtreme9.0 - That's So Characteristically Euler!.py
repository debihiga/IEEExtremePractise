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

n_iterations = 0
MAX_ITERATIONS = 10000 # Segmentation fault with 100000
sys.setrecursionlimit(100000)

def readString(reader):
    return reader.readline().replace("\n", "")


def readInt(reader):
    line = reader.readline().replace("\n", "")
    if line == "":
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
    if n < 1:
        return None
    if n % 2 == 1:
        return sorted(list)[n // 2]
    else:
        return sum(sorted(list)[n // 2 - 1:n // 2 + 1]) / 2.0


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
    return n_connections - n_holes


"""
In this problem, we consider 
filled-in regions that touch diagonally to be part of the same connected region; however, 
holes that only touch diagonally are considered to be separate.
"""


def getConnectionsNHoles(matrix, h, w):

    # print(matrix)
    map = getMatrix(h, w, None)

    n_borders = mapBorders(matrix, map, h, w)
    # print(map)
    #print("After borders")
    #print(map)
    # for row in map:
    #     if None in row:
    #         print(row)

    n_connections = 0
    n_holes = 0
    for row in range(h):
        for col in range(w):

            pixel_mapped = map[row][col]

            if pixel_mapped is not None:
                continue

            pixel = matrix[row][col]
            if pixel == "X":
                # Filled
                value = getValueInKernel(map, row, col, h, w, True)
                if value is None:
                    # New connection.
                    n_connections += 1
                    value = n_connections
                mapAllPixels(matrix, map, row, col, h, w, value, True)
            elif pixel == "O":
                # Hole or border.
                value = getValueInKernel(map, row, col, h, w, False)
                if value is None:
                    # New hole.
                    n_holes += 1
                    value = n_holes*(-1)
                mapAllPixels(matrix, map, row, col, h, w, value, False)

    if DEBUG:
        print(map)
        print(n_connections)
        print(n_holes)
        print(n_borders)

    #print(map)
    return n_connections, n_holes

########################################################################################################################
# KERNEL
########################################################################################################################

def getValueInKernel(map, i, j, h, w, x):

    row_min = i - 1 if 0 <= (i - 1) else i
    row_max = i + 1 if (i + 1) < h else i
    col_min = j - 1 if 0 <= (j - 1) else j
    col_max = j + 1 if (j + 1) < w else j

    values = []

    if x:
        """
        X:
        (i-1, j-1)   (i-1, j)   (i-1, j+1)
        (i  , j-1)   (i  , j)   (i  , j+1)
        (i+1, j-1)   (i+1, j)   (i+1, j+1)
        """
        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                element = map[row][col]
                if element is not None and 0 < element:
                    values.append(element)
    else:
        """
        O:
                     (i-1, j)
        (i  , j-1)   (i  , j)   (i  , j+1)
                     (i+1, j)
        """
        for row in range(row_min, row_max + 1):
            element = map[row][j]
            if element is not None and element < 0:
                values.append(element)
        for col in range(col_min, col_max + 1):
            element = map[i][col]
            if element is not None and element < 0:
                values.append(element)

    if 0 < len(values):
        if x:
            return min(values)
        else:
            return max(values)

    return None

########################################################################################################################
# BORDERS
########################################################################################################################

"""
---------->
OOOOO
O???O
O???O
O???O
O???O
OOOOO
"""
def mapBorders(matrix, map, h, w):
    for row in range(h):
        if row == 0 or row == h-1:
            for col in range(w):
                mapBorder(matrix, map, row, col, h, w)
        else:
            mapBorder(matrix, map, row, 0, h, w)
            mapBorder(matrix, map, row, w - 1, h, w)

def mapBorder(matrix, map, row, col, h, w):
    if matrix[row][col] == "O" and map[row][col] is None:
        mapAllPixels(matrix, map, row, col, h, w, 0, False)

########################################################################################################################
# MAP PIXELS
########################################################################################################################

"""
Problemas con la recursividad!
Hay que limitar la cantidad de recursividades.
Una vez que llego a un maximo (seteado arriba, por una constante)
cerrar todos los nodos que se abrieron y
devolver el nodo que no se pudo abrir.
"""
def mapAllPixels(matrix, map, row, col, h, w, value, x):
    global n_iterations
    opened_nodes = []
    opened_nodes.append((row, col))
    mapPixels(matrix, map, opened_nodes, h, w, value, x)
    #print(result)
    while len(opened_nodes) != 0:
        #print(opened_nodes)
        # Open and map until no opened nodes are left.
        #print(">>>>> mapAllPixels")
        #print(str(row) + "," + str(col))
        mapPixels(matrix, map, opened_nodes, h, w, value, x, )
        n_iterations = 0


def mapPixels(matrix, map, opened_nodes, h, w, value, x):
    """
    Rescursively, opens nodes and checks all surrounding nodes.
    But if maximum recursive iterations have been achieved,
    returns the node that must be opened later
    (but finishes with all nodes that have been opened already)
    """
    global n_iterations

    n_iterations += 1
    if MAX_ITERATIONS < n_iterations:
        # Do not open node, return it to open later.
        #print("mapPixels MAX_ITERATIONS")
        # print(str(row)+","+str(col))
        return

    i, j = opened_nodes[-1]

    #if map[i][j] is not None:
    #    return n_iteration
    map[i][j] = value


    #print(n_iteration)

    if DEBUG:
        print("map")
        print(x)
        print(str(i)+","+str(j))
        print(value)
        print(n_iterations)

    #row_min = i # Previous row already analyzed.
    row_min = i - 1 if 0 <= (i - 1) else i
    row_max = i + 1 if (i + 1) < h else i
    col_min = j - 1 if 0 <= (j - 1) else j
    col_max = j + 1 if (j + 1) < w else j

    if x:
        """
            X            X          X      
            X        (i  , j)   (i  , j+1)
        (i+1, j-1)   (i+1, j)   (i+1, j+1)
        """
        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                if map[row][col] is None and matrix[row][col] == "X":
                    opened_nodes.append((row, col))
                    mapPixels(matrix, map, opened_nodes, h, w, value, x)
    else:
        """
                         X
            X        (i  , j)   (i  , j+1)
                     (i+1, j)
        """
        #col_min = j
        for row in range(row_min, row_max + 1):
            if row != i:
                if map[row][j] is None and matrix[row][j] == "O":
                    opened_nodes.append((row, j))
                    mapPixels(matrix, map, opened_nodes, h, w, value, x)
            else:
                for col in range(col_min, col_max + 1):
                    if map[row][col] is None and matrix[row][col] == "O":
                        opened_nodes.append((row, col))
                        mapPixels(matrix, map, opened_nodes, h, w, value, x)

    opened_nodes.remove((i, j))



########################################################################################################################
# MAIN
########################################################################################################################

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