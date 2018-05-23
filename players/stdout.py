import sys

from abc import abstractmethod

from engine import MainBoardCoords, SubBoardCoords
from players.player import UltimatePlayer


class StdOutPlayer(UltimatePlayer):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_my_move(self):
        pass

    def process_input(self, input_line: str) -> None:
        if input_line == "init":
            self.__init__()
        elif input_line == "move":
            self.get_and_publish_player_move()
        elif input_line.startswith("opponent"):
            self.react_to_opponent_move(input_line)

    def get_and_publish_player_move(self) -> None:
        main_board_coords, sub_board_coords = self.get_my_move()
        self.add_my_move(main_board_coords, sub_board_coords)
        self.write_move(main_board_coords, sub_board_coords)

    @staticmethod
    def write_move(main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        move_str = "%d,%d;%d,%d" % (
            main_board_coords.row, main_board_coords.col, sub_board_coords.row, sub_board_coords.col)
        print(move_str)
        sys.stdout.flush()

    def react_to_opponent_move(self, input_line: str):
        main_board_coords, sub_board_coords = self.read_move(input_line)
        self.add_opponent_move(main_board_coords, sub_board_coords)
        if not self.is_game_finished:
            self.get_and_publish_player_move()

    @staticmethod
    def read_move(input_line: str):
        received_move = input_line.split(" ")[1]
        main_board_coords_str, opponent_move_str = received_move.split(";")
        main_board_coords = MainBoardCoords(*map(int, main_board_coords_str.split(",")))
        sub_board_coords = SubBoardCoords(*map(int, opponent_move_str.split(",")))
        return main_board_coords, sub_board_coords
