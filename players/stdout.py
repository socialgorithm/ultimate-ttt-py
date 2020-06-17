import sys

from abc import abstractmethod

from engine import MainBoardCoords, SubBoardCoords
from players.player import UltimatePlayer


class StdOutPlayer(UltimatePlayer):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def onMove(self):
        pass

    @abstractmethod
    def onOpponent(self, board, move):
        pass

    @abstractmethod
    def gameOver(self, result, board, move):
        pass

    @abstractmethod
    def matchOver(self, result):
        pass
    
    @abstractmethod
    def timeout(self):
        pass

    def process_input(self, input_line: str) -> None:
        try:
            if input_line == "init":
                self.__init__()
            elif input_line == "move":
                self.react_to_move()
            elif input_line.startswith("opponent"):
                self.react_to_opponent_move(input_line)
            elif input_line.startswith("game"):
                self.react_to_game_over(input_line)
            elif input_line.startswith("match"):
                self.react_to_match_over(input_line)
            elif input_line == "timeout":
                self.react_to_timeout(input_line)
        except:
            print("ERROR: Failed To Process Message. May Forfit Game, But Should Reinitilize On New Game.")

    def react_to_move(self) -> None:
        main_board_coords, sub_board_coords = self.onMove()
        self.add_my_move(main_board_coords, sub_board_coords)
        self.write_move(main_board_coords, sub_board_coords)

    def react_to_opponent_move(self, input_line: str):
        main_board_coords, sub_board_coords = self.read_move_opponent(input_line)
        self.add_opponent_move(main_board_coords, sub_board_coords)
        my_main_board_coords, my_sub_board_coords = self.onOpponent(main_board_coords, sub_board_coords)
        self.add_my_move(my_main_board_coords, my_sub_board_coords)
        self.write_move(my_main_board_coords, my_sub_board_coords)

    def react_to_game_over(self, input_line: str):
        result, main_board_coords, sub_board_coords = self.read_result_move_game(input_line)
        if main_board_coords is not None and sub_board_coords is not None:
            self.add_opponent_move(main_board_coords, sub_board_coords)
        self.gameOver(result, main_board_coords, sub_board_coords)

    def react_to_match_over(self, input_line: str):
        result = self.read_result_match(input_line)
        self.matchOver(result)

    def react_to_timeout(self, input_line: str):
        self.timeout()

    @staticmethod
    def write_move(main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        move_str = "send:%d,%d;%d,%d" % (
            main_board_coords.row, main_board_coords.col, sub_board_coords.row, sub_board_coords.col)
        print(move_str)
        sys.stdout.flush()

    @staticmethod
    def parse_move(received_move: str):
        main_board_coords_str, opponent_move_str = received_move.split(";")
        main_board_coords = MainBoardCoords(*map(int, main_board_coords_str.split(",")))
        sub_board_coords = SubBoardCoords(*map(int, opponent_move_str.split(",")))
        return main_board_coords, sub_board_coords

    @staticmethod
    def read_move_opponent(input_line: str):
        received_move = input_line.split(" ")[1]
        return StdOutPlayer.parse_move(received_move)

    @staticmethod
    def read_result_move_game(input_line: str):
        message_split = input_line.split(" ")
        if len(message_split) == 3:
            received_move = message_split[2]
            main_board_coords, sub_board_coords = StdOutPlayer.parse_move(received_move)
            return message_split[1], main_board_coords, sub_board_coords
        return message_split[1], None, None

    @staticmethod
    def read_result_match(input_line: str):
        return input_line.split(" ")[1]
