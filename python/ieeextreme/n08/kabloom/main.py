#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

DEBUG = True

def readString(reader):
    return reader.readline().replace("\n","")

def readInt(reader):
    line = reader.readline().replace("\n","")
    if line=="":
        return None
    else:
        return int(line)

def main(argv):

    reader = io.open(sys.stdin.fileno())

if __name__ == "__main__":
    main(sys.argv)