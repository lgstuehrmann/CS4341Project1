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
	best_score = alpha_beta(float("-inf"), float("inf"))
	for m in moves:
		# clone the state of the board with that possible move
		clone = board_state.next_board(m)
		# Now look at the move options available to the min player and get score
		score = min_move(clone, max_depth, best_score)
		# check to see if the move is the best move based on score knowledge
		if score > best_score.a:
			best_move = m
			best_score.a = score
	return best_move

"""
input: the board state after the program makes a theoretical move
output: the "score" of the move that the min player will make based
on a heuristic function we have yet to write
"""
def min_move(board_state, max_depth, best_score):
	max_depth -= 1
	# list of the moves available to the opponent
	moves = board_state.get_available_moves()
	for m in moves:
		clone = board_state.next_board(m)
		if max_depth == 0:
			score = clone.board_score()
		else:
			score = max_move(clone, max_depth, best_score)
		if score < best_score.b:
			best_score.b = score
	return best_score.b


"""
input: the board state after the opponent makes a move
output: the "score" of the move that the max player will make
might make based on a heuristic function we have yet to write
"""
def max_move(board_state, max_depth, best_score):
	max_depth -= 1
	# list of the moves available to the player after opponent moves
	moves = board_state.state.get_available_moves()
	for m in moves:
		clone = board_state.next_board(move)
		if max_depth == 0:
			score = clone.board_score()
		else:
			score = min_move(clone, max_depth, best_score)
		if score > best_score.a:
			best_score.a = score
	return best_score.a

# *** Following funnctions inside the yet to be made board class
"""
input: the current state of the board & the team who moves next
output: a list of all possible moves that the program should consider
"""
def get_available_moves(currBoard, team):
	stack = list
	if team == "white":
		marker = 'X'
	else: marker = 'O'
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
def isOccupied(currBoard, x,y):
    index = (x,y)
    if referee.GomokuBoard.isFieldOpen(currBoard, index):
        check = False
    else: check = True
    return check


"""
input: a possible move that the board wants to put into play
output: a board state where the specified move has been added to the new board_state
"""
def next_board(move):
    return 1

"""
determine the "score" of the board 
input: the state of the board
output: the score of the board based on math-stuff
"""
def board_score():
	return 0

"""
want this to work in a way where the program (currently) applies a +1 to each
location around a friendly piece (unless the opposing player has a piece there,
but maybe ignore that part for now).
convert the letters of the columns into numbers (easiest way I can think of currently)
do we want to keep track of each piece in play currently, then from there determine scores
from there, rather than continually looking at new pieces.
"""
def check_turn():
	#True if our turn, false otherwise
	return os.path.exists("Sno_Stu_Son.go")

def check_end():
	#True if game is over, false otherwise
	return os.path.exists("end_game")

def str_to_move(moveString):
	moveList = moveString.split()
	return referee.Move(moveList[0], moveList[1], moveList[2])

#replace with str(referee.Move)
def move_to_str(move):
	moveString = "{} {} {}".format(move.p, move.c, move.r)
	return moveString

timeout_flag = 0

def timeout():
	timeout_flag = 1
	file("move_file", 'r').close()
	with open("move_file", 'w') as f:
		f.write("Sno_Stu_Son D 8")

def make_move():
	oppMove = referee.Move("groupname", 0, "Z")
	playerMove = referee.Move("Sno_Stu_Son", 0, "Z")
	if check_turn() is True:
		if check_end() is False:
			with open("move_file", 'r') as f:
				move = f.readline()
				if move is '':
					#If the first line of the file is empty, then this is the first move of the game
					#White stones, make a move
					#playerMove = minimax(empty board_state)
					print("Empty file")
				else:
					#If there is a move in the file, then this is not the first move of the game
					#Black stones, send opponent's move to str_to_move
					oppMove = str_to_move(move)
			playerMove = minimax(next_board(oppMove))
			moveString = move_to_str(playerMove)
			if timeout_flag is 0:
				with open("move_file", 'w') as f:
					f.write(moveString)
			else:
				print("Process went over 10 second limit")
		else:
			print("Game over")
	else:
		print("Not your turn")

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
