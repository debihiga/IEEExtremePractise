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
Mod 998244353
https://codeforces.com/blog/entry/62541
"""

"""
Each entry will follow a format described in the Xplore API website: 
developer.ieee.org/docs/read/Metadata_API_responses
"""

"""
The IEEE Xplore Application Programming Interface (API) is an efficient 
data delivery vehicle for content indexing/discovery as well as 
text and data mining of IEEE metadata content of academic publications. 
Loading a database/repository using the content delivered by the IEEE API can be subsequently used to 
draw domain/subject relationships, data analytics, and various other use cases for researchers. 
To learn more about the IEEE Xplore API please visit developer.ieee.org and register for an API key. 
All participants of the IEEEXtreme 12.0 competition will have access to the IEEE API during and after the competition, 
for a limited period of time, to discover its research utility potential.

A useful metric commonly associated with academic publishing is the h-index. 
An author with an index of h has published 
h papers each of which has been 
cited in other papers at least h times.

For this challenge, 
write a program that reads a set of N entries from the Xplore database, in a JSON format, 
and prints the top 10 author names followed by the their h-index. 
The authors should be raked by h-index and by alphabetical order in case of an h-index tie.


Standard output
Print the authors ranked by their h-index followed by a space and by the h-index itself. 
The authors should be ranked alphabetically if there are ties.

Constraints and notes
2 \leq N \leq 100002≤N≤10000 

"""
import json

########################################################################################################################
# MAIN
########################################################################################################################

def main(argv):

    reader = io.open(sys.stdin.fileno())

    # N: number of articles
    # 2 <= N <= 10000
    N = readInt(reader)

    authors = {}
    authors_h = {}

    for i in range(N):

        json_data = json.loads(readString(reader))
        #print(json_data)

        #article_number = json_data["article_number"]
        #print(article_number)

        citing_paper_count = json_data["citing_paper_count"]
        #print(citing_paper_count)

        authors_json = json_data["authors"]["authors"]
        for author in authors_json:
            name = author["full_name"]
            if name not in authors:
                authors[name] = []
            aux = authors[name]
            aux.append(citing_paper_count)
            authors[name] = aux

    for name in authors.keys():
        aux = authors[name]
        authors[name] = sorted(aux, reverse=True)
        authors_h[name] = 0
        for n_article in range(len(authors[name])):
            if n_article < authors[name][n_article]:
                authors_h[name] = n_article + 1

    authors_h_list = list(authors_h.items())
    authors_h_list.sort(key=lambda x: (-x[1],) + x[:1])

    for author in authors_h_list:
        print(author[0]+" "+str(author[1]))
    #print(authors)

if __name__ == "__main__":
    main(sys.argv)