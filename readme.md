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

## Utility Function Explanation

## Evaluation Function Explanation

## Heuristics & Strategies for Expansion
In order to ensure that system timeout did not occur, it was necessary to implement strategies for pruning and node
expansion selection. We implemented alpha-beta pruning first in order to remove unprofitable branches from the tree. 
This helped decrease system latency, however, there were still memory and space issues when expanding the game tree.
We also used depth-limited iterative search to expand the game tree and preselected the initial move. Preselecting the 
initial move to be in the center of the board reduced the possible number of board states from 225! to 224!, which 
greatly decreases the number of board states that need to be expanded. Depth-limited iterative search also decreased
the number of board states expanded, as limiting depth to 4, for example, results in an expansion of only (225! - 221!)
board states, which is a substantial decrease in complexity as compared to expanding all possible board states.

## Results
We tested this system by having it play against a clone of itself. This allowed us to test its behavior when playing 
both first and second and therefore allowed us to observe its behavior in both an offensive and a defensive scenario.
During these games, the program performed somewhat well, often playing games that resulted in an optimal win. 
Unfortunately the program also struggled with system latency and timed out frequently due to lack of sufficient 
pruning. 

## Discussion
