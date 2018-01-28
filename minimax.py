# Script for development and testing of the minimax algorithm for Project 1.
# Will use symmetry to prune identical game boards from the search tree.
#

import numpy as np


# move class with columns and rows
class move:
	def __init__(self, column, row)
		self.c = column
		self.r = row
"""
This is the algorithm that looks for the best possible move to be 
for now, assume unlimited space and go through all board
made by evaluating the states of the board
input: the current state of the gomoku board
output: the move that our program should make 
"""
# WARNING: infinite loop exists currently
minimax(board_state):
	# get list of possible moves ***(later fixed to smaller list)
	moves = board_state.get_available_moves()
	best_move = moves[0]
	best_score = float("-inf")
	for m in moves:
		# clone the state of the board with that possible move
		clone = board_state.next_board(move)
		# Now look at the move options available to the min player
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
min_move(board_state):
	# list of the moves available to the opponent
	moves = board.state.get_available_moves()
	best_move = moves[0]
	best_score = float("inf")
	for m in moves:
		clone = board_state.next_board(move)
		score = max_move(clone)
		if score < best_score:
			best_move = m
			best_score = score:

	return best_score


"""
input: the board state after the opponent makes a move
output: the "score" of the move that the max player will make
might make based on a heuristic function we have yet to write
"""
max_move(board_state):
	# list of the moves available to the player after opponent moves
	moves = board.state.get_available_moves()
	best_move = moves[0]
	best_score = float("-inf")
	for m in moves:
		clone = board_state.next_board(move)
		# next line creates infinite loop right now
		#score = min_move(clone)
		if score > best_score:
			best_move = m
			best_score = score
	return best_score

# *** Following funnctions inside the yet to be made board class
"""
input: the current state of the board
output: a list of all possible moves that could be 
"""
get_available_moves()

"""
input: a possible move that the board wants to put into play
output: a board state where the specified move has been added to the new board_state
"""
next_board(move)


# moves represented by column letter / Row number (i.e. F8)