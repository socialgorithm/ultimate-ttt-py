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

    @abstractmethod
    def timeout(self):
        pass

    @abstractmethod
    def game_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        pass

    @abstractmethod
    def match_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        pass

    def process_input(self, input_line: str) -> None:
        if input_line == "init":
            self.__init__()
        elif input_line == "move":
            self.get_and_publish_player_move()
        elif input_line.startswith("opponent"):
            self.react_to_opponent_move(input_line)
        elif input_line == "timeout":
            self.timeout()
        elif input_line.startswith("game"):
            self.react_to_game_over(input_line)
        elif input_line.startswith("match"):
            self.react_to_match_over(input_line)

    def get_and_publish_player_move(self) -> None:
        main_board_coords, sub_board_coords = self.get_my_move()
        self.add_my_move(main_board_coords, sub_board_coords)
        self.write_move(main_board_coords, sub_board_coords)

    @staticmethod
    def write_move(main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        move_str = "send:%d,%d;%d,%d" % (
            main_board_coords.row, main_board_coords.col, sub_board_coords.row, sub_board_coords.col)
        print(move_str)
        sys.stdout.flush()

    def react_to_opponent_move(self, input_line: str):
        main_board_coords, sub_board_coords = self.read_move(self, input_line)
        self.add_opponent_move(main_board_coords, sub_board_coords)
        if not self.is_game_finished:
            self.get_and_publish_player_move()

    def react_to_game_over(self, input_line: str):
        outcome = input_line.split(" ")[1]
        if (len(input_line.split(" ")) == 3):
            main_board_coords, sub_board_coords = self.read_last_move(self, input_line)
            self.game_over(outcome, main_board_coords, sub_board_coords)
        else:
            self.game_over(outcome, None, None)
        

    def react_to_match_over(self, input_line: str):
        outcome = input_line.split(" ")[1]
        if (len(input_line.split(" ")) == 3):
            main_board_coords, sub_board_coords = self.read_last_move(self, input_line)
            self.match_over(outcome, main_board_coords, sub_board_coords)
        else:
            self.match_over(outcome, None, None)

    @staticmethod
    def read_move(self, input_line: str):
        received_move = input_line.split(" ")[1]
        return self.process_move(received_move)

    @staticmethod
    def read_last_move(self, input_line: str):
        received_move = input_line.split(" ")[2]
        return self.process_move(received_move)


    @staticmethod
    def process_move(received_move: str):
        main_board_coords_str, opponent_move_str = received_move.split(";")
        main_board_coords = MainBoardCoords(*map(int, main_board_coords_str.split(",")))
        sub_board_coords = SubBoardCoords(*map(int, opponent_move_str.split(",")))
        return main_board_coords, sub_board_coords
