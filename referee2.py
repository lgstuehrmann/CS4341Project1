#!env python

import logging
import sys
import os
import random
import time
import hashlib
import shutil

import copy

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

    def __init__(self, width=15, height=15):
        super(GomokuBoard, self).__init__()
        self.width = width
        self.height = height
        self._field = [[self._SingleField() for y in range(height)]
                                            for x in range(width)]

        self.move_history = []      # not really necessary for us right?

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

    def printBoard(self, teams):
        print("")
        print("%s -- %s" % ('X', teams[0]))
        print("%s -- %s" % ('O', teams[1]))
        print("")
        sys.stdout.write("   ")
        for x in range(self.width):
            sys.stdout.write('%s ' % (chr(x+ord('A'))))
        sys.stdout.write("\n")
        for y in range(self.height):
            sys.stdout.write('%02s ' % (y+1))
            for x in range(self.width):
                if self._field[x][y].team is None:
                    sys.stdout.write('-')
                else:
                    #team_name_hash = hashlib.md5(self._field[x][y].team).hexdigest()
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
