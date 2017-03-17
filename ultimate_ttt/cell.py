"""
A cell of a sub board in a game of ultimate TicTacToe

This is an object so that it can contain game metadata such as when the move was
played
"""

from .gameplay import Player

class Cell(object):
    """Cell class"""
    def __init__(self, played_by = Player.NONE):
        self.played_by = played_by

    def __str__(self):
        return str(self.played_by.value)

    def is_played(self):
        return not(self.played_by == Player.NONE)
