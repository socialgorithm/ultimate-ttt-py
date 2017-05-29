import random

from ultimate_ttt.gameplay import *
from ultimate_ttt.main_board import MainBoard
from ultimate_ttt_player.ultimate_ttt_player import UltimateTTTPlayer

global random_player


class Random(UltimateTTTPlayer):
    def __init__(self, board_size=3):
        UltimateTTTPlayer.__init__(self)
        self.board_size = board_size
        self.player = Player.ME
        self.opponent = Player.OPPONENT
        self.game = None

    def initialize(self):
        self.game = MainBoard(3)

    def add_opponent_move(self, board, opponent_move):
        self.game = self.game.add_opponent_move(board, opponent_move)

    def add_my_move(self, board, move):
        self.game = self.game.add_my_move(board, move)

    def get_my_move(self):
        """
        Returns: Player's next move
        """
        next_board_coords = self._pick_next_board()
        next_board = self.game.get_sub_board(next_board_coords)
        move = self._pick_random_move(next_board)
        return next_board_coords, move

    @property
    def player_name(self):
        return 'random'

    def wait(self):
        return

    @property
    def is_current_match_finished(self):
        return self.game.is_finished

    def _pick_next_board(self):
        """
        Returns: random, unfinished SubBoard to play in
        """
        next_board_coords = self.game.next_board_coords
        if next_board_coords is None:
            valid_boards = self.game.get_valid_boards()
            next_board_coords = random.choice(valid_boards)
        return next_board_coords

    def _pick_random_move(self, board):
        """
        Returns: random cell to play in SubBoard
        """
        valid_moves = board.get_valid_moves()
        return random.choice(valid_moves)
