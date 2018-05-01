import pytest
from engine import MainBoard, MainBoardCoords, SubBoardCoords, Player
from engine.errors import MoveOutsideMainBoardError, MoveOutsideSubBoardError, \
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

    assert len(board) == 3  # Rows
    for row in board:
        assert len(row) == 3  # Columns


def test_whenBoardInitializedThenAllSubBoardsInitialized():
    board = MainBoard(3)._board

    assert len(board) == 3  # Rows
    for row in board:
        assert len(row) == 3  # Columns
        for sub_board in row:
            assert str(sub_board) == '0 0 0 \n0 0 0 \n0 0 0 \n'


def test_whenSubBoardsArePlayedThenGetSubBoardReturnsCorrectly():
    main_board = MainBoard(3)
    main_board = force_sub_board_win(main_board, 0, 0, Player.ME)
    sub_board = main_board.get_sub_board(MainBoardCoords(0, 0))
    assert (sub_board.is_finished)
    assert (sub_board.winner == Player.ME)

    other_sub_board = main_board.get_sub_board(MainBoardCoords(0, 1))
    assert (not other_sub_board.is_finished)


def test_whenBoardNewThenBoardIsNotFinished():
    assert MainBoard().is_finished == False


def test_whenNewMoveSubBoardCoordsAreOutOfBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideMainBoardError):
        MainBoard().add_my_move(MainBoardCoords(1, 3), SubBoardCoords(0, 0))

    with pytest.raises(MoveOutsideMainBoardError):
        MainBoard().add_opponent_move(MainBoardCoords(3, 1), SubBoardCoords(0, 0))


def test_whenNewMoveIsOutsideValidSubBoardBoundsThenExceptionRaised():
    with pytest.raises(MoveOutsideSubBoardError):
        MainBoard().add_my_move(MainBoardCoords(1, 1), SubBoardCoords(1, 3))


def test_whenNewMoveIsNotOnGameNextBoardThenExceptionRaised():
    board = MainBoard().add_my_move(MainBoardCoords(0, 0), SubBoardCoords(1, 1))

    # Move must now be on board at 1, 1
    with pytest.raises(MoveNotOnNextBoardError):
        board.add_opponent_move(MainBoardCoords(1, 0), SubBoardCoords(1, 1))


def test_whenNextBoardIsAvailableThenGetValidBoardsReturnsOnlyThatBoard():
    board = MainBoard().add_my_move(MainBoardCoords(0, 0), SubBoardCoords(2, 2))

    # Only valid board now should be 2, 2
    assert len(board.get_playable_sub_board_coords()) == 1
    assert board.get_playable_sub_board_coords()[0] == MainBoardCoords(2, 2)


def test_whenNextBoardIsFinishedThenAnyBoardCanBePlayed():
    main_board = MainBoard()
    # Force some sub_board plays to finish a board
    finished_sub_board = main_board._board[2][2] \
        .add_my_move(SubBoardCoords(0, 0)) \
        .add_my_move(SubBoardCoords(1, 1)) \
        .add_my_move(SubBoardCoords(2, 2))

    # Set that sub-board where the sub_board_next_player_must_play will be
    main_board._board[2][2] = finished_sub_board
    # Play a move that will make the finished board the next board (Move 2, 2)
    main_board = main_board.add_my_move(MainBoardCoords(0, 0), SubBoardCoords(2, 2))
    # Playing anywhere is now allowed
    assert main_board.sub_board_next_player_must_play == None
    assert main_board.is_playing_on_sub_board_allowed(MainBoardCoords(1, 1)) == True
    main_board.add_opponent_move(MainBoardCoords(0, 0), SubBoardCoords(1, 1))


def test_whenMainBoardIsFinishedThenGetValidBoardsIsEmpty():
    main_board = MainBoard()
    main_board = force_sub_board_win(main_board, 0, 0, Player.ME)
    main_board = force_sub_board_win(main_board, 1, 1, Player.ME)
    main_board = force_sub_board_win(main_board, 2, 2, Player.ME)

    assert len(main_board.get_playable_sub_board_coords()) == 0


