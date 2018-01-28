import os.path

def check_turn():
	#True if our turn, false otherwise
	return os.path.exists("groupname.go")

def check_end():
	#True if game is over, false otherwise
	return os.path.exists("end_game")

def minimax(moveList):
	if moveList is not '':
		print("Row %c" % moveList[1])
		print("Column %c" % moveList[2])
	else:
		print("First move of the game")
	return "groupname G 8"

def make_move():
	if check_turn() is True:
		if check_end() is False:
			with open("move_file", 'r+') as f:
				move = f.readline()
				if move is '':
					#If the first line of the file is empty, then this is the first move of the game
					#White stones, make a move
					f.write(minimax(move))
					print(minimax(move))
				else:
					#If there is a move in the file, then this is not the first move of the game
					#Black stones, send opponent's move to minimax
					moveParts = move.split()
					newMove = minimax(moveParts)
					f.seek(0) #Returns to top of file to overwrite move
					f.write(newMove)
					print("New move written")
		else:
			print("Game over")
	else:
		print("Not your turn")

make_move()
