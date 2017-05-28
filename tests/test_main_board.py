import pytest
from ultimate_ttt import MainBoard, BoardCoords, Move, Player, PlayerMove
from ultimate_ttt.errors import MoveOutsideMainBoardError, MoveOutsideSubBoardError,\
                            MoveNotOnNextBoardError, MoveInFinishedBoardError, BoardNotFinishedError

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

def test_whenNewMoveIsNotOnGameNextBoardThenExceptionRaised():
    board = MainBoard().add_my_move(BoardCoords(0, 0), Move(1, 1))

    #Move must now be on board at 1, 1
    with pytest.raises(MoveNotOnNextBoardError):
        board.add_opponent_move(BoardCoords(1, 0), Move(1, 1))

def test_whenNextBoardIsAvailableThenGetValidBoardsReturnsOnlyThatBoard():
    board = MainBoard().add_my_move(BoardCoords(0, 0), Move(2, 2))

    #Only valid board now should be 2, 2
    assert len(board.get_valid_boards()) == 1
    assert board.get_valid_boards()[0] == BoardCoords(2, 2)

def test_whenNextBoardIsFinishedThenAnyBoardCanBePlayed():
    main_board = MainBoard()
    #Force some sub_board plays to finish a board
    finished_sub_board = main_board._board[2][2]\
                                    .add_my_move(Move(0, 0))\
                                    .add_my_move(Move(1, 1))\
                                    .add_my_move(Move(2, 2))

    #Set that sub-board where the next_board_coords will be
    main_board._board[2][2] = finished_sub_board
    #Play a move that will make the finished board the next board (Move 2, 2)
    main_board = main_board.add_my_move(BoardCoords(0, 0), Move(2, 2))
    #Playing anywhere is now allowed
    assert main_board.next_board_coords == None
    assert main_board.is_valid_board_for_next_move(BoardCoords(1, 1)) == True
    main_board.add_opponent_move(BoardCoords(0, 0), Move(1, 1))

def test_whenNextBoardIsFinishedThenGetValidBoardsReturnsAllAvailableBoards():
    main_board = MainBoard()
    #Force some sub_board plays to finish a board
    finished_sub_board = main_board._board[2][2]\
                                    .add_my_move(Move(0, 0))\
                                    .add_my_move(Move(1, 1))\
                                    .add_my_move(Move(2, 2))

    #Set that sub-board where the next_board_coords will be
    main_board._board[2][2] = finished_sub_board
    #Play a move that will make the finished board the next board (Move 2, 2)
    main_board = main_board.add_my_move(BoardCoords(0, 0), Move(2, 2))
    #Playing anywhere is now allowed
    available_boards = main_board.get_valid_boards()
    expected_boards = [BoardCoords(0, 0), BoardCoords(0, 1), BoardCoords(0, 2),\
                        BoardCoords(1, 0), BoardCoords(1, 1), BoardCoords(1, 2),\
                        BoardCoords(2, 0), BoardCoords(2, 1)]
    assert len(available_boards) == 8
    assert available_boards == expected_boards

def test_whenAllSubBoardsAreFinishedThenMainBoardIsFinished():
    main_board = MainBoard(3)

    for row in main_board._board:
        for sub_board in row:
            sub_board._is_finished = True

    assert main_board.is_finished == True

def test_whenMainBoardIsNotFinishedThenWinnerCheckRaisesException():
    with pytest.raises(BoardNotFinishedError):
        MainBoard().winner

def test_whenRowOfSubBoardsIsWonThenMainBoardIsWon():

    #LTR Diag check
    ltr_check = MainBoard()
    ltr_check = force_sub_board_win(ltr_check, 0, 0, Player.ME)
    ltr_check = force_sub_board_win(ltr_check, 1, 1, Player.ME)
    ltr_check = force_sub_board_win(ltr_check, 2, 2, Player.ME)

    print(str(ltr_check))

    assert ltr_check.is_finished == True
    assert ltr_check.winner == Player.ME

    #RTL Diag check
    rtl_check = MainBoard()
    rtl_check = force_sub_board_win(rtl_check, 0, 2, Player.OPPONENT)
    rtl_check = force_sub_board_win(rtl_check, 1, 1, Player.OPPONENT)
    rtl_check = force_sub_board_win(rtl_check, 2, 0, Player.OPPONENT)

    assert rtl_check.is_finished == True
    assert rtl_check.winner == Player.OPPONENT

    #Row check
    row_check = MainBoard()
    row_check = force_sub_board_win(row_check, 0, 0, Player.ME)
    row_check = force_sub_board_win(row_check, 1, 0, Player.ME)
    row_check = force_sub_board_win(row_check, 2, 0, Player.ME)

    assert row_check.is_finished == True
    assert row_check.winner == Player.ME

    #Col check
    col_check = MainBoard()
    col_check = force_sub_board_win(col_check, 0, 2, Player.OPPONENT)
    col_check = force_sub_board_win(col_check, 1, 2, Player.OPPONENT)
    col_check = force_sub_board_win(col_check, 2, 2, Player.OPPONENT)

    assert col_check.is_finished == True
    assert col_check.winner == Player.OPPONENT

