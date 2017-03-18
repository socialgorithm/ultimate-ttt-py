import pytest
from ultimate_ttt import MainBoard, BoardCoords, Move
from ultimate_ttt.errors import MoveOutsideMainBoardError, MoveOutsideSubBoardError

def test_whenInitSizeIsStringThenExceptionRaised():
    with pytest.raises(ValueError):
        MainBoard("mustFail")

# We only support size 3 boards for now
def test_whenInitSizeNot3ExceptionRaised():
    with pytest.raises(ValueError):
        MainBoard(4)

    with pytest.raises(ValueError):
        MainBoard(2)

def test_whenNoGivenSizeThenSizeIs3():
    board = MainBoard()._board

    assert len(board) == 3  #Rows
    for row in board:
        assert len(row) == 3 #Columns


def test_whenBoardInitializedThenAllSubBoardsInitialized():
    board = MainBoard(3)._board

    assert len(board) == 3 #Rows
    for row in board:
        assert len(row) == 3 #Columns
        for sub_board in row:
            assert str(sub_board) == '0 0 0 \n0 0 0 \n0 0 0 \n'

def test_whenBoardNewThenBoardIsNotFinished():
    assert MainBoard().is_finished == False

def test_whenNewMoveBoardCoordsAreOutOfBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideMainBoardError):
        MainBoard().add_my_move(BoardCoords(1, 3), Move(0, 0))

    with pytest.raises(MoveOutsideMainBoardError):
        MainBoard().add_opponent_move(BoardCoords(3, 1), Move(0, 0))

def test_whenNewMoveIsOutsideValidSubBoardBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideSubBoardError):
        MainBoard().add_my_move(BoardCoords(1, 1), Move(1, 3))

def whenNewMoveIsNotOnAvailableNextBoardThenExceptionRaised():
    assert False

def whenNextBoardIsFinishedThenAnyBoardCanBePlayed():
    assert False

def whenBoardSize3Then0x0IsOutOfBounds():
    assert False

def whenBoardSize3Then3x3IsInBounds():
    assert False

def whenBoardIsPrettyPrintedThenItIsRenderedCorrectly():
    MainBoard(3).pretty_print_board()

def areBoardDimensionXbyX(board, x):
    if not len(board) == x:
        return False

    for row in board:
        if not len(row) == x:
            return False

    return True

def whenMoveIsOutOfMainBoardBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideMainBoardError):
        MainBoard(3).play_square_in_sub_board(1,2,3,4)

def whenMaxMovesExceededThenBoardIsFull():
    assert False

def whenWinnerGetsSetOrBoardIsFullThenBoardIsFinished():
    assert False

def whenBoardIsFullAndMoveAttemptedThenExceptionRaised():
    assert False

def whenRowFilledThenRowCheckReturnsWon():
    assert False

def whenRowNotFilledThenRowCheckReturnsNotWon():
    assert False

def whenColumnFilledThenColumnCheckReturnsWon():
    assert False

def whenColumnNotFilledThenColumnCheckReturnsNotWon():
    assert False

#Do both here?
def whenDiagonalFilledThenDiagonalCheckReturnsWon():
    assert False

def whenDiagonalNotFilledThenDiagonalCheckReturnsNotWon():
    assert False

def whenBoardIsFinishedAndWinnerNotSetThenSetResultToTie():
    assert False