def test_whenNextBoardIsFinishedThenGetValidBoardsReturnsAllAvailableBoards():
    main_board = MainBoard()
    # Force some sub_board plays to finish a board
    finished_sub_board = main_board._board[2][2] \
        .add_my_move(SubBoardCoords(0, 0)) \
        .add_my_move(SubBoardCoords(1, 1)) \
        .add_my_move(SubBoardCoords(2, 2))

    # Set that sub-board where the sub_board_next_player_must_play will be
    main_board._board[2][2] = finished_sub_board
    # Play a move that will make the finished board the next board (Move 2, 2)
    main_board = main_board.add_my_move(MainBoardCoords(0, 0), SubBoardCoords(2, 2))
    # Playing anywhere is now allowed
    valid_boards = main_board.get_playable_sub_board_coords()
    assert len(valid_boards) == 8
    assert valid_boards == [MainBoardCoords(0, 0), MainBoardCoords(0, 1), MainBoardCoords(0, 2),
                            MainBoardCoords(1, 0), MainBoardCoords(1, 1), MainBoardCoords(1, 2),
                            MainBoardCoords(2, 0), MainBoardCoords(2, 1)]


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
    # LTR Diag check
    ltr_check = MainBoard()
    ltr_check = force_sub_board_win(ltr_check, 0, 0, Player.ME)
    ltr_check = force_sub_board_win(ltr_check, 1, 1, Player.ME)
    ltr_check = force_sub_board_win(ltr_check, 2, 2, Player.ME)

    print(str(ltr_check))

    assert ltr_check.is_finished == True
    assert ltr_check.winner == Player.ME

    # RTL Diag check
    rtl_check = MainBoard()
    rtl_check = force_sub_board_win(rtl_check, 0, 2, Player.OPPONENT)
    rtl_check = force_sub_board_win(rtl_check, 1, 1, Player.OPPONENT)
    rtl_check = force_sub_board_win(rtl_check, 2, 0, Player.OPPONENT)

    assert rtl_check.is_finished == True
    assert rtl_check.winner == Player.OPPONENT

    # Row check
    row_check = MainBoard()
    row_check = force_sub_board_win(row_check, 0, 0, Player.ME)
    row_check = force_sub_board_win(row_check, 1, 0, Player.ME)
    row_check = force_sub_board_win(row_check, 2, 0, Player.ME)

    assert row_check.is_finished == True
    assert row_check.winner == Player.ME

    # Col check
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
        main_board.add_my_move(MainBoardCoords(1, 1), SubBoardCoords(1, 1))


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
    string_board = str(MainBoard(3).add_my_move(MainBoardCoords(0, 0), SubBoardCoords(1, 1))
                       .add_opponent_move(MainBoardCoords(1, 1), SubBoardCoords(2, 2))
                       .add_opponent_move(MainBoardCoords(2, 2), SubBoardCoords(0, 0)))

    assert string_board == "0 0 0 | 0 0 0 | 0 0 0 \n" \
                           "0 1 0 | 0 0 0 | 0 0 0 \n" \
                           "0 0 0 | 0 0 0 | 0 0 0 \n" \
                           "- - - | - - - | - - - \n" \
                           "0 0 0 | 0 0 0 | 0 0 0 \n" \
                           "0 0 0 | 0 0 0 | 0 0 0 \n" \
                           "0 0 0 | 0 0 2 | 0 0 0 \n" \
                           "- - - | - - - | - - - \n" \
                           "0 0 0 | 0 0 0 | 2 0 0 \n" \
                           "0 0 0 | 0 0 0 | 0 0 0 \n" \
                           "0 0 0 | 0 0 0 | 0 0 0 \n"


def force_sub_board_win(main_board, board_row, board_col, player):
    return main_board.copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(0, 0), player) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(1, 1), player) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(2, 2), player)


def force_sub_board_tie(main_board, board_row, board_col):
    return main_board \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(0, 0), Player.ME) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(1, 1), Player.OPPONENT) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(2, 2), Player.ME) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(0, 2), Player.OPPONENT) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(2, 0), Player.ME) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(1, 0), Player.OPPONENT) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(1, 2), Player.ME) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(2, 1), Player.OPPONENT) \
        .copy_applying_move(MainBoardCoords(board_row, board_col), SubBoardCoords(0, 1), Player.ME)
