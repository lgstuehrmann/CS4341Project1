# Script for development and testing of the minimax algorithm for Project 1.
# Will use symmetry to prune identical game boards from the search tree.
#

import numpy as np
from time import sleep

from __builtin__ import file

import referee
import tester
import os.path
from threading import Thread, Timer

# Global Variable Total_Score keeps track of the known score of the board
Total_Score = 0


# alpha_beta class containing alpha beta values
class alpha_beta:
    def __init__(self, alpha, beta):
        self.a = alpha
        self.b = beta


# move class with columns and rows
class move:
    def __init__(self, column, row, player):
        self.c = column
        self.r = row
        self.p = player


"""
This is the algorithm that looks for the best move for the program to make
by evaluating the states of the board
input: the current state of the gomoku board
output: the move that our program should make 
"""


def minimax(board_state):
    # get list of possible moves ***(later fixed to smaller list)
    moves = board_state.get_available_moves()
    best_move = moves[0]
    max_depth = 4
    alpha_beta = alpha_beta(float("-inf"), float("inf"))
    for m in moves:
        # reset temp_Total to Total_Score
        global Total_Score
        temp_total = Total_Score
        # clone the state of the board with that possible move
        clone = board_state.next_board(m)
        # Still need board_score function
        temp_total += clone.board_score(m)
        # Now look at the move options available to the min player and get score
        score = min_move(clone, max_depth, alpha_beta, temp_total)
        # check to see if the move is the best move based on score knowledge
        if score > alpha_beta.a:
            best_move = m
            alpha_beta.a = score
    # Before returning move, add board score change made by best_move
    global Total_Score
    Total_Score += clone.board_score(best_move)
    return best_move


"""
input: the board state after the opponent makes a move, max depth, 
alpha beta values, and temporary total board score
output: the "score" of the move that the min player will make based
on a heuristic function we have yet to write
"""


def min_move(board_state, max_depth, alpha_beta, temp_total):
    max_depth -= 1
    # list of the moves available to the opponent
    moves = board_state.get_available_moves()
    for m in moves:
        clone = board_state.next_board(m)
        # subtract value of opponent mve from board score val
        temp_total -= clone.board_score(m)
        if max_depth == 0:
            return temp_total
        else:
            score = max_move(clone, max_depth, alpha_beta, temp_total)
            if score < alpha_beta.b:
                alpha_beta.b = score
            return alpha_beta.b


"""
input: the board state after the opponent makes a move, max depth, 
alpha beta values, and temporary total board score
output: the "score" of the move that the max player will make
might make based on a heuristic function we have yet to write
"""


def max_move(board_state, max_depth, alpha_beta, temp_total):
    max_depth -= 1
    # list of the moves available to the player after opponent moves
    moves = board_state.state.get_available_moves()
    for m in moves:
        clone = board_state.next_board(m)
        temp_total += clone.board_score(m)
        if max_depth == 0:
            return temp_total
        else:
            score = min_move(clone, max_depth, alpha_beta, temp_total)
            if score > alpha_beta.a:
                alpha_beta.a = score
            return alpha_beta.a


# *** Following funnctions inside the yet to be made board class
"""
input: the current state of the board & the team who moves next
output: a list of all possible moves that the program should consider
"""


def get_available_moves(currBoard, team):
    stack = list
    if team == "white":
        marker = 'X'
    else:
        marker = 'O'
    for each in currBoard.x:
        for one in currBoard.y:
            if isOccupied(currBoard, each, one):
                break
            else:
                potentialMove = referee.Move(marker, each, one)
                stack += potentialMove

    return stack


"""
input: current board, x and y coordinates of the global current board
returns true if the current position has a marker
returns false otherwise
"""


def isOccupied(currBoard, x, y):
    index = (x, y)
    if referee.GomokuBoard.isFieldOpen(currBoard, index):
        check = False
    else:
        check = True
    return check


"""
input: a possible move that the board wants to put into play
output: a board state where the specified move has been added to the new board_state
"""


def next_board(move):
    return 1


