import pytest
from ultimate_ttt import SubBoard, Player, Move
from ultimate_ttt.errors import MoveOutsideSubBoardError, MoveInPlayedCellError,\
                                BoardNotFinishedError, MoveInFinishedBoardError

def test_whenGivenSizeIsStringThenExceptionRaised():
    with pytest.raises(ValueError):
        SubBoard("mustFail")

# We only support size 3 boards for now
def test_whenGivenSizeNot3ExceptionRaised():
    with pytest.raises(ValueError):
        SubBoard(4)

    with pytest.raises(ValueError):
        SubBoard(2)

def test_whenNoGivenSizeThenSizeIs3():
    board = SubBoard()._board

    assert len(board) == 3  #Rows
    for row in board:
        assert len(row) == 3 #Columns

def test_whenBoardInitializedThenAllCellsAreUnplayed():
    board = SubBoard(3)._board

    assert len(board) == 3 #Rows
    for row in board:
        assert len(row) == 3 #Columns
        for cell in row:
            assert cell.played_by == Player.NONE

def test_whenBoardNewThenBoardIsNotFinished():
    assert SubBoard().is_finished == False

def test_whenNewMoveIsOutsideBoardBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideSubBoardError):
        SubBoard().add_my_move(Move(1, 3))

    with pytest.raises(MoveOutsideSubBoardError):
        SubBoard().add_opponent_move(Move(-1, 1))

def test_whenNewMoveIsInValidCellThenReturnedBoardHasMove():
    assert SubBoard().add_my_move(Move(0, 0))\
            ._board[0][0].played_by == Player.ME

    assert SubBoard().add_opponent_move(Move(0, 0))\
            ._board[0][0].played_by == Player.OPPONENT

def test_whenNewMoveIsInAlreadyPlayedCellThenExceptionRaised():
    board = SubBoard().add_my_move(Move(1, 2))
    string_board = str(board)
    move_count_before = board._moves_so_far

    with pytest.raises(MoveInPlayedCellError):
        board = board.add_opponent_move(Move(1, 2))

    #Ensure board state has not changed
    assert string_board == str(board)
    assert board._moves_so_far == move_count_before

def test_whenBoardIsNotFinishedThenGetWinnerRaisesException():
    with pytest.raises(BoardNotFinishedError):
        SubBoard().winner

def test_whenRowIsWonThenBoardIsFinishedAndWon():
    #LTR Diag check
    i_win = SubBoard().add_my_move(Move(0, 0))\
                        .add_my_move(Move(1, 1))\
                        .add_my_move(Move(2, 2))

    assert i_win.is_finished == True
    assert i_win.winner == Player.ME

    #RTL Diag check
    i_win = SubBoard().add_my_move(Move(0, 2))\
                    .add_my_move(Move(1, 1))\
                    .add_my_move(Move(2, 0))

    assert i_win.is_finished == True
    assert i_win.winner == Player.ME

    #Row check
    opponent_wins = SubBoard().add_opponent_move(Move(1, 0))\
                        .add_opponent_move(Move(1, 1))\
                        .add_opponent_move(Move(1, 2))

    assert opponent_wins.is_finished == True
    assert opponent_wins.winner == Player.OPPONENT

    #Col check
    opponent_wins = SubBoard().add_opponent_move(Move(0, 1))\
                        .add_opponent_move(Move(1, 1))\
                        .add_opponent_move(Move(2, 1))

    assert opponent_wins.is_finished == True
    assert opponent_wins.winner == Player.OPPONENT

def test_whenRowIsBlockedThenBoardIsNotFinished():
    blocked = SubBoard().add_my_move(Move(0, 0))\
                            .add_my_move(Move(1, 1))\
                            .add_opponent_move(Move(2, 2))

    assert blocked.is_finished == False
    with pytest.raises(BoardNotFinishedError):
        blocked.winner

def test_whenNewMoveIsInFinishedBoardThenExceptionRaised():
    finished_board = SubBoard().add_my_move(Move(0, 0))\
                        .add_my_move(Move(0, 1))\
                        .add_my_move(Move(0, 2))

    with pytest.raises(MoveInFinishedBoardError):
        finished_board.add_my_move(Move(1, 1))

def test_whenBoardIsInProgressThenBoardIsNotFinished():
    assert SubBoard().add_my_move(Move(0, 0))\
                .add_my_move(Move(0, 1))\
                .add_opponent_move(Move(0, 2))\
                .is_finished == False

def test_whenBoardReachesMaxMovesThenBoardIsFinishedAndTied():
    tied_board = SubBoard().add_my_move(Move(0, 0))\
                .add_opponent_move(Move(2, 2))\
                .add_my_move(Move(2, 0))\
                .add_opponent_move(Move(1, 0))\
                .add_my_move(Move(0, 2))\
                .add_opponent_move(Move(0, 1))\
                .add_my_move(Move(1, 2))\
                .add_opponent_move(Move(1, 1))\
                .add_my_move(Move(2, 1))

    assert tied_board.is_finished == True
    assert tied_board.winner == Player.NONE

def test_whenBoardIsPlayedThenStringRepresentationIsCorrect():
    board = SubBoard().add_my_move(Move(0,0))\
                .add_opponent_move(Move(1,1))\
                .add_my_move(Move(2,2))

    assert str(board) == "1 0 0 \n0 2 0 \n0 0 1 \n"
