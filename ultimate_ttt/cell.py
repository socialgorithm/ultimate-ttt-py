from .gameplay import Player

class Cell(object):
    """A cell in a game of TicTacToe

    This class records the ultimate_ttt_player
    """
    def __init__(self, played_by = Player.NONE):
        self.played_by = played_by

    def __str__(self):
        return str(self.played_by.value)

    def is_played(self):
        """Whether this cell has been played by a ultimate_ttt_player"""
        return not(self.played_by == Player.NONE)
