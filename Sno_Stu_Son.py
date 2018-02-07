# Robert Harrison
# Brady Snowden
# Lucy Stuehrmann
#
# Script for development and testing of the minimax algorithm for Project 1.
# Will use symmetry to prune identical game boards from the search tree.
#
import threading
import time
from time import sleep
from io import FileIO
import os

# Global Variable Total_Score keeps track of the known score of the board

Total_Score = 0
Opponent = "groupname"
best_move = None
timeout_flag = 0
first_move = 0

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

        self.move_history = []

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


class Move(object):
    def __init__(self, team_name, x_loc, y_loc):
        self.team_name = team_name
        self.x = x_loc
        self.y = y_loc - 1

    def __str__(self):
        return "%s %s %s" % (self.team_name, chr(self.x + ord('a')), (self.y + 1))


"""
This is the algorithm that looks for the best move for the program to make
by evaluating the states of the board
input: the current state of the gomoku board
output: the move that our program should make 
"""


def minimax(board_state):
    global Total_Score, best_move, timeout_flag
    # get list of possible moves for player
    moves = get_available_moves(board_state, "Sno_Stu_Son", board_state.move_history[0])
    best_move = moves[0]
    max_depth = 4
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
    moves = get_available_moves(board_state, Opponent, board_state.move_history[0])
    avg = 0
    mid = len(moves) // 2
    while len(moves) != 0:
        board = board_state
        m = moves.pop(0)
        board.placeFakeToken(m)
        temp_total += board_score(board, m)
        avg += temp_total
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
        if len(moves) > mid:
            if avg > 0:
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
    moves = get_available_moves(board_state, "Sno_Stu_Son", board_state.move_history[0])
    avg = 0
    mid = len(moves) // 2
    while len(moves):
        board = board_state
        m = moves.pop(0)
        board.placeFakeToken(m)
        temp_total += board_score(board, m)
        avg += temp_total
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
        if len(moves) > mid:
            if avg < 0:
                break
    return alpha


"""
input: the current state of the board & the team who moves next
output: a list of all possible moves that the program should consider
"""


def get_available_moves(currBoard, team, m):
    stack = []
    maxX = currBoard.width
    minX = 0
    maxY = currBoard.height
    minY = 0
    numMoves = currBoard.move_history.__len__()
    if numMoves < 3:
        minX = max(0, m.x - 2)
        maxX = min(currBoard.width, m.x + 2)
        minY = max(0, m.y - 2)
        maxY = min(currBoard.height, m.y + 2)
    elif numMoves >= 3 and numMoves < 7:
        minX = max(0, m.x - 3)
        maxX = min(currBoard.width, m.x + 3)
        minY = max(0, m.y - 3)
        maxY = min(currBoard.height, m.y + 3)
    elif numMoves >= 7 and numMoves < 13:
        minX = max(0, m.x - 4)
        maxX = min(currBoard.width, m.x + 4)
        minY = max(0, m.y - 4)
        maxY = min(currBoard.height, m.y + 4)
    elif numMoves >= 13 and numMoves < 16:
        minX = max(0, m.x - 6)
        maxX = min(currBoard.width, m.x + 6)
        minY = max(0, m.y - 6)
        maxY = min(currBoard.height, m.y + 6)
    elif numMoves >= 16 and numMoves < 25:
        minX = max(0, m.x - 9)
        maxX = min(currBoard.width, m.x + 9)
        minY = max(0, m.y - 9)
        maxY = min(currBoard.height, m.y + 9)
    else:
        minX = 0
        maxX = currBoard.width
        minY = 0
        maxY = currBoard.height
    for each in range(minX, maxX):
        for one in range(minY, maxY):
            if currBoard.isFieldOpen(each, one):
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


def getSymbol(currBoard, x, y):
    team = currBoard.getTeam(Move(None, x, y))
    if team == None:
        return "-"
    elif team == "Sno_Stu_Son":
        return "P"
    else:
        return "O"


"""
determine the "score" of the board 
input: the state of the board and the last move made
output: the score difference that the specified move made on the board
"""


