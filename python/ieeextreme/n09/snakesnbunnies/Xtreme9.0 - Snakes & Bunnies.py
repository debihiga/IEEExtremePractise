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

n_recursive_cycles_threshold = 0
n_recursive_cycles = 0
evil_cycle_achieved = False

"""
The following N lines contain the game-board configuration: 
each line contains N characters, 
and each character represents a square of the board. 

1) The character '-' represents a normal square, 
i.e. one with no snake heads/tails nor bunny feet/ears depicted on it; 

2) Digits (0-9) represent bunnies 
Given a pair of identical digits representing a bunny in two numbered squares, 
the feet of the bunny is located in the square with the lower number, 
and the ears are located in the square with the higher number.

3) Letters (a-z) represent snakes. 
Given a pair of identical letters representing a snake in two numbered squares, 
the head of the snake are located in the square with the higher number, 
and the tail is located in the square with the lower number. 

There can be at most 10 bunnies and 26 snakes, 
and each represented by an appropriate pair of digits or letters. 

No square has two or more snake's heads/tails or bunny's ears/feet on it; 
there is at most one special drawing for each cell. 
Moreover, the last square is always free of drawings.
"""
def getGameBoard(reader, N):

    specials_squares = []

    gameboard = []
    # Get full gameboard
    for i in range(N):
        if i%2==0:
            row = reversed(readString(reader))
        else:
            row = readString(reader)
        for square in row:
            gameboard.append(square)

    gameboard = list(reversed(gameboard))
    #print(gameboard)

    # Get specials
    for i in range(len(gameboard)):
        square = gameboard[i]
        # Bunny
        if square.isdigit():
            indices = getIndices(gameboard, square)
            gameboard[indices[0]] = "-"
            gameboard[indices[1]] = "-"
            specials_squares.append((indices[0]+1, indices[1]+1))
        # Snake
        elif square.isalpha():
            indices = getIndices(gameboard, square)
            gameboard[indices[0]] = "-"
            gameboard[indices[1]] = "-"
            specials_squares.append((indices[1]+1, indices[0]+1))
        # Normal
        else:
            pass

    if DEBUG:
        print(specials_squares)
    return specials_squares

def getIndices(list, element):
    return [i for i, value in enumerate(list) if value==element]

def movePlayer(n_player, n_squares, players, specials_squares):

    global evil_cycle_achieved

    players[n_player] = players[n_player] + n_squares
    if DEBUG:
        print(players[n_player])

    global n_recursive_cycles
    n_recursive_cycles = 0
    removed = True
    while removed:
        checkSquareTaken(players, n_player)
        if not evil_cycle_achieved:
            removed = checkSpecialsSquares(players, n_player, specials_squares)
        else:
            break

"""
3) If a square is already taken by another player’s token, 
then the current player’s token moves forward to the next square not occupied by a token.
"""
def checkSquareTaken(players, current_player):

    global n_recursive_cycles_threshold
    global n_recursive_cycles
    global evil_cycle_achieved

    another_player = getIndices(players, players[current_player])
    if DEBUG:
        print("checkSquareTaken")
        print(another_player)
        print(players)
    if n_recursive_cycles_threshold<n_recursive_cycles:
        #print("checkSquareTaken Evil Cycle!")
        evil_cycle_achieved = True
        return
    elif len(another_player)==2:
        if DEBUG:
            print("Square already token by "+str(another_player[0]))
        players[current_player] += + 1
        n_recursive_cycles += 1
        checkSquareTaken(players, current_player)

"""
4) If the final position of a player’s token is a square with the head of a snake, 
then it must be moved backwards to the square corresponding to the snake’s tail. 
Similarly, if the token ends on a square with bunny’s feet, 
it goes to the top of the bunny’s ears.
"""
def checkSpecialsSquares(players, n_player, specials_squares):

    current_square = players[n_player]
    #print("checkSpecialsSquares")
    #print(current_square)

    for square in specials_squares:
        #print(square)
        if current_square == square[0]:
            """
            If a player lands on the tail of snake or the ears of a bunny, the player does not make any special moves.
            """
            players[n_player] = square[1]
            if DEBUG:
                print("Special square!")
                print(square)
                print("Moved to "+str(players[n_player]))
            return True

    return False

