"""
The TicTacToe Engine module, containing the board and all move logic

When the board size is 3, the main board looks like this:

| SubBoard 1,1 | SubBoard 1,2 | SubBoard 1,3 |
| SubBoard 2,1 | SubBoard 2,2 | SubBoard 2,3 |
| SubBoard 3,1 | SubBoard 3,2 | SubBoard 3,3 |

Each SubBoard looks like this:

| Square 1,1 | Square 1,2 | Square 1,3 |
| Square 2,1 | Square 2,2 | Square 2,3 |
| Square 3,1 | Square 3,2 | Square 3,3 |

To play in Square(2,2) in SubBoard(1,1), call move as follows:

play_square_in_sub_board([2,2],[1,1])

"""

class TicTacToe(object):
    """TicTacToe board class"""
    def __init__(self, board_size = 3):
        if not isinstance(board_size, int) or board_size < 3 or board_size > 10:
            raise ValueError("Size must be a number between 3 and x")

        self.board_size = board_size
        self.maxMoves = self.board_size * self.board_size

        self.board = [
            [
                [
                    [
                        0 for sub_board_x in range(board_size)
                    ]
                    for sub_board_y in range(board_size)
                ]
                for main_board_x in range(board_size)
            ]
            for main_board_y in range(board_size)
        ]

        self.pretty_print_board()

    def play_square_in_sub_board(self, square_x, square_y, board_x, board_y):
        if not self.is_in_bounds(square_x, square_y):
            raise MoveOutsideSubBoardError('Failed! Square '+str(square_x)+','+str(square_y)+' out of bounds!')

        if not self.is_in_bounds(board_x, board_y):
            raise MoveOutsideMainBoardError('Failed! Board '+str(board_x)+','+str(board_y)+' out of bounds!')

        if self.is_square_filled(sq_x, sq_y, board_x, board_y):
            raise MoveInFilledSquareError('Failed! Square '+str(square_x)+','+str(square_y)+' in board '+str(board_x)+','+str(board_y)+' already filled')


    def is_in_bounds(self, x, y):
        if x < 1 or x > self.board_size or y < 1 or y > self.board_size:
            return False

    def is_square_filled(self, sq_x, sq_y, board_x, board_y):
        return True

    def is_board_full():
        return

    def pretty_print_board(self):
        for main_board_row in self.board:
            for sub_board in main_board_row:
                for sub_board_row in sub_board:
                    for square in sub_board_row:
#                        print(square, end='|')
                print '\n'

#Errors

class MoveIncompleteError(Exception):
    pass

class MoveOutsideSubBoardError(Exception):
    pass

class MoveOutsideMainBoardError(Exception):
    pass

class MoveInFilledSquareError(Exception):
    pass
