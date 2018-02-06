# Script for development and testing of the minimax algorithm for Project 1.
# Will use symmetry to prune identical game boards from the search tree.
#
import threading
from time import sleep
from io import FileIO
import sys
import os
import random

# Global Variable Total_Score keeps track of the known score of the board

Total_Score = 0
Opponent = "groupname"
best_move = None
timeout_flag = 0


class GomokuBoard(object):
    class _SingleField(object):
        isEmpty = True
        team = None

        def playField(self, team):
            self.isEmpty = False
            self.team = team
            return True

        # Added to remove pieces at the end of the loop in minimax
        def emptyField(self):
            self.isEmpty = True
            self.team = None
            return True

    width = None
    height = None

    def __init__(self, width=8, height=8):
        super(GomokuBoard, self).__init__()
        self.width = width
        self.height = height
        self._field = [[self._SingleField() for y in range(height)]
                       for x in range(width)]

        self.move_history = []  # not really necessary for us right?

    def __getitem__(self, index):
        (x, y) = index
        return self._field[x][y]

    def isFieldOpen(self, row, column):
        return self._field[row][column].isEmpty

    def placeToken(self, move):
        self.move_history.append(move)
        return self._field[move.x][move.y].playField(move.team_name)

    def placeFakeToken(self, move):
        return self._field[move.x][move.y].playField(move.team_name)

    def removeToken(self, move):
        return self._field[move.x][move.y].emptyField()

    def getTeam(self, move):
        return self._field[move.x][move.y].team

    def printBoard(self, teams):
        print("")
        print("%s -- %s" % ('X', teams[0]))
        print("%s -- %s" % ('O', teams[1]))
        print("")
        sys.stdout.write("   ")
        for x in range(self.width):
            sys.stdout.write('%s ' % (chr(x + ord('A'))))
        sys.stdout.write("\n")
        for y in range(self.height):
            sys.stdout.write('%02s ' % (y + 1))
            for x in range(self.width):
                if self._field[x][y].team is None:
                    sys.stdout.write('-')
                else:
                    # team_name_hash = hashlib.md5(self._field[x][y].team).hexdigest()
                    if teams.index(self._field[x][y].team) == 0:
                        team_color = 'X'
                    else:
                        team_color = 'O'
                    sys.stdout.write(team_color)
                sys.stdout.write(' ')
            sys.stdout.write('\n')

        sys.stdout.flush()


class Move(object):
    def __init__(self, team_name, x_loc, y_loc):
        self.team_name = team_name
        self.x = x_loc
        self.y = y_loc - 1

    def __str__(self):
        return "%s %s %s" % (self.team_name, chr(self.x + ord('a')), (self.y + 1))


# alpha_beta class containing alpha beta values
class alpha_beta:
    def __init__(self, alpha, beta):
        self.a = alpha
        self.b = beta

"""
This is the algorithm that looks for the best move for the program to make
by evaluating the states of the board
input: the current state of the gomoku board
output: the move that our program should make 
"""


def minimax(board_state):
    global Total_Score, best_move, timeout_flag
    # get list of possible moves for player
    moves = get_available_moves(board_state, "Sno_Stu_Son2")
    best_move = moves[0]
    print("best move:", best_move)
    max_depth = 3
    alpha = float("-inf")
    beta = float("inf")
    while len(moves) != 0:
        board = board_state
        m = moves.pop(0)
        temp_total = Total_Score
        # add move to the board
        board.placeFakeToken(m)
        temp_total += board_score(board, m)
        # Now look at the move options available to the min player and get score
        score = min_move(board, max_depth, alpha, beta, temp_total)
        board.removeToken(m)
        # check to see if the move is the best move based on score knowledge
        if score > alpha:
            best_move = m
            alpha = score
        if timeout_flag == 1:
            break
    # Before returning move, add board score change made by best_move
    return best_move


"""
input: the board state after the opponent makes a move, max depth, 
alpha beta values, and temporary total board score
output: the "score" of the move that the min player will make based
on a heuristic function we have yet to write
"""


def min_move(board_state, max_depth, alpha, beta, temp_total):
    global timeout_flag
    max_depth -= 1
    # list of the moves available to the opponent
    moves = get_available_moves(board_state, Opponent)
    while len(moves) != 0:
        board = board_state
        m = moves.pop(0)
        board.placeFakeToken(m)
        # subtract value of opponent mve from board score val
        temp_total += board_score(board, m)
        # if in final node
        if max_depth == 1:
            score = temp_total
        else:
            score = max_move(board, max_depth, alpha, beta, temp_total)
        board.removeToken(m)
        if score < beta:
            beta = score
        if alpha > beta:
            break
        if timeout_flag == 1:
            break
    return beta


