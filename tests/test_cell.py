import pytest
from ultimate_ttt import Cell, Player

def test_whenCellIsNewThenCellIsPlayedByNone():
    assert Cell().played_by == Player.NONE

def test_whenCellIsPlayedByMeThenPlayedByIsMe():
    assert Cell(Player.ME).played_by == Player.ME

def test_whenCellIsPlayedByOpponentThenPlayedByIsOpponent():
    assert Cell(Player.OPPONENT).played_by == Player.OPPONENT