def getDices(reader, is_aditional_turn):
    if not is_aditional_turn:
        dice_1 = readInt(reader)
        if dice_1 is None:
            dice_1 = 0
        dice_2 = readInt(reader)
        if dice_2 is None:
            dice_2 = 0
        if dice_1 == dice_2:
            """
            2) If the dice roll is a double, then the player has an additional turn just after the current one. 
            Note that the additional turn begins after applying the additional rules below. 
            The additional turn follows the same rules of standard turns, 
            except that only one die can be rolled.
            """
            return dice_1+dice_2, True
        else:
            return dice_1+dice_2, False
    else:
        dice = readInt(reader)
        if dice is None:
            dice = 0
        return dice, False

def main(argv):

    reader = io.open(sys.stdin.fileno())

    """
    N (1 < N < 100 and N is odd) 
    dimension of the game-board.
    Ordered row-wise from the bottom-left to the top-right 
    """
    N = readInt(reader)
    final_position = N*N
    if DEBUG:
        print(N)
    global n_recursive_cycles_threshold
    global evil_cycle_achieved
    n_recursive_cycles_threshold = final_position

    specials_squares = getGameBoard(reader, N)

    """
    M (2 <= M <= 10), 
    number of players.
    """
    M = readInt(reader)
    #print(M)

    players = []
    for i in range(M):
        players.append(0)

    n_player = 0
    aditional_turn = False

    while True:

        #print("Player#"+str(n_player))
        n_squares = 0

        """
        1) Two standard 6-faced die are rolled by the player and his/her game piece moves forward on the board, 
        following the square's numbers. 
        The piece is advanced by a number of squares equal to the sum of the die.
        """
        n_squares, aditional_turn = getDices(reader, aditional_turn)
        if n_squares == 0:
            break

        """
        The given sequence of dice rolls may not always lead a game to an end. 
        There will be no extra dice rolls after a game has ended. 
        There will always be sufficient dice roles for a player to complete their turn.
        """
        """
        while dice_2==dice_3:
            dice_3 = readInt(reader)
            if dice_3 is None:
            #    break
                dice_3 = 0
            n_squares += dice_3
        """
        #print("Dices: "+str(dice_1)+" "+str(dice_2)+" "+str(dice_3))
        #n_squares = dice_1 + dice_2 + dice_3
        #print("Total: "+str(n_squares))
        movePlayer(n_player, n_squares, players, specials_squares)
        player_position = players[n_player]
        #print("Final position: "+str(player_position))



        """
        The given sequence of dice rolls may not always lead a game to an end. 
        """
        if final_position<=player_position:
            """
            5) Game ends when a player arrives at the last square or when a player can move over the last square 
            (for example if the player is on the second-to-last square and rolls 3+4). 
            In this latter case, the player stops on the last square and wins.
            """
            players[n_player] = final_position
            break
        if evil_cycle_achieved:
            break

        if not aditional_turn:
            n_player += 1
            aditional_turn = False
        if n_player%M==0:
            n_player = 0

        #print("")


    """
    Note that infinite loops can happen while a player moves: 
    this is the EVIL CYCLE case! When it happens, 
    the game ends and the player in the evil cycle wins the game.
    """

    # Output
    if not evil_cycle_achieved:
        """
        The output is a single line containing M integers separated by a blank space. 
        The first integer is the final position on the game-board of the first player (i.e. the one who rolled the dice first), 
        the second integer is the final position of the second player, etc.
        """
        output = " ".join([str(i) for i in players])
        print(output)
    else:
        """
        In case of evil cycle, the output is a single line containing the string 
        “PLAYER x WINS BY EVIL CYCLE!”, 
        where x is the player number (1 to M).
        """
        print("PLAYER "+str(n_player+1)+" WINS BY EVIL CYCLE!")

if __name__ == "__main__":
    main(sys.argv)