"""
input: the board state after the opponent makes a move, max depth, 
alpha beta values, and temporary total board score
output: the "score" of the move that the max player will make
might make based on a heuristic function we have yet to write
"""


def max_move(board_state, max_depth, alpha, beta, temp_total):
    global timeout_flag
    max_depth -= 1
    # list of the moves available to the player
    moves = get_available_moves(board_state, "Sno_Stu_Son2")
    while len(moves):
        board = board_state
        m = moves.pop(0)
        board.placeFakeToken(m)
        temp_total += board_score(board, m)
        if max_depth == 1:
            score = temp_total
        else:
            score = min_move(board, max_depth, alpha, beta, temp_total)
        board.removeToken(m)
        if score > alpha:
            alpha = score
        if alpha > beta:
            break
        if timeout_flag == 1:
            break
    return alpha


# *** Following functions inside the yet to be made board class
"""
input: the current state of the board & the team who moves next
output: a list of all possible moves that the program should consider
"""


def get_available_moves(currBoard, team):
    stack = []
    for each in range(currBoard.width): #A to L; no problem here
        for one in range(currBoard.height): #0 to 14
            if currBoard.isFieldOpen(each, one): # A 1 = false
                potentialMove = Move(team, each, (one + 1))
                stack.append(potentialMove)
    return stack


"""
input: current board, x and y coordinates of the global current board
returns true if the current position has a marker
returns false otherwise
"""


def isOccupied(currBoard, x, y):
    if GomokuBoard.isFieldOpen(currBoard, x, y):
        check = False
    else:
        check = True
    return check


"""
input: a possible move that the board wants to put into play
output: a board state where the specified move has been added to the new board_state
"""


def next_board(board_state, move):
    board_state.placeToken(move)
    return board_state


"""
determine the "score" of the board 
input: the state of the board and the last move made
output: the score difference that the specified move made on the board
"""


def board_score(currBoard, move):
    score = random.randint(1,50)
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
    return os.path.exists("Sno_Stu_Son2.go")


def check_end():
    # True if game is over, false otherwise
    return os.path.exists("end_game")


def str_to_move(moveString):
    moveList = moveString.split()
    return Move(moveList[0], letter_to_int(moveList[1].upper()), int(moveList[2]))


def move_to_str(move):
    print(move.x, move.y)
    ydir = move.y + 1
    xdir = move.x + ord('A')
    return "%s %c %s" % (str(move.team_name), chr(xdir), str(ydir))


def letter_to_int(letter):
    return ord(letter) - ord('A')


def timeout():
    global timeout_flag
    FileIO("move_file", 'r').close()
    with open("move_file", 'w') as f:
        move = move_to_str(best_move)
        f.write(move)
    timeout_flag = 1


def make_move(board_state):
    global Opponent, Total_Score, timeout_flag
    oppMove = None #referee2.Move(Opponent, letter_to_int("A"), 1)
    playerMove = None #referee2.Move("Sno_Stu_Son2", letter_to_int("A"), 1)
    if check_end() == False:
        with open("move_file", 'r') as f:
            move = f.readline()
            if len(move) == 0:
                # If the first line of the file is empty, then this is the first move of the game
                # White stones, make a move
                # playerMove = minimax(empty board_state)
                print("Empty file")
                playerMove = Move("Sno_Stu_Son2", letter_to_int("H"), 8)
            else:
                # If there is a move in the file, then this is not the first move of the game
                # Black stones, send opponent's move to str_to_move
                oppMove = str_to_move(move)
                print("Opp move", oppMove.x, oppMove.y)
                Opponent = oppMove.team_name
                print(Opponent)
                board_state = next_board(board_state, oppMove)
                board_state.printBoard(["Sno_Stu_Son", "Sno_Stu_Son2"])
                playerMove = minimax(board_state)
            board_state.placeToken(playerMove)
            Total_Score += board_score(board_state, playerMove)
            moveString = move_to_str(playerMove)
        if timeout_flag == 0:
            with open("move_file", 'w') as f:
                f.write(moveString)
            return [0, board_state]
        else:
            print("Move went over 10 second limit")
    else:
        print("Game over")
    return [1, board_state]


def turn_loop(board_state):
    t1 = threading.Timer(8, timeout)
    #t2 = threading.Thread(target=make_move)
    while check_turn() == False:
        sleep(0.025)
    t1.start()
    #t2.start()
    val = make_move(board_state)
    if val[0] == 0:
        t1.cancel()
        return val[1]
    else:
        return val[1]


if __name__ == "__main__":
    Current_Board_State = GomokuBoard(15, 15)
    while not check_end():
        timeout_flag = 0
        Current_Board_State = turn_loop(Current_Board_State)
        sleep(0.5)