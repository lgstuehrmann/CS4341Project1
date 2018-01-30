import os.path
from threading import Thread
import minimax

# class Move:
# 	def __init__(self, column, row, player):
# 		self.c = column
# 		self.r = row
# 		self.p = player

# def minimax(move):
# 	return Move('E', 7, "Sno_Stu_Son")

def check_turn():
	#True if our turn, false otherwise
	return os.path.exists("Sno_Stu_Son.go")

def check_end():
	#True if game is over, false otherwise
	return os.path.exists("end_game")

def str_to_move(moveString):
	moveList = moveString.split()
	return Move(moveList[1], moveList[2], moveList[0])

def move_to_str(move):
	moveString = "{} {} {}".format(move.p, move.c, move.r)
	return moveString

def timeout():
	with open("move_file", 'w') as f:
		f.write("Sno_Stu_Son D 8")

def make_move():
	oppMove = Move('Z', 0, "groupname")
	playerMove = Move('Z', 0, "Sno_Stu_Son")
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
			with open("move_file", 'w') as f:
				f.write(moveString)
		else:
			print("Game over")
	else:
		print("Not your turn")

make_move()

# t1 = Thread(target=Timer, args=(9.9, timeout))
# t2 = Thread(target=make_move, name=moveThread)

# while check_turn() is False:
# 	sleep(0.025)

# t1.start()
# t2.start()
