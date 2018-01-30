# Script for development and testing of the minimax algorithm for Project 1.
# Will use symmetry to prune identical game boards from the search tree.
#

import numpy as np
import referee
import tester
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
	best_score = float("-inf")
	for m in moves:
		# clone the state of the board with that possible move
		clone = board_state.next_board(m)
		# Now look at the move options available to the min player and get score
		score = min_move(clone)
		# check to see if the move is the best move based on score knowledge
		if score > best_score:
			best_move = m
			best_score = score
	return best_move

"""
input: the board state after the program makes a theoretical move
output: the "score" of the move that the min player will make based
on a heuristic function we have yet to write
"""
def min_move(board_state):
	# list of the moves available to the opponent
	moves = board_state.get_available_moves()
	best_move = moves[0]
	best_score = float("inf")
	for m in moves:
		clone = board_state.next_board(m)
		score = max_move(clone)
		if score < best_score:
			best_move = m
			best_score = score
	return best_score


"""
input: the board state after the opponent makes a move
output: the "score" of the move that the max player will make
might make based on a heuristic function we have yet to write
"""
def max_move(board_state):
	# list of the moves available to the player after opponent moves
	moves = board_state.state.get_available_moves()
	best_move = moves[0]
	best_score = float("-inf")
	for m in moves:
		clone = board_state.next_board(move)
		# next line creates infinite loop right now
		#score = min_move(clone)
		score = clone.board_score()
		if score > best_score:
			best_move = m
			best_score = score
	return best_score

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


"""
determine the "score" of the board 
input: the state of the board
output: the score of the board based on math-stuff
"""
def board_score():