"""
determine the "score" of the board 
input: the state of the board and the last move made
output: the score difference that the specified move made on the board
"""


def board_score(currBoard, move):
    # restrict range to 0 - boardsize
    xMin = max(move.c - 5, 0)
    xMax = min(move.c + 5, currBoard.width)
    yMin = max(move.r - 5, 0)
    yMax = min(move.r + 5, currBoard.height)

    smallBoard = [[0 for x in range(xMax - xMin)] for y in range(yMax - yMin)]
    smallx = 0
    smally = 0
    for each in range(xMax, xMin):
        for one in range(yMin, yMax):
            team = currBoard.__getitem__[each][one].team
            if team is None:
                smallBoard[smallx][smally] = "-"
            elif team is "Sno_Stu_Son":
                smallBoard[smallx][smally] = "P"
            else:
                smallBoard[smallx][smally] = "O"
            smally = smally + 1
        smallx = smallx + 1
    # small board initialized
    # possible wins
    xdir = ""
    ydir = ""
    diag1 = ""
    diag2 = ""
    for each in range(smallx):
        xdir += smallBoard[each][5]
        diag1 += smallBoard[each][each]
        diag2 += smallBoard[each][smallx - each]
    for each in range(smally):
        ydir += smallBoard[5][each]

    # scoring moves
    # search directions for OO---, -OO--, --OO-, ---OO
    # CLOSED 2			   POO---, ---OOP
    # OPEN 3				   -OOO-
    # CLOSED 3			   --OOOP, POOO--
    # OPEN 4				   -OOOO-
    # CLOSED 4			   -OOOOP, POOOO-
    # FIVE				   OOOOO

    pO2 = xdir.count("PP---") + xdir.count("-PP--") + xdir.count("--PP-") + xdir.count("---PP")
    pO2 += ydir.count("PP---") + ydir.count("-PP--") + ydir.count("--PP-") + ydir.count("---PP")
    pO2 += diag1.count("PP---") + diag1.count("-PP--") + diag1.count("--PP-") + diag1.count("---PP")
    pO2 += diag2.count("PP---") + diag2.count("-PP--") + diag2.count("--PP-") + diag2.count("---PP")

    pCl2 = xdir.count("OPP---") + xdir.count("---PPO") + ydir.count("OPP---") + ydir.count("---PPO")
    pCl2 += diag1.count("OPP---") + diag1.count("---PPO") + diag2.count("OPP---") + diag2.count("---PPO")

    pO3 = xdir.count("-PPP-") + ydir.count("-PPP-") + diag1.count("-PPP-") + diag2.count("-PPP-")

    pCl3 = xdir.count("OPPP--") + xdir.count("--PPPO") + ydir.count("OPPP--") + ydir.count("--PPPO")
    pCl3 += diag1.count("OPPP--") + diag1.count("--PPPO") + diag2.count("OPPP--") + diag2.count("--PPPO")

    pO4 = xdir.count("-PPPP-") + ydir.count("-PPPP-") + diag1.count("-PPPP-") + diag2.count("-PPPP-")

    pCl4 = xdir.count("OPPPP-") + xdir.count("-PPPPO") + ydir.count("OPPPP-") + ydir.count("-PPPPO")
    pCl4 += diag1.count("OPPPP-") + diag1.count("-PPPPO") + diag2.count("OPPPP-") + diag2.count("-PPPPO")

    p5 = xdir.count("PPPPP") + ydir.count("PPPPP") + diag1.count("PPPPP") + diag2.count("PPPPP")

    oppO2 = xdir.count("OO---") + xdir.count("-OO--") + xdir.count("--OO-") + xdir.count("---OO")
    oppO2 += ydir.count("OO---") + ydir.count("-OO--") + ydir.count("--OO-") + ydir.count("---OO")
    oppO2 += diag1.count("OO---") + diag1.count("-OO--") + diag1.count("--OO-") + diag1.count("---OO")
    oppO2 += diag2.count("OO---") + diag2.count("-OO--") + diag2.count("--OO-") + diag2.count("---OO")

    oppCl2 = xdir.count("POO---") + xdir.count("---OOP") + ydir.count("POO---") + ydir.count("---OOP")
    oppCl2 += diag1.count("POO---") + diag1.count("---OOP") + diag2.count("POO---") + diag2.count("---OOP")

    oppO3 = xdir.count("-OOO-") + ydir.count("-OOO-") + diag1.count("-OOO-") + diag2.count("-OOO-")

    oppCl3 = xdir.count("POOO--") + xdir.count("--OOOP") + ydir.count("POOO--") + ydir.count("--OOOP")
    oppCl3 += diag1.count("POOO--") + diag1.count("--OOOP") + diag2.count("POOO--") + diag2.count("--OOOP")

    oppO4 = xdir.count("-OOOO-") + ydir.count("-OOOO-") + diag1.count("-OOOO-") + diag2.count("-OOOO-")

    oppCl4 = xdir.count("POOOO-") + xdir.count("-OOOOP") + ydir.count("POOOO-") + ydir.count("-OOOOP")
    oppCl4 += diag1.count("POOOO-") + diag1.count("-OOOOP") + diag2.count("POOOO-") + diag2.count("-OOOOP")

    opp5 = xdir.count("OOOOO") + ydir.count("OOOOO") + diag1.count("OOOOO") + diag2.count("OOOOO")

    playerScore = pO2 * 2 + pCl2 + pO3 * 200 + pCl3 * 2 + pO4 * 2000 + pCl4 * 200 + p5 * 2000
    oppScore = oppO2 * 2 + oppCl2 + oppO3 * 2000 + oppCl3 * 20 + oppO4 * 20000 + oppCl4 * 2000 + opp5 * 20000
    score = playerScore - oppScore

    return score


