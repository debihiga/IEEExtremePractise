#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

def readString(reader):
    return reader.readline().replace("\n","")

def readInt(reader):
    return int(reader.readline().replace("\n",""))

def main(argv):


    reader = io.open(sys.stdin.fileno())

    """
    1 <= n <= 100, 
    columns each character will use when printed "zoomed-in".
    """
    n = readInt(reader)
    #print(n)
    """
    1 <= m <= 100, 
    rows each character will use when printed "zoomed-in". 
    """
    m = readInt(reader)
    #print(m)
    """
    3 <= k <= 95, 
    characters may need to be translated.
    """
    k = readInt(reader)
    #print(k)

    descriptions = {}
    for i in range(k):
        character = readString(reader)
        description = []
        for j in range(m):
            description.append(readString(reader))
        descriptions[character] = description
        #print(descriptions[character])

    """
    1 <= x <= 500.
    """
    x = readInt(reader)
    for i in range(x):

        matrix = []
        for row in range(m):
            matrix.append([])

        line = readString(reader)
        for character in line:
            #print(character)
            for row in range(m):
                #print(descriptions[character])
                matrix[row].append(descriptions[character][row])

        # Print zoomed.
        for row in matrix:
            print("".join(row))

if __name__ == "__main__":
    main(sys.argv)