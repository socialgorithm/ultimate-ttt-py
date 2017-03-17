import pytest
from ultimate_ttt import SubBoard, Player, Move
from ultimate_ttt.errors import MoveOutsideSubBoardError, MoveInPlayedCellError

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
    assert SubBoard().is_finished() == False

def test_whenNewMoveIsOutsideBoardBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideSubBoardError):
        SubBoard().add_my_move(Move(1, 3))

    with pytest.raises(MoveOutsideSubBoardError):
        SubBoard().add_opponent_move(Move(-1, 1))

def test_whenNewMoveIsInValidCellThenReturnedBoardHasMove():
    assert SubBoard().add_my_move(Move(0, 0))._board[0][0].played_by == Player.ME
    assert SubBoard().add_opponent_move(Move(0, 0))._board[0][0].played_by == Player.OPPONENT

def test_whenNewMoveIsInAlreadyPlayedCellThenExceptionRaised():
    board = SubBoard().add_my_move(Move(1, 2))
    stringBoard = str(board)
    with pytest.raises(MoveInPlayedCellError):
        board = board.add_opponent_move(Move(1, 2))
    #Ensure board state has not changed
    assert stringBoard == str(board)

def whenNewMoveIsInFinishedBoardThenExceptionRaised():
    assert False

def whenMoveIsPlayedThenNewBoardHasMove():
    assert False

def whenBoardIsInProgressThenBoardIsNotFinished():
    sub_board = SubBoard()

def whenBoardIsFullThenBoardIsFinished():
    assert False

def whenBoardIsWonThenBoardIsFinished():
    assert False

def whenBoardIsLostThenBoardIsFinished():
    assert False

def whenBoardIsNotFinishedThenResultCheckThrowsException():
    assert False

def whenBoardIsWonByMeThenResultReturnsPlayerMe():
    assert False

def whenBoardIsWonByOpponentThenResultReturnsPlayerOpponent():
    assert False

def whenMoveIsMadeInFreeSquareThenSquareRecordsId():
    assert False

def whenValidMoveIsMadeThenMoveCounterIsIncremented():
    assert False

def whenInvalidMoveIsMadeThenMoveCounterNotIncremented():
    assert False
