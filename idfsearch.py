#Lucy Stuehrmann
# Implementation of functions for searching through game tree
# Using Iterative Depth First Search to nav through game tree
import referee
import tester
##EXPANDING TREE
# Start by figuring out where we are in the tree, i.e. are we at move 1 or 3 or what?
# Take current move, add it to the gameboard that we generate
# Take the current board, find it in current expanded node
# Trim impossible moves at this point from the frontier
# Get to searching! Until we implement heuristics, just do IDFS
# Return expanded tree

def genCurrBoard(move_file):
    curr_move = move_file.readMoveFile()
    x = curr_move.x_loc
    y = curr_move.y_loc
    team = curr_move.team_name
