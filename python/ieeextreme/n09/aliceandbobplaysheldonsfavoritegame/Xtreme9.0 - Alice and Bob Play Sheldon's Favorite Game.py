#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io
import math

DEBUG = False

def readString(reader):
    return reader.readline().replace("\n","")

def readInt(reader):
    line = reader.readline().replace("\n","")
    return int(line)

"""
[AliceShape] [BobShape] [n]
Where
    [AliceShape] is the shape that Alice will choose in the first game of the series.
    [BobShape] is the shape that Bob will choose in the first game of the series.
    [n] is an integer, 1 <= n <= 10^18, indicating how many games Alice and Bob will play in the series.
"""
def getTestcase(reader):
    line = readString(reader)
    parameters = line.split(" ")
    alice_shape = parameters[0]
    bob_shape = parameters[1]
    n = int(parameters[2])
    return alice_shape, bob_shape, n

shapes = {  "rock":         0,
            "paper":        1,
            "lizard":       2,
            "spock":        3,
            "scissors":     4}

def run(alice_shape, bob_shape, n):

    alice_win_games = 0
    bob_win_games = 0
    tied_games = 0

    matches = []

    for i in range(n):

        match = match_table[alice_shape][bob_shape]

        if match not in matches:
            matches.append(match)
            (alice_shape, bob_shape, winner) = match
            if winner==0:
                alice_win_games += 1
            elif winner==1:
                bob_win_games += 1
            elif winner==-1:
                tied_games += 1

        else:
            # Is already a match.
            j = matches.index(match)
            cycle = matches[j:]
            """
            [(4, 3, -1), (2, 0, 1), (1, 3, 1), (1, 1, 0)]
            [(2, 1, 0), (2, 3, 0)]
              ^ current result.
            """
            #print("Cycle!")

            alice_win_games_in_cycle = 0
            bob_win_games_in_cycle = 0
            tied_games_in_cycle = 0
            for c in cycle:
                if c[2] == 0:
                    alice_win_games_in_cycle += 1
                elif c[2] == 1:
                    bob_win_games_in_cycle += 1
                elif c[2] == -1:
                    tied_games_in_cycle += 1

            remaining = n-i
            if DEBUG:
                print("remaining")
                print(i)
                print(n)
                print(remaining)

            n_periods = math.floor(remaining//len(cycle))
            if DEBUG:
                print("n_periods")
                print(n_periods)

            alice_win_games += ((n_periods)*alice_win_games_in_cycle)
            bob_win_games += ((n_periods)*bob_win_games_in_cycle)
            tied_games += ((n_periods)*tied_games_in_cycle)

            for alice_shape, bob_shape, winner in cycle[:remaining % len(cycle)]:
                if winner == 0:
                    alice_win_games += 1
                elif winner == 1:
                    bob_win_games += 1
                elif winner == -1:
                    tied_games += 1

            break

    if alice_win_games == bob_win_games:
        printTieResult(alice_win_games, tied_games)
    elif alice_win_games < bob_win_games:
        printWinResult("Bob", bob_win_games, tied_games)
    else:
        printWinResult("Alice", alice_win_games, tied_games)

"""
Output will consist of a single line in the appropriate one of the following forms:

1) [Player] wins, by winning [WinGames] game(s) and tying [TieGames] game(s)
2) Alice and Bob tie, each winning [WinGames] game(s) and tying [TieGames] game(s)

where
    [Player] is the name of the player with more wins (either "Alice" or "Bob")
    [WinGames] is the number of games won either by the winner or, in the case of a tie, by each player
    [TieGames] is the number of games in which the players tied

Notes:
    The output is case sensitive. 
    The player names, for example, must be either "Alice" or "Bob". Neither "alice" nor "BOB" will be acceptable.
    The words are separated by a single space, 
    and there are no spaces before the first word in the line, 
    nor after the last word in the line.
"""
def printWinResult(Player, WinGames, TieGames):
    print(Player+" wins, by winning "+str(WinGames)+" game(s) and tying "+str(TieGames)+" game(s)")
def printTieResult(WinGames, TieGames):
    print("Alice and Bob tie, each winning "+str(WinGames)+" game(s) and tying "+str(TieGames)+" game(s)")

match_table = [[(1, 3, -1), (4, 3, 1),  (0, 3, 0),  (2, 0, 1),  (0, 3, 0)],
               [(1, 3, 0),  (4, 3, -1), (0, 3, 1),  (1, 1, 0),  (3, 3, 1)],
               [(1, 3, 1),  (2, 3, 0),  (0, 3, -1), (2, 1, 0),  (3, 3, 1)],
               [(3, 3, 0),  (4, 3, 1),  (0, 3, 1),  (2, 2, -1), (3, 3, 0)],
               [(1, 3, 1),  (4, 3, 0),  (4, 3, 0),  (2, 0, 1),  (3, 3, -1)]]
"""
[[(1, 3, -1), (4, 3, 1), (0, 3, 0), (2, 0, 1), (0, 3, 0)], 
[(1, 3, 0), (4, 3, -1), (0, 3, 1), (1, 1, 0), (3, 3, 1)], 
[(1, 3, 1), (2, 3, 0), (0, 3, -1), (2, 1, 0), (3, 3, 1)], 
[(3, 3, 0), (4, 3, 1), (0, 3, 1), (2, 2, -1), (3, 3, 0)], 
[(1, 3, 1), (4, 3, 0), (4, 3, 0), (2, 0, 1), (3, 3, -1)]]

"""
"""
cycles_table = [[None, None, None, None],
                [None, [(4, 3, -1), (2, 0, 1), (1, 3, 1), (1, 1, 0)], None, [(1, 1, 0), (4, 3, -1), (2, 0, 1), (1, 3, 1)]],
                [[(1, 3, 1), (1, 1, 0), (4, 3, -1), (2, 0, 1)], [(2, 3, 0), (2, 1, 0)], None, [(2, 1, 0), (2, 3, 0)]],
                [None, None, None, None],
                [None, None, None, [(2, 0, 1), (1, 3, 1), (1, 1, 0), (4, 3, -1)]]]
a = [[None, None, None, None],
     [None, [(4, 3, -1), (2, 0, 1), (1, 3, 1), (1, 1, 0)], None, [(1, 1, 0), (4, 3, -1), (2, 0, 1), (1, 3, 1)]],
     [[(1, 3, 1), (1, 1, 0), (4, 3, -1), (2, 0, 1)], [(2, 3, 0), (2, 1, 0)], None, [(2, 1, 0), (2, 3, 0)]],
     [None, None, None, None],
     [None, None, None, [(2, 0, 1), (1, 3, 1), (1, 1, 0), (4, 3, -1)]]]
"""



"""
cycles_table = [[[],                                [],                                 [], []],
                [[],                                [(4, 3), (2, 0), (1, 3), (1, 1)],   [], [(1, 1), (4, 3), (2, 0), (1, 3)]],
                [[(1, 3), (1, 1), (4, 3), (2, 0)],  [(2, 3), (2, 1)],                   [], [(2, 1), (2, 3)]],
                [[],                                [],                                 [], []],
                [[],                                [],                                 [], [(2, 0), (1, 3), (1, 1), (4, 3)]]]
"""

def main(argv):

    reader = io.open(sys.stdin.fileno())

    """
    t, 1 <= t <= 50, 
    number of test cases in the input.
    """
    t = readInt(reader)

    for i in range(t):
        alice_shape, bob_shape, n = getTestcase(reader)
        run(shapes[alice_shape.lower()], shapes[bob_shape.lower()], n)

if __name__ == "__main__":
    main(sys.argv)