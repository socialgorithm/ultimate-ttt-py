import sys

from abc import abstractmethod

from engine import MainBoardCoords, SubBoardCoords
from players.player import UltimatePlayer


class StdOutPlayer(UltimatePlayer):

    @abstractmethod
    def get_my_move(self):
        pass

    def process_input(self, line):
        if line == "move":
            main_board_coords, sub_board_coords = self.get_my_move()
            self.add_my_move(main_board_coords, sub_board_coords)
            self.write_move(main_board_coords, sub_board_coords)
        elif line.startswith("opponent"):
            received_move = line.split(" ")[1]
            main_board_coords_str, opponent_move_str = received_move.split(";")
            main_board_coords = MainBoardCoords(*map(int, main_board_coords_str.split(",")))
            sub_board_coords = SubBoardCoords(*map(int, opponent_move_str.split(",")))
            self.add_opponent_move(main_board_coords, sub_board_coords)
            if not self.is_game_finished:
                main_board_coords, sub_board_coords = self.get_my_move()
                self.add_my_move(main_board_coords, sub_board_coords)
                self.write_move(main_board_coords, sub_board_coords)
            else:
                # Match finished
                sys.stdout.flush()
                return

    @staticmethod
    def write_move(main_board_coords, sub_board_coords):
        move_str = "%d,%d;%d,%d" % (
            main_board_coords.row, main_board_coords.col, sub_board_coords.row, sub_board_coords.col)
        print(move_str)
        sys.stdout.flush()
