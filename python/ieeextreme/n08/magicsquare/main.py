"""
https://www.hackerrank.com/contests/ieeextreme-challenges/challenges/magic-square

Magic Square
Johnny designed a magic square (square of numbers with the same sum for all rows, columns and diagonals
i.e. both the  main diagonal - meaning the diagonal that leads from the top-left corner towards bottom-right corner -
and the antidiagonal - meaning the diagonal that leads from top-right corner towards bottom-left corner).
Write a program to test it.

Task
Write a program that will check if the given square is magic
(i.e. has the same sum for all rows, columns and diagonals).

Input
First line: N , the size of the square (1 <= N <= 600).
Next N lines: The square, N space separated integers pre line, representing the entries per each row of the square.

Output
First line: M , the number of lines that do not sum up to the sum of the main diagonal
(i.e. the one that contains the first element of the square).
If the Square is magic, the program should output 0.
Next M lines: A sorted (in incremental order ) list of the lines that do not sum up to the sum of the main diagonal.
The rows are numbered 1,2,...,N;
the columns are numbered -1,-2,...,-N;
and the antidiagonal is numbered zero.

Note: There is a newline character at the end of the last line of the output.
Sample Input 1
3
8 1 6
3 5 7
4 9 2

Sample Output 1
0

Sample Input 2
4
16 3 2 13
5 10 11 8
6 9 7 12
4 15 14 1

Sample Output 2
3
-2
-1
0

Explanation of Sample Output 2
The input square looks as follows: IMAGE 1

The square has
4 rows (labeled from 1 to 4 in orange) and
4 columns (labeled from -1 to -4 in green) as depicted in the image above.
The main diagonal and antidiagonal of the square are highlighted in red and blue respectively.

The main diagonal has sum = 16 + 10 + 7 +1 = 34.
The antidiagonal has sum = 13 + 11 + 9 + 4 = 37.
This is different to the sum of the main diagonal so value 0 corresponding to the antidiagonal should be reported.
Row 1 has sum = 16 + 3 + 2 + 13 = 34.
Row 2 has sum = 5 + 10 + 11 + 8 = 34.
Row 3 has sum = 6 + 9 + 7 + 12 = 34.
Row 4 has sum = 4 + 15 + 14 + 1 = 34.
Column -1 has sum = 16 + 5 + 6 + 4 = 31. This is different to the sum of the main diagonal so value -1 should be reported.
Column -2 has sum = 3 + 10 + 9 + 15 = 37. This is different to the sum of the main diagonal so value -2 should be reported.
Column -3 has sum = 2 + 11 + 7 + 14 = 34.
Column -4 has sum = 13 + 8 + 12 + 1 = 34.
Based on the above, there are 3 lines that do not sum up to the sum of the elements of the main diagonal. Since they should be sorted in incremental order, the output should be:
3
-2
-1
0
"""

import sys
#import numpy not supported in this challenge

def getSumMainDiagonal(matrix):
    """
    :param matrix:
    :return:

    main diagonal - meaning the diagonal that leads from the top-left corner towards bottom-right corner
    """
    N = len(matrix)
    col = 0
    sum = 0
    for row in range(N):
        element = matrix[row][col]
        col = col + 1
        sum = sum + element
    return sum

def getSumAntiDiagonal(matrix):
    """
    :param matrix:
    :return:

    antidiagonal - meaning the diagonal that leads from top-right corner towards bottom-left corner).
    """
    N = len(matrix)
    col = N-1
    sum = 0
    for row in range(N):
        element = matrix[row][col]
        col = col - 1
        sum = sum + element
    return sum

def getSumCol(matrix, n_col):
    sum = 0
    for n_row in range(len(matrix)):
        sum = sum + matrix[n_row][n_col]
    return sum

def getSumRow(matrix, n_row):
    return getSumList(matrix[n_row])

def getSumList(list):
    sum = 0
    for element in list:
        sum = sum + element
    return sum



def main(argv):

    lines = getInput()

    # Read size N.
    # N: size of the square (1 <= N <= 600).
    #N = int(input("N: "))
    N = int(lines[0])
    assert (1<=N and N<=600), "not 1<=N and N<=600"
    lines.pop(0)

    # Read lines.
    # N space separated integers pre line,
    # representing the entries per each row of the square.
    matrix = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(0)
        matrix.append(row)

    for row in range(len(lines)):
        #line = input("line #"+str(row+1)+": ")
        #line = inputs()
        line = lines[row].replace("\n","")
        line = line.split(" ")
        assert (len(line)==N), "not len(line)==N"
        for col in range(N):
            matrix[row][col] = int(line[col])

    # Main diagonal sum.
    sum_main_diagonal = getSumMainDiagonal(matrix)
    #print("Main diagonal sum: "+str(sum_main_diagonal))

    lines_not_sum = []

    # Anti diagonal sum.
    sum_anti_diagonal = getSumAntiDiagonal(matrix)
    #print("Anti diagonal sum: "+str(sum_anti_diagonal))
    if(sum_main_diagonal!=sum_anti_diagonal):
        lines_not_sum.append(0)

    # Rows' sum.
    for row in range(N):
        sum = getSumRow(matrix, row)
        #print("Row#"+str(row+1)+" sum: "+str(sum))
        if(sum_main_diagonal!=sum):
            lines_not_sum.append(row+1)

    # Cols' sum.
    for col in range(N):
        sum = getSumCol(matrix, col)
        #print("Col#"+str(col+1)+" sum: "+str(sum))
        if(sum_main_diagonal!=sum):
            lines_not_sum.append((col+1)*-1)

    lines_not_sum.sort()
    print(len(lines_not_sum))
    for line in lines_not_sum:
        print(line)

######################################################################################

def getInput():
    inputs = []
    for input in sys.stdin:
        inputs.append(input)
    return inputs

if __name__ == "__main__":
    main(sys.argv)