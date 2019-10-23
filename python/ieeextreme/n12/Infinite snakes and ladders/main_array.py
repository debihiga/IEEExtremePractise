#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

DEBUG = False

def readString(reader):
    return reader.readline().replace("\n","")

def readInt(reader):
    line = reader.readline().replace("\n","")
    if line=="":
        return None
    else:
        return int(line)

"""

"""
def getGameBoard(reader, N):

    specials_squares = {}

    # S: number of snakes
    S = readInt(reader)
    for i in range(S):
        positions = readString(reader).split(" ")
        col = int(positions.pop(0))
        row = int(positions.pop(0))
        i = coordinates2Position(col, row, N)
        col = int(positions.pop(0))
        row = int(positions.pop(0))
        f = coordinates2Position(col, row, N)
        specials_squares[i] = f

    # L: number of ladders
    L = readInt(reader)
    for i in range(L):
        positions = readString(reader).split(" ")
        col = int(positions.pop(0))
        row = int(positions.pop(0))
        i = coordinates2Position(col, row, N)
        col = int(positions.pop(0))
        row = int(positions.pop(0))
        f = coordinates2Position(col, row, N)
        specials_squares[i] = f

    return specials_squares

def coordinates2Position(col, row, N):
    position = N * (row - 1)
    if row%2 == 1:
        position += (col - 1)
        return position
    else:
        position += (N - col)
        return position

def position2Coordinates(position, N):
    if position < -1:
        return "0 1"
    if ((N * N) + 1) <= position:
        return "winner"
    row = int(position // N) + 1
    col = position - (N * (row - 1))

    if row%2 == 1:
        col = col + 1
    else:
        col = N - col
    return str(col) + " " + str(row)

def movePlayer(n_player, n_squares, players, specials_squares, final_position):

    players[n_player] = players[n_player] + n_squares
    #if DEBUG:
    #    print(players[n_player])

    if final_position <= players[n_player]:
        return

    """
    If after following a ladder or a snake, 
    a player ends up at a position with a ladder start or a snake head, 
    they must follow it as well. 
    However, there will be no infinite loops of ladders and snakes.
    """
    moved = True
    while moved:
        moved = checkSpecialsSquares(players, n_player, specials_squares, final_position)

"""
4) If the final position of a player’s token is a square with the head of a snake, 
then it must be moved backwards to the square corresponding to the snake’s tail. 
Similarly, if the token ends on a square with bunny’s feet, 
it goes to the top of the bunny’s ears.
"""
def checkSpecialsSquares(players, n_player, specials_squares, final_position):

    #if final_position <= players[n_player]:
    #    return False

    if players[n_player] in specials_squares:
        """
        If a player lands on the tail of snake or the ears of a bunny, the player does not make any special moves.
        """
        players[n_player] = specials_squares[players[n_player]]
        if DEBUG:
            print("Special square!")
            #print(square)
            print("Moved to "+str(players[n_player]))
        return True

    return False

def getDices(reader):
    dice_1, dice_2 = readString(reader).split(" ")
    return int(dice_1) + int(dice_2)

def getNextPlayer(current_player, players, final_position):

    next_player = current_player + 1
    if next_player % len(players) == 0:
        next_player = 0

    """
    When a player has already won, 
    skip their turn and use their dice rolls for the players still in the game. 
    If every player has already won, the remaining dice rolls are unused.
    """
    while final_position <= players[next_player]:
        next_player += 1
        if next_player == (current_player + 1): # ya recorrio todos
            return None
        if next_player % len(players) == 0:
            next_player = 0

    return next_player

def main(argv):

    reader = io.open(sys.stdin.fileno())

    """
    N: dimension of the game-board.
    4 <= N <= 10^6
    N always even
    Ordered row-wise from the bottom-left to the top-right 
    """
    N = readInt(reader)
    final_position = (N * N) + 1
    #if DEBUG:
    #    print(N)

    """
    M (2 <= M <= 10), 
    number of players.
    """
    M = readInt(reader)
    #print(M)
    players = {}
    for i in range(M):
        players[i] = -1

    specials_squares = getGameBoard(reader, N)
    #print(specials_squares)

    # K: number of dice pairs
    K = readInt(reader)
    if DEBUG:
        K = 5

    n_player = 0

    for i in range(K):

        """
        1) Two standard 6-faced die are rolled by the player and his/her game piece moves forward on the board, 
        following the square's numbers. 
        The piece is advanced by a number of squares equal to the sum of the die.
        """
        n_squares = getDices(reader)
        if DEBUG:
            print("n_squares")
            print(n_squares)

        movePlayer(n_player, n_squares, players, specials_squares, final_position)

        n_player = getNextPlayer(n_player, players, final_position)
        if n_player is None:
            if DEBUG:
                print("All already won!")
            break

    for i in range(M):
        print(str(i+1)+" "+position2Coordinates(players[i], N))

if __name__ == "__main__":
    main(sys.argv)