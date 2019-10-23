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

"""
Greatest Common Divisor (GCD)
http://en.wikipedia.org/wiki/Greatest_common_divisor
The GCD of k numbers say [n1,n2,n3… nk] is the 
largest positive integer that divides all these numbers without any remainder. 

Minka has N (1 <= N <= 10^5) balls and there is a number 
V (1 <= V <= 10^4) written on every ball. 

Now Minka has to perform Q queries, 
and in each query he wants to know the number of possible ways 
he can choose balls out of the N balls, 
so that GCD of the numbers written on the chosen balls equals to the number X of each query. 
Although he already knows the answer for each query, 
he would still like you to check if you can also find answer to his queries. 
Since number of ways can be very large, your program should output the number of ways modulus 10^9+7. 
Notes: 
1) There can be at most 100 distinct numbers written on N balls. 
2) By definition, the GCD is only defined for 2 or more numbers. 
For this problem, however, we will consider that the GCD of a single number 
may also defined and in such case the GCD of a single number will be equal to the number itself 
(i.e. the GCD of 2 is 2. Please refer to the explanation of Sample Input 1 for more details).
"""

def getV(reader):
    # Vi: number written on the ith ball.
    # 1 <= Vi <= 10^4
    V_aux = readString(reader).split(" ")
    V_aux.pop() # Remove "\n"
    # N = len(V)
    V = []
    for i in V_aux:
        V.append(int(i))
    return V

"""
v: V without repetitions
w: number of repetitions
"""
def getv(V):
    # Note 1: There can be at most 100 distinct numbers written on N balls.
    v = []
    w = {}
    for i in V:
        if i not in v:
            v.append(i)
            w[str(i)] = 1
        else:
            w[str(i)] += 1
    return v, w

def getGCDPairs(v):
    """
    gcd(a, b) = X
    C(100, 2) = 4950 <- obligatorio (y es la cantidad de pares maxima posible)
    Pares que cumplen:
    (a1, b1) (a2, b2) ... (an, bn)

    3 5 6 8 10
    2 = gcd(6, 8) = gcd(6, 10) = gcd(8, 10) -> n = 3
    15 20 25 47 90
    5 = gcd(15, 20) = gcd(15, 25) -> n = 2
    """

    pass

def main(argv):

    reader = io.open(sys.stdin.fileno())

    # N: number of balls.
    # 1 <= N <= 10^5
    N = readInt(reader)

    # Vi: number written on the ith ball.
    # 1 <= Vi <= 10^4
    V = getV(reader)
    print(V)

    # Note 1: There can be at most 100 distinct numbers written on N balls.
    v, w = getv(V)
    print(v)
    print(w)

    """
    https://www.wyzant.com/resources/lessons/math/precalculus/factorials_permutations_and_combinations
    Combinations:
    Groups from 1 to 100 items.
    1 <= n <= 100
    1 <= r <= 100
    nCr = C(n,r)
    C(100,100) = 1
    C(100C,1) = 100
    C(100,50) = 100891344545564193334812497256
    Nop, no puedo andar calculando a mano las combinaciones.
    Ni tampoco tenerlas calculadas de prepo.
    C(100,2) = 4950
    Encuentro los pares y armo los grupos de 3 a 100.
    https://www.geeksforgeeks.org/gcd-two-array-numbers/
    https://www.sparknotes.com/math/prealgebra/wholenumbers/section4/
    
    

    
    gcd(a, b, c) = gcd(gcd(a, b), c) = gcd(X, c) = X
    C(100, 2) = 4950
    gcd(a, b, c, d) = gcd(gcd(a, b, c), d) = gcd(X, d) <- ya lo hice antes con gcd(X, c)
    Pares que cumplen:
    (X, c1) (X, c2) ... (X, cm)
    
    Armo:
    (a1, b1, c1) (a1, b1,c2) ... (a1, b1, cm)
    (a2, b2, c1) (a2, b2,c2) ... (a2, b2, cm)
    ...
    (an, bn, c1) (an, bn,c2) ... (an, bn, cm)
    
    d11 d12 ... d1m
    d21 d22 ... d2m
    ...
    dn1 dn2 ... dnm
    
    Luego:
    -         (d11,c2) ... (d11, cm)
    (d12, c1) -        ... (d21, cm)
    ...
    (d1m, c1)
    
    n pares gcd(a, b)
    m pares gcd(X, c)
    n * m grupos de 2
    
    
    3 5 6 8 10
    2 = gcd(6, 8) = gcd(6, 10) = gcd(8, 10) -> n = 3
    2 = gcd(2, 6) = gcd(2, 8) = gcd(2, 10) -> m = n = 3 (no siempre)
    6 8 10
    C(3, 2) = 3
    C(3, 3) = 1
    -> 4 posibilidades
    
    15 20 25 30 47 90 100
    5 = gcd(15, 20) = gcd(15, 25) = gcd(20, 25) = gcd(25, 30) -> n = 4
    5 = gcd(5, 15) = gcd(5, 20) = gcd(5, 25) = gcd(5, 30) = gcd(5, 90) = gcd(5, 100) -> m = 6
    90 100 (descartando a los de la otra lista)
    (15, 20)
    (15, 25)
    
    1) Calculo el GCD para los 100 numeros
    2) Armo el array de los que cumplen + sus repeticiones
    3) Calculo la combinatoria
    
    Una vez que tengo los pares,
    (a, b) (c, d)
    armo los grupos
    C(4, 2) = 6 -> (a, b) (a, c) (a, d) (b, c) (b, d) (c, d)
    
    (a, b, c)
    (a, b, d)
    (b, c, d)
    
    
    """

    # Q: number of GCD queries that will have to be performed.
    # 1 <= Q <= 10^4
    Q = readInt(reader)

    for i in range(Q):

        # X: GCD of each query
        # 1 <= X <= 10^4
        X = readInt(reader)
        print(X)

    """
    Your program should output the number of ways modulus 10^9+7 that balls can be drawn from the set, so that their GCD equals the number X corresponding to each query. 
Note: There is a newline character at the end of the last line of the output.
    """
if __name__ == "__main__":
    main(sys.argv)