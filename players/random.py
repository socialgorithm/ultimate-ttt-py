import sys

import random

from players.stdout import StdOutPlayer


class Random(StdOutPlayer):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.__init__()

    def get_my_move(self):
        main_board_coords = self._pick_next_board_coords()
        next_board = self.main_board.get_sub_board(main_board_coords)
        sub_board_coords = self._pick_random_playable_move_coords(next_board)
        sys.stdout.flush()
        return main_board_coords, sub_board_coords

    def _pick_next_board_coords(self):
        forced_sub_board_coords = self.main_board.sub_board_next_player_must_play
        if forced_sub_board_coords is not None:
            return forced_sub_board_coords
        else:
            # We can play any board - pick one
            playable_boards_coords = self.main_board.get_playable_sub_board_coords()
            return random.choice(playable_boards_coords)

    @staticmethod
    def _pick_random_playable_move_coords(board):
        playable_coords = board.get_playable_coords()
        return random.choice(playable_coords)
