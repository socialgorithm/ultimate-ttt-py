from players import Random


def test_it_returns_a_valid_move_coordinates():
    assert_move_is_in_bounds(*Random().get_my_move())


def assert_move_is_in_bounds(main_board_coords, sub_board_coords):
    assert_coords_are_in_bounds(main_board_coords)
    assert_coords_are_in_bounds(sub_board_coords)


def assert_coords_are_in_bounds(board_coords):
    assert 0 <= board_coords.row <= 2
    assert 0 <= board_coords.col <= 2
