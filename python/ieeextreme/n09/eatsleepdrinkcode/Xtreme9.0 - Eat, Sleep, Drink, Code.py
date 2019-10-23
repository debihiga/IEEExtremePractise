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

# https://stackoverflow.com/questions/24101524/finding-median-of-list-in-python
def median(list):
    n = len(list)
    if n<1:
        return None
    if n%2==1:
        return sorted(list)[n//2]
    else:
        return sum(sorted(list)[n//2-1:n//2+1])/2.0

"""
Alice starts the competition with a certain energy level. 

She can only attempt a problem if her energy level prior to starting the problem is 
greater than or equal to the energy required by the problem. 

Furthermore, if she attempts to solve the problem, 
her energy level after the hour is reduced by the energy required by the problem.

Alice wants you to assume that every hour a problem is released, 
and she can make the following decisions:
1) Attempt to solve the problem. 
She is able to accurately predict how many points she will earn by attempting the problem.
2) Skip the problem and sleep. 
Note that she will not come back to this problem later. 
She will gain a fixed amount of energy by doing so.
3) Drink a caffeinated cola and attempt the problem, if she has drinks remaining. 
She will gain a fixed amount of energy immediately. 
She can only choose this option if her resulting current energy level would be 
greater than or equal to the energy level required by the problem. 
As usual she will expend the energy required to solve the problem. 
In addition, as the caffeine wears off, 
she will lose a certain amount of energy units exactly two hours later.

Notes:

It is ok for her energy level to become negative after losing the points due to the cola consumption.
However, she will need to boost her energy by sleeping or drinking additional cola 
before she will be able to solve a problem.

She can only drink one cola per hour.

If she drinks a cola, she must attempt the problem.

For each hour that she sleeps and skips a problem, 
she gains the fixed amount of energy. 
Thus, if she sleeps for two consecutive hours, 
she will gain twice as much energy as if she slept for one hour. 
If she sleeps for three consecutive hours, 
she will gain three times as much energy, etc.
"""
def main(argv):

    reader = io.open(sys.stdin.fileno())
    """
    The first line of input contains an integer k, 1 <= k <= 20, 
    which indicates how many test cases are present.
    """
    k = readInt(reader)
    """
    Each test case then has the following format. 
    The first line of the test case consists of the following:
    [Hours] [Energy] [Sleep] [DrinkCount] [Drink] [Crash]
    Where
    [Hours] gives the length of the contest in hours, 
        1 <= [Hours] <= 168. 
        (Alice envisions the day when Xtreme is a week-long contest!)
    [Energy] is Alice’s energy level at the beginning of the contest, 
        0 <= [Energy] <= 107.
    [Sleep] is the amount of energy that Alice gains by skipping a problem and sleeping, 
        1 <= [Sleep] <= 106.
    [DrinkCount] is a count of colas that Alice has at the start of the contest, 
        0 <= [DrinkCount] <= 24.
    [Drink] is the initial boost that Alice receives from drinking a cola, 
        1 <= [Drink] <= 106.
    [Crash] is the amount of additional energy that Alice loses two hours after drinking a cola, 
        1 <= [Crash] <= 106.
    """
    """
    Then there follow [Hours] lines, 
        each describing a problem, 
        and listed in the order in which the problem is released, 
        i.e. the problem on the first line is released at the start of the contest, 
        the second problem is released one hour later, 
        the third problem is released an hour after that, etc. 
        These lines have the following format:
    [EnergyRequired] [Points]
    Where
    [EnergyRequired] is an integer equal to the amount of energy that Alice 
        will expend in attempting to solve the problem, 
        1 <= [EnergyRequired] <= 107.
    [Points] is equal to the points that Alice will earn if she attempts the problem. 
        [Points] will be equal to an integer chosen from the following set 
        {10, 20, 30, 40, 50, 60, 70, 80, 90, 100}.
    """

if __name__ == "__main__":
    main(sys.argv)