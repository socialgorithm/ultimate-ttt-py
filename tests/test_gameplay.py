import pytest
import re

from ultimate_ttt import MainBoard, BoardCoords, Move, Player, PlayerMove, is_diagonal_won, is_col_won, is_row_won

def test_row_col_checks_work():
    main_board = MainBoard()

    for game_event in get_game_events('tests/logs/diag_fail.log'):
        main_board = main_board._add_move(game_event[0], game_event[1])

    assert is_diagonal_won(main_board._board[0][1]._board, PlayerMove(Player.OPPONENT, Move(1,1))) is True
    assert is_col_won(main_board._board[0][2]._board, PlayerMove(Player.ME, Move(0, 1))) is True
    assert is_row_won(main_board._board[2][1]._board, PlayerMove(Player.ME, Move(1, 1))) is True

def get_game_events(filename):
    log_file = open(filename, 'r')
    lines = log_file.readlines()
    log_file.close()

    game_events = []
    for line in lines:
        line = line.strip()

        player = Player.NONE

        if 'opponent' in line:
            player = Player.OPPONENT
        elif 'player' in line:
            player = Player.ME
        else:
            continue

        move_str = line[-7:]
        board_coords = BoardCoords(int(move_str[0]),int(move_str[2]))
        move_coords = Move(int(move_str[4]),int(move_str[6]))

        game_events.append((board_coords, PlayerMove(player, move_coords)))

    return game_events
