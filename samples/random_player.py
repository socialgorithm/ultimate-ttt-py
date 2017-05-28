from ultimate_ttt.main_board import MainBoard
from ultimate_ttt.gameplay import *

import sys
import random

global random_player

class Random(object):
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.player = Player.ME
        self.opponent = Player.OPPONENT
        self.game = None

    def initialize(self):
        self.game = MainBoard(3)

    def add_opponent_move(self, board, opponent_move):
        self.game = self.game.add_opponent_move(board, opponent_move)

    def add_move(self, board, move):
        self.game = self.game.add_move(board, move)

    def get_my_move(self):
        """
        Returns: Player's next move
        """
        next_board_coords = self._pick_next_board()
        next_board = self.game.get_sub_board(next_board_coords)
        move = self._pick_random_move(next_board)
        return next_board_coords, move

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


def main():
    for line in sys.stdin:
        process_input(line.strip())

def process_input(line):
    if line == "init":
        random_player.initialize()
    elif line == "waiting":
        return
    elif line == "move":
        write_move(random_player.get_my_move())
    elif line.startswith("opponent"):
        received_move = line.split(" ")[1]
        board_coords_str, opponent_move_str = received_move.split(";")
        board_coords = BoardCoords(*map(int, board_coords_str.split(",")))
        opponent_move = Move(*map(int, opponent_move_str.split(",")))
        random_player.add_opponent_move(board_coords, opponent_move)
        write_move(random_player.get_my_move())

def write_move(move):
    next_board_coords = move[0]
    next_move = move[1]
    print("%d,%d;%d,%d" % (next_board_coords.row, next_board_coords.col, next_move.row, next_move.col))


if __name__ == "__main__":
    random_player = Random()
    main()
