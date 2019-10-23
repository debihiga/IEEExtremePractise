#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

DEBUG = False
n_iterations = 0
# N <= 2x10^4
MAX_ITERATIONS = 40000 # Segmentation fault with 100000
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

MOD = 998244353
"""
Mod 998244353
https://codeforces.com/blog/entry/62541
https://www.geeksforgeeks.org/modulo-1097-1000000007/

"""

"""
https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
"""
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

"""
A, B: commodities
r: exchange rate
A = r*B (mod 998244353)

[(id, r, True/False), (id, r, True/False), ...]
"""
def getExchangeRates(reader):

    # N: number of given exchange rates to follow
    # 1 <= N <= 10^4
    N = readInt(reader)

    # exchange_rates = np.empty([N, N])
    # El peor caso no es NxN sino 2xNxN y no me alcanza la memoria (256MB)
    exchange_rates = {}
    for i in range(N):
        line = readString(reader)
        A, B, r = line.split(" ")
        if A not in exchange_rates:
            exchange_rates[A] = {}
        if B not in exchange_rates:
            exchange_rates[B] = {}
        exchange_rates[A][B] = int(r)
        exchange_rates[B][A] = modinv(int(r), MOD)

    return exchange_rates

def searchConnection(exchange_rates, connection, commodities, K, L):

    # Type 1
    for commodity in exchange_rates[K]:
        if commodity in exchange_rates[L]:
            if DEBUG:
                print("searchConnection")
                print(L)
                print(commodity)
            #connection.append(L)
            connection.append(commodity)
            commodities.append(commodity)
            return True

    # Type n.
    for commodity in exchange_rates[K]:
        if commodity not in commodities:
            commodities.append(commodity)
            found = searchConnection(exchange_rates, connection, commodities, commodity, L)
            if found:
                if DEBUG:
                    print("insert")
                    print(connection)
                    print(commodity)
                connection.insert(0, commodity)
                return True

    return False

########################################################################################################################
# MAIN
########################################################################################################################

def main(argv):

    reader = io.open(sys.stdin.fileno())

    exchange_rates = getExchangeRates(reader)
    #print(exchange_rates)

    # Q: number of queries.
    Q = readInt(reader)

    for i in range(Q):

        K, L = readString(reader).split(" ")

        # Check if same.
        if K == L:
            print("1")

        # Check direct.
        elif L in exchange_rates[K]:
            r = exchange_rates[K][L]
            print(r)

        # Check inverse.
        # Al pedo, porque si esta en inverse, esta en direct.
        #elif K in exchange_rates[L]:
        #    pass

        # Check conversion.
        else:
            connection = []
            commodities = []
            if DEBUG:
                print(K)
                print(L)
            commodities.append(K)
            commodities.append(L)
            searchConnection(exchange_rates, connection, commodities, K, L)

            if len(connection) == 0:
                # No relationship.
                print(-1)

            else:

                connection.insert(0, K)
                connection.append(L)
                if DEBUG:
                    print(connection)

                total_r = 1
                for i in range(len(connection)-1):
                    r = exchange_rates[connection[i]][connection[i+1]]
                    #print(r)
                    #print(is_direct)
                    #print(total_r)
                    total_r = (total_r * r) % MOD

                exchange_rates[K][L] = total_r
                exchange_rates[L][K] = modinv(total_r, MOD)
                print(total_r)

if __name__ == "__main__":
    main(sys.argv)