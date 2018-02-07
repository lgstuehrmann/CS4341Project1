# CS 4341 Project 1

**Team Members**: Robert Harrison, Brady Snowden, and Lucy Stuehrmann

## Running This Script:
This program runs on Python 3.x. In order to run it, open a terminal,
navigate to the directory containing minimax.py, and run the following command:
1. On Linux:

`./minimax.py`

2. On Windows: 

`python3 minimax.py`

3. On Mac:

`python3 ./minimax.py`

## Utility and Evaluation Function Explanation
We used an evaluation function that assigned a value to each grid space
within 11 squares of the opponent's last move for each potential board
state. This function, which is named `board_score()` in the code, works
as-follows:
1. The function finds an 11 by 11 square centered on the opponent's previous
move
2. Starting from the center of the square, the function checks each cardinal and ordinal direction for scoring moves.
3. When evaluating the scoring moves in each direction, the function assigns negative values to opponent scoring moves 
and positive values to player scoring moves, with moves that are closer to a win condition weighted higher (these
scoring moves are defined in a comment within the function).
4. The sum of the values of the grid spaces is returned, which gives a 
rough estimate of the potential heuristic value of a board state. This is 
then fed into the minimax algorithm so that it can decide which potential
board state gives the best score.   

This results in a reasonable heuristic estimate for use in conjunction with 
the minimax algorithm, and typically results in good move decisions.


## Heuristics and Strategies for Expansion
In order to ensure that system timeout did not occur, it was necessary to
implement strategies for pruning and node expansion selection. We
implemented alpha-beta pruning first in order to remove unprofitable 
branches from the tree. This helped decrease system latency, however, 
there were still memory and space issues when expanding the game tree.
We also used depth-limited iterative search to expand the game tree and 
preselected the initial move. Preselecting the initial move to be in the 
center of the board reduced the possible number of board states from 225! 
to 224!, which greatly decreases the number of board states that need to 
be expanded. Depth-limited iterative search also decreased the number of 
board states expanded, as limiting depth to 4, for example, results in an 
expansion of only (225! - 221!) board states, which is a substantial 
decrease in complexity as compared to expanding all possible board 
states. Furthermore, to decrease complexity in the game tree, we limited
the area represented in a board state to an 11 by 11 grid centered at 
the opponent's last move. This greatly decreased system latency and did 
not lead to a significant sacrifice in gameplay, as most desirable moves
typically occur close to a previous move.

## Results
We tested this system by having it play against a clone of itself. 
This allowed us to test its behavior when playing both first and
second and therefore allowed us to observe its behavior in both an 
offensive and a defensive scenario. During these games, the program 
performed somewhat well, often playing games that resulted in an 
optimal win. We also tested the program against an online gomoku program,
which can be found at the following link:  
`http://gomoku.yjyao.com/`   
Against this opponent, once again, the system performs relatively well.
It mainly displayed defensive behavior, as the opponent AI was typically
more aggressive and played better, but it was making intelligent and 
rational defensive decisions.  
One source of concern was the system latency. Occasionally, in long games, 
our program would time out, which was not desired.

## Discussion
