from engine import MainBoardCoords, SubBoardCoords, SubBoard
from players.stdout import StdOutPlayer


class FirstAvailable(StdOutPlayer):
    def __init__(self):
        super().__init__()

    def get_my_move(self):  # -> Tuple[MainBoardCoords, SubBoardCoords]
        main_board_coords = self.main_board.get_playable_coords()[0]
        sub_board = self.main_board.get_sub_board(main_board_coords)
        sub_board_coords = sub_board.get_playable_coords()[0]
        return main_board_coords, sub_board_coords

    def timeout(self):
        return

    def game_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        return

    def match_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        return