def board_score(currBoard, move):
    # restrict range to 0 - boardsize
    if (move.x - 5) < 0:
        xMin = 0
    else:
        xMin = move.x - 5
    if (move.x + 5) > 14:
        xMax = 14
    else:
        xMax = move.x + 5
    if (move.y - 5) < 0:
        yMin = 0
    else:
        yMin = move.y - 5
    if (move.y + 5) > 14:
        yMax = 14
    else:
        yMax = move.y + 5

    xdir = ""
    ydir = ""
    prediag1 = ""
    prediag2 = ""
    prediag3 = ""
    prediag4 = ""

    for x in range(xMin, xMax + 1):
        xdir += getSymbol(currBoard, x, move.y)
    for y in range(yMin, yMax + 1):
        ydir += getSymbol(currBoard, move.x, y)
    xStart = move.x
    yStart = move.y
    while xStart >= xMin and yStart >= yMin:
        prediag1 += getSymbol(currBoard, xStart, yStart)
        xStart -= 1
        yStart -= 1
    xStart = move.x
    yStart = move.y
    while xStart <= xMax and yStart >= yMin:
        prediag2 += getSymbol(currBoard, xStart, yStart)
        xStart += 1
        yStart -= 1
    xStart = move.x - 1
    yStart = move.y + 1
    while xStart >= xMin and yStart <= yMax:
        prediag3 += getSymbol(currBoard, xStart, yStart)
        xStart -= 1
        yStart += 1
    xStart = move.x + 1
    yStart = move.y + 1
    while xStart <= xMax and yStart <= yMax:
        prediag4 += getSymbol(currBoard, xStart, yStart)
        xStart += 1
        yStart += 1

    diag1 = "".join(reversed(prediag1)) + prediag4
    diag2 = "".join(reversed(prediag3)) + prediag2

    # scoring moves
    # search directions for OO---, -OO--, --OO-, ---OO
    # CLOSED 2			   POO---, ---OOP
    # OPEN 3				   -OOO-
    # CLOSED 3			   --OOOP, POOO--
    # OPEN 4				   -OOOO-
    # CLOSED 4			   -OOOOP, POOOO-
    # FIVE				   OOOOO

    if xdir.find("P") == -1 and xdir.find("O") == -1 and ydir.find("P") == -1 and ydir.find("O") == -1 and diag1.find(
            "P") == -1 and diag1.find("O") == -1 and diag2.find("P") == -1 and diag2.find("O") == -1:
        score = -1
    else:
        pO2 = xdir.count("PP---") + xdir.count("-PP--") + xdir.count("--PP-") + xdir.count("---PP")
        pO2 += ydir.count("PP---") + ydir.count("-PP--") + ydir.count("--PP-") + ydir.count("---PP")
        pO2 += diag1.count("PP---") + diag1.count("-PP--") + diag1.count("--PP-") + diag1.count("---PP")
        pO2 += diag2.count("PP---") + diag2.count("-PP--") + diag2.count("--PP-") + diag2.count("---PP")

        pCl2 = xdir.count("OPP---") + xdir.count("---PPO") + ydir.count("OPP---") + ydir.count("---PPO")
        pCl2 += diag1.count("OPP---") + diag1.count("---PPO") + diag2.count("OPP---") + diag2.count("---PPO")

        pO3 = xdir.count("-PPP-") + ydir.count("-PPP-") + diag1.count("-PPP-") + diag2.count("-PPP-")
        pO3 += xdir.count("P-PP") + ydir.count("P-PP") + diag1.count("P-PP") + diag2.count("P-PP")
        pO3 += xdir.count("PP-P") + ydir.count("PP-P") + diag1.count("PP-P") + diag2.count("PP-P")

        pCl3 = xdir.count("OPPP--") + xdir.count("--PPPO") + ydir.count("OPPP--") + ydir.count("--PPPO")
        pCl3 += diag1.count("OPPP--") + diag1.count("--PPPO") + diag2.count("OPPP--") + diag2.count("--PPPO")

        pO4 = xdir.count("-PPPP-") + ydir.count("-PPPP-") + diag1.count("-PPPP-") + diag2.count("-PPPP-")
        pO4 += xdir.count("P-PPP") + ydir.count("P-PPP") + diag1.count("P-PPP") + diag2.count("P-PPP")
        pO4 += xdir.count("PP-PP") + ydir.count("PP-PP") + diag1.count("PP-PP") + diag2.count("PP-PP")
        pO4 += xdir.count("PPP-P") + ydir.count("PPP-P") + diag1.count("PPP-P") + diag2.count("PPP-P")

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
        oppO3 += xdir.count("O-OO") + ydir.count("O-OO") + diag1.count("O-OO") + diag2.count("O-OO")
        oppO3 += xdir.count("O-OO") + ydir.count("O-OO") + diag1.count("O-OO") + diag2.count("O-OO")

        oppCl3 = xdir.count("POOO--") + xdir.count("--OOOP") + ydir.count("POOO--") + ydir.count("--OOOP")
        oppCl3 += diag1.count("POOO--") + diag1.count("--OOOP") + diag2.count("POOO--") + diag2.count("--OOOP")

        oppO4 = xdir.count("-OOOO-") + ydir.count("-OOOO-") + diag1.count("-OOOO-") + diag2.count("-OOOO-")
        oppO4 += xdir.count("O-OOO") + ydir.count("O-OOO") + diag1.count("O-OOO") + diag2.count("O-OOO")
        oppO4 += xdir.count("OO-OO") + ydir.count("OO-OO") + diag1.count("OO-OO") + diag2.count("OO-OO")
        oppO4 += xdir.count("OOO-O") + ydir.count("OOO-O") + diag1.count("OOO-O") + diag2.count("OOO-O")

        oppCl4 = xdir.count("POOOO-") + xdir.count("-OOOOP") + ydir.count("POOOO-") + ydir.count("-OOOOP")
        oppCl4 += diag1.count("POOOO-") + diag1.count("-OOOOP") + diag2.count("POOOO-") + diag2.count("-OOOOP")

        opp5 = xdir.count("OOOOO") + ydir.count("OOOOO") + diag1.count("OOOOO") + diag2.count("OOOOO")

        playerScore = pO2 * 2 + pCl2 + pO3 * 200 + pCl3 * 2 + pO4 * 2000 + pCl4 * 200 + p5 * 20000
        oppScore = oppO2 * 2 + oppCl2 + oppO3 * 2000 + oppCl3 * 20 + oppO4 * 20000 + oppCl4 * 2000 + opp5 * 20000
        score = playerScore - oppScore
    return score