def test_whenMainBoardIsFinishedThenNewMoveRaisesException():
    main_board = MainBoard()
    main_board._is_finished = True

    with pytest.raises(MoveInFinishedBoardError):
        main_board.add_my_move(BoardCoords(1, 1), Move(1, 1))

def test_whenAllSubBoardsFinishedWithNoWinnerThenResultIsATie():
    main_board = MainBoard(3)
    main_board = force_sub_board_win(main_board, 0, 0, Player.ME)
    main_board = force_sub_board_win(main_board, 1, 1, Player.OPPONENT)
    main_board = force_sub_board_tie(main_board, 2, 2)
    main_board = force_sub_board_tie(main_board, 0, 1)
    main_board = force_sub_board_tie(main_board, 1, 0)
    main_board = force_sub_board_tie(main_board, 1, 2)
    main_board = force_sub_board_tie(main_board, 2, 1)
    main_board = force_sub_board_win(main_board, 0, 2, Player.ME)
    main_board = force_sub_board_win(main_board, 2, 0, Player.OPPONENT)

    assert main_board.is_finished == True
    assert main_board.winner == Player.NONE

def test_whenBoardIsPrettyPrintedThenItIsRenderedCorrectly():
    string_board = str(MainBoard(3).add_my_move(BoardCoords(0, 0), Move(1, 1))\
                                    .add_opponent_move(BoardCoords(1, 1), Move(2, 2))\
                                    .add_opponent_move(BoardCoords(2, 2), Move(0, 0)))

    assert string_board == "0 0 0 | 0 0 0 | 0 0 0 \n"+\
                            "0 1 0 | 0 0 0 | 0 0 0 \n"+\
                            "0 0 0 | 0 0 0 | 0 0 0 \n"+\
                            "- - - | - - - | - - - \n"+\
                            "0 0 0 | 0 0 0 | 0 0 0 \n"+\
                            "0 0 0 | 0 0 0 | 0 0 0 \n"+\
                            "0 0 0 | 0 0 2 | 0 0 0 \n"+\
                            "- - - | - - - | - - - \n"+\
                            "0 0 0 | 0 0 0 | 2 0 0 \n"+\
                            "0 0 0 | 0 0 0 | 0 0 0 \n"+\
                            "0 0 0 | 0 0 0 | 0 0 0 \n"

def test_whenBoardIsPlayedThenGetValidBoardsReturnsCorrectly():
    main_board = MainBoard(3)
    main_board = force_sub_board_win(main_board, 0, 0, Player.ME)
    main_board = force_sub_board_win(main_board, 1, 1, Player.OPPONENT)

    valid_boards = main_board.get_valid_boards()
    assert(len(valid_boards) == 7)
    assert(BoardCoords(0, 0) not in valid_boards)
    assert(BoardCoords(1, 1) not in valid_boards)
    assert(BoardCoords(2, 2) in valid_boards)

def test_getSubBoardReturnsCorrectly():
    main_board = MainBoard(3)
    main_board = force_sub_board_win(main_board, 0, 0, Player.ME)
    sub_board = main_board.get_sub_board(BoardCoords(0, 0))
    assert(sub_board.is_finished)
    assert(sub_board.winner == Player.ME)

    other_sub_board = main_board.get_sub_board(BoardCoords(0, 1))
    assert(not other_sub_board.is_finished)

def force_sub_board_win(main_board, board_row, board_col, player):
    return main_board._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(player, Move(0, 0)))\
                ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(player, Move(1, 1)))\
                ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(player, Move(2, 2)))

def force_sub_board_tie(main_board, board_row, board_col):
    return main_board._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.ME, Move(0, 0)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.OPPONENT, Move(1, 1)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.ME, Move(2, 2)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.OPPONENT, Move(0, 2)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.ME, Move(2, 0)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.OPPONENT, Move(1, 0)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.ME, Move(1, 2)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.OPPONENT, Move(2, 1)))\
                        ._copy_applying_move(BoardCoords(board_row, board_col), PlayerMove(Player.ME, Move(0, 1)))
