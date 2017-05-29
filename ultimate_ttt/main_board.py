from copy import deepcopy

from .sub_board import SubBoard
from .cell import Cell
from .gameplay import Player, PlayerMove, BoardCoords
from .gameplay import is_winning_move
from .errors import MoveOutsideMainBoardError, MoveNotOnNextBoardError,\
                    BoardNotFinishedError, MoveInFinishedBoardError,\
                    MoveInPlayedCellError

class MainBoard(object):
    """An Ultimate TicTacToe board, containing several SubBoards where players play

    When the board size is 3, the main board looks like this:

    ::

        | SubBoard 0,0 | SubBoard 0,1 | SubBoard 0,2 |
        | SubBoard 1,0 | SubBoard 1,1 | SubBoard 1,2 |
        | SubBoard 2,0 | SubBoard 2,1 | SubBoard 2,2 |

    Each SubBoard looks like this:

    ::

        | Cell 0,0 | Cell 0,1 | Cell 0,2 |
        | Cell 1,0 | Cell 1,1 | Cell 1,2 |
        | Cell 2,0 | Cell 2,1 | Cell 2,2 |

    """

    def __init__(self, board_size = 3):
        if not isinstance(board_size, int) or not board_size == 3:
            raise ValueError("Size must be integer of size 3 (for now)")

        self._board_size = board_size
        self._board = [
                [SubBoard() for board_col in range(board_size)]
                for board_row in range(board_size)
            ]

        self._next_player = Player.NONE
        self._next_board_coords = None

        self._is_finished = False
        self._winner = Player.NONE

    @property
    def next_board_coords(self):
        """The next board to play on. None if the next move can be on any board"""
        return self._next_board_coords

    @property
    def is_finished(self):
        """Whether the board is finished (tied, won or lost)"""
        if self._is_finished == True:
            return True

        for row in self._board:
            for sub_board in row:
                if sub_board.is_finished == False:
                    return False

        return True

    @property
    def winner(self):
        """The winner of the board if finished. Exception otherwise"""
        if not self.is_finished:
            raise BoardNotFinishedError
        return self._winner

    def add_my_move(self, board_coords, move):
        """Adds your move to the specified sub-board

        Args:
            board_coords: The co-ordinates (row, column) of the SubBoard to play on
            move: The move (row, column) to make on the SubBoard

        Returns:
            A new MainBoard instance with the move applied
        """
        return self._add_move(board_coords, PlayerMove(Player.ME, move))

    def add_opponent_move(self, board_coords, move):
        """Adds the opponent's move to the specified sub-board

        Args:
            board_coords: The co-ordinates (row, column) of the SubBoard to play on
            move: The move (row, column) to make on the SubBoard

        Returns:
            A new MainBoard instance with the move applied
        """
        return self._add_move(board_coords, PlayerMove(Player.OPPONENT, move))

    def get_sub_board(self, board_coords):
        row = board_coords.row
        col = board_coords.col
        return self._board[row][col]

    def get_valid_boards(self):
        """Returns all board co-ordinates that are valid for the next move. Empty if board is finished.

        Returns:
            Array of valid board co-ordinates (Row, Col), e.g. [BoardCoords(2, 2),BoardCoords(1, 1)]
        """
        if self.next_board_coords is not None:
            return [self.next_board_coords]
        else:
            if self.is_finished:
                return []
            available_boards = []
            for row_index in range(0, self._board_size):
                for col_index in range(0, self._board_size):
                    if not self._board[row_index][col_index].is_finished:
                        available_boards.append(BoardCoords(row_index, col_index))
            return available_boards

    def is_valid_board_for_next_move(self, board_coords):
        """Whether this is a valid board for the next move

        Args:
            board_coords: The co-ordinates (row, column) of the SubBoard to check
        """
        if self.next_board_coords == None:
            return True
        elif self.next_board_coords == board_coords:
            return True
        return False

    def __str__(self):
        """Returns a pretty printed representation of the main board"""
        pretty_printed = ''
        #TODO: Shouldn't access sub-board private var
        board_size = len(self._board)
        board_size_range = range(board_size)
        for (mb_idx,mb_row) in enumerate(self._board):
            for sub_board_row_num in board_size_range:
                for (sb_idx,sub_board) in enumerate(mb_row):
                    for cell in sub_board._board[sub_board_row_num]:
                        pretty_printed += str(cell)+' '
                    #Print vertical separator - if not last sub_board
                    if(sb_idx < board_size - 1):
                        pretty_printed += '| '
                pretty_printed += '\n'
            #Print horizontal separators
            #Only if this is not the last row
            if(mb_idx < board_size - 1):
                for (bm_idx, board_marker) in enumerate(board_size_range):
                    for cell_marker in board_size_range:
                        pretty_printed += '- '
                    if(bm_idx < board_size - 1):
                        pretty_printed += '| '
                pretty_printed += '\n'

        return pretty_printed

    ### Private functions

    def _add_move(self, board_coords, player_move):
        """Adds a move by a ultimate_ttt_player to a deep copy of the current board, returning the copy

        Args:
            player_main_board_move: Player, co-ordinates of the SubBoard, and intended move on that SubBoard

        Returns:
            A new MainBoard instance with the move applied and all properties calculated
        """

        if self._is_finished == True:
            raise MoveInFinishedBoardError(board_coords)

        if not self._is_board_in_bounds(board_coords):
            raise MoveOutsideMainBoardError(board_coords)

        if not self.is_valid_board_for_next_move(board_coords):
            raise MoveNotOnNextBoardError(board_coords, self._next_board_coords)

        return self._copy_applying_move(board_coords, player_move)

    def _copy_applying_move(self, board_coords, player_move):
        #Apply the move to the sub board first to ensure it works
        try:
            updated_sub_board = self._board[board_coords.row][board_coords.col]\
                                    .add_move(player_move)
        except MoveInPlayedCellError as e:
            raise MoveInPlayedCellError(player_move, board_coords) from e

        #Copy the board so we can update it
        #Maybe this should all go in the constructor/classmethod
        updated_main_board = deepcopy(self)

        updated_main_board._board[board_coords.row][board_coords.col] = updated_sub_board

        #Check that the next board to play is not finished
        if not updated_main_board._board[player_move.row][player_move.col].is_finished:
            updated_main_board._next_board_coords = BoardCoords(player_move.row, player_move.col)
        else:
            updated_main_board._next_board_coords = None

        #Convert to board of cells format so we can reuse check logic
        cell_board = updated_main_board._as_cell_board()

        if is_winning_move(cell_board, PlayerMove(player_move.player, board_coords)):
            updated_main_board._is_finished = True
            updated_main_board._winner = player_move.player

        return updated_main_board

    def _as_cell_board(self):
        """Returns this main board in the form of a board of cells

        Each cell represents a sub-board of this board, with
        `cell.played_by` set to the ultimate_ttt_player that won the board (Player.NONE if tied)
        """

        return [[Cell(sub_board.winner) if sub_board.is_finished else Cell(Player.NONE) for sub_board in row] for row in self._board]

    def _is_board_in_bounds(self, coords):
        """Checks whether the given move is inside the boundaries of the main board

        Args:
            coords: The coords of the intended sub-board

        Returns:
            True if the move is within the bounds of the main board, False otherwise
        """

        if (coords.row >= 0 and coords.row < len(self._board) and
            coords.col >= 0 and coords.col < len(self._board)):
            return True
        return False
