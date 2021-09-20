from engine import MainBoardCoords, SubBoardCoords, SubBoard, Player
from players.stdout import StdOutPlayer

class Defensive(StdOutPlayer):
    def __init__(self):
        self.move = 0
        super().__init__()

    def react_to_opponent_move(self, input_line: str):
        self.move += 1
        super().react_to_opponent_move(input_line)

    def get_my_move(self):  # -> Tuple[MainBoardCoords, SubBoardCoords]
        self.move += 1
        validBoards = self.main_board.get_playable_coords()
        weightedMoves = [x for x in [self.get_move_for_board(x) for x in validBoards] if x is not None]
        if 0<len(weightedMoves):
            return weightedMoves[0]
        #fall back to the first available logic
        main_board_coords = self.main_board.get_playable_coords()[0]
        sub_board = self.main_board.get_sub_board(main_board_coords)
        sub_board_coords = sub_board.get_playable_coords()[0]
        return main_board_coords, sub_board_coords

    def get_move_for_board(self, board):
        subBoard = self.main_board.get_sub_board(board)
        opponentWinningPositions = self.get_closeable_positions(board, Player.OPPONENT)
        if 0<len(opponentWinningPositions):
            return (board, opponentWinningPositions[0])
        myWinningPositions = self.get_closeable_positions(board, Player.ME)
        if 0<len(myWinningPositions):
            return (board, myWinningPositions[0])
        return None


    def _column(self, board, n):
        return [x[n] for x in board]

    def _columns(self, board):
        return [self._column(board,x) for x in range(len(board[0]))]

    def _major_diagonal(self, board):
        return [board[x][x] for x in range(len(board[0]))]

    def _minor_diagonal(self, board):
        n = len(board[0])
        return [board[x][n-1-x] for x in range(n)]

    def get_winning_position(self, cells, playerNo):
        playerScore = sum([1 if x.played_by == playerNo else 0 for x in cells])
        if playerScore == len(cells)-1:
            notPlayed = [i for i,x in enumerate(cells) if x.played_by == Player.NONE]
            if 0<len(notPlayed):
                return notPlayed[0]
        return None

    def get_closeable_positions(self, board, playerNo):
        subBoard = self.main_board.get_sub_board(board)
        rows=([SubBoardCoords(i,x) for i,x in enumerate([self.get_winning_position(row, playerNo) for row in subBoard]) if x is not None]
            + [SubBoardCoords(x,i) for i,x in enumerate([self.get_winning_position(column, playerNo) for column in self._columns(subBoard)]) if x is not None]
            + (lambda x:[SubBoardCoords(x,x)] if x is not None else [])(self.get_winning_position(self._major_diagonal(subBoard), playerNo))
            + (lambda x:[SubBoardCoords(x,len(subBoard[0])-1-x)] if x is not None else [])(self.get_winning_position(self._minor_diagonal(subBoard), playerNo)))
        return [x for x in rows if x is not None]

    def timeout(self):
        return

    def game_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        return

    def match_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        return