def check_turn():
    # True if our turn, false otherwise
    return os.path.exists("Sno_Stu_Son.go")


def check_end():
    # True if game is over, false otherwise
    return os.path.exists("end_game")


def str_to_move(moveString):
    moveList = moveString.split()
    return Move(moveList[0], letter_to_int(moveList[1].upper()), int(moveList[2]))


def move_to_str(move):
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
    print("Made move :", move_to_str(best_move))
    timeout_flag = 1


def make_move(board_state):
    global Opponent, Total_Score, timeout_flag, first_move
    oppMove = None
    playerMove = None
    if check_end() == False:
        with open("move_file", 'r') as f:
            move = f.readline()
            if first_move != 1:
                # If the first line of the file is empty, then this is the first move of the game
                # White stones, make a move
                playerMove = Move("Sno_Stu_Son", letter_to_int("H"), 8)
                first_move = 1
            else:
                # If there is a move in the file, then this is not the first move of the game
                # Black stones, send opponent's move to str_to_move
                oppMove = str_to_move(move)
                print("Opponent moved: ", oppMove.x, oppMove.y)
                Opponent = oppMove.team_name
                board_state = next_board(board_state, oppMove)
                playerMove = minimax(board_state)
            board_state.placeToken(playerMove)
            Total_Score += board_score(board_state, playerMove)
            moveString = move_to_str(playerMove)
        if timeout_flag == 0:
            with open("move_file", 'w') as f:
                f.write(moveString)
            print("Made move: ", moveString)
            return [0, board_state]
        else:
            print("Move went over 10 second limit")
    else:
        print("Game over")
        return [0, board_state]
    return [1, board_state]


def turn_loop(board_state):
    t1 = threading.Timer(9, timeout)
    while check_turn() == False:
        sleep(0.06)
    t1.start()
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