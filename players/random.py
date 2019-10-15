import random

from engine import MainBoardCoords, SubBoardCoords, SubBoard
from players.stdout import StdOutPlayer


class Random(StdOutPlayer):
    #
    # New Game Has Been Started.
    # Do Whatever You Need To Do For The Player To Be Ready To Play
    #
    def __init__(self):
        super().__init__()

    #
    # You are the First To Move
    # Place Whereever You Want
    # You Get To Pick The Board
    #
    # Returns Tuple[MainBoardCoords, SubBoardCoords] Position coordinates {board: [row, col], cell: [row, col]}
    #
    def onMove(self):
        board = self.pick_next_main_board_coords()
        sub_board = self.main_board.get_sub_board(board)
        move = self.pick_random_sub_board_coords(sub_board)
        return board, move

    #
    # Opponent Has Moved.
    # You Have Opponents Board
    # You Have Opponents Move
    #
    # You Must Respond With Board Matching Opponents Move
    # Unless That Board Is Complete
    #
    # Returns Tuple[MainBoardCoords, SubBoardCoords] Position coordinates {board: [row, col], cell: [row, col]}
    #
    def onOpponent(self, board, move):
        sub_board = self.main_board.get_sub_board(move)
        if sub_board.is_finished == True:
            return self.onMove()
        sub_board_coords = self.pick_random_sub_board_coords(sub_board)
        return move, sub_board_coords

    #
    # Game Is Over.
    # You May Wish To Change Stratagy For The New Game.
    # Your Opponent Has Not Changed.
    # 
    # result Either 'win' | 'lose' | 'tie'
    # board Last Opponent Board identifier [row, col]
    # move Last Opponent Cell identifier [row, col]
    #
    def gameOver(self, result, board, move):
        if result == "win":
            # DO SOMETHING FOR WIN
            pass
        elif result == "lose":
            # DO SOMETHING FOR LOST
            pass
        elif result == "tie":
            # DO SOMETHING FOR TIE
            pass
        return

    #
    # Match Is Over.
    # You Will Soon Have A New Opponent.
    # 
    # result Either 'win' | 'lose' | 'tie'
    #
    def matchOver(self, result):
        if result == "win":
            # DO SOMETHING FOR WIN
            pass
        elif result == "lose":
            # DO SOMETHING FOR LOST
            pass
        elif result == "tie":
            # DO SOMETHING FOR TIE
            pass
        return

    #
    # Game Lost.
    # You Have Timed Out.
    #
    def timeout(self):
        # DO SOMETHING FOR TIMEOUT
        return

    def pick_next_main_board_coords(self) -> MainBoardCoords:
        if self.main_board.sub_board_next_player_must_play is None:
            return random.choice(self.main_board.get_playable_coords())
        else:
            return self.main_board.sub_board_next_player_must_play

    @staticmethod
    def pick_random_sub_board_coords(sub_board: SubBoard) -> SubBoardCoords:
        return random.choice(sub_board.get_playable_coords())