"""
want this to work in a way where the program (currently) applies a +1 to each
location around a friendly piece (unless the opposing player has a piece there,
but maybe ignore that part for now).
convert the letters of the columns into numbers (easiest way I can think of currently)
do we want to keep track of each piece in play currently, then from there determine scores
from there, rather than continually looking at new pieces.
"""


def check_turn():
    # True if our turn, false otherwise
    return os.path.exists("Sno_Stu_Son.go")


def check_end():
    # True if game is over, false otherwise
    return os.path.exists("end_game")


def str_to_move(moveString):
    moveList = moveString.split()
    return referee.Move(moveList[0], moveList[1], moveList[2])


# replace with str(referee.Move)
def move_to_str(move):
    moveString = "{} {} {}".format(move.p, move.c, move.r)
    return moveString


def letter_to_int(letter):
    return ord(letter) - ord('A')


timeout_flag = 0


def timeout():
    global timeout_flag
    timeout_flag = 1
    file("move_file", 'r').close()
    with open("move_file", 'w') as f:
        f.write("Sno_Stu_Son D 8")


def make_move():
    oppMove = referee.Move("groupname", 0, "Z")
    playerMove = referee.Move("Sno_Stu_Son", 0, "Z")
    if check_end() is False:
        with open("move_file", 'r') as f:
            move = f.readline()
            if move is '':
                # If the first line of the file is empty, then this is the first move of the game
                # White stones, make a move
                # playerMove = minimax(empty board_state)
                print("Empty file")
            else:
                # If there is a move in the file, then this is not the first move of the game
                # Black stones, send opponent's move to str_to_move
                oppMove = str_to_move(move)
        playerMove = minimax(next_board(oppMove))
        moveString = move_to_str(playerMove)
        if timeout_flag is 0:
            with open("move_file", 'w') as f:
                f.write(moveString)
        else:
            print("Move went over 10 second limit")
    else:
        print("Game over")


def turn_loop():
    t1 = Thread(target=Timer, args=(9, 9, timeout))
    t2 = Thread(target=make_move)
    while check_turn() is False:
        sleep(0.025)
    t1.start()
    t2.start()
    while True:
        if t2.isAlive() is False:
            t1.cancel()
            break
