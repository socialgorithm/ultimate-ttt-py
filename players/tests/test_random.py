import pytest

import subprocess
import os
import re


def init_random_player():
    dir_path = os.path.dirname(os.path.dirname(__file__))
    player_path = os.path.join(dir_path, "random.py")
    _args = ("python " + player_path).split(" ")
    return subprocess.Popen(args=_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def test_whenPlayerIsSentMoveKeywordThenPlayerRespondsWithMove():
    random_player = init_random_player()
    player_response = random_player.communicate(b'move' + os.linesep.encode())[0].decode().strip()
    _assertValidMove(player_response)


def test_whenPlayerIsSentWaitingThenPlayerDoesNothing():
    random_player = init_random_player()
    player_response = random_player.communicate(b'init' + os.linesep.encode() + b'waiting' + os.linesep.encode())[
        0].decode().strip()
    assert (player_response == '')


def test_whenPlayerIsSentOpponentMoveThenPlayerRespondsWithValidMove():
    random_player = init_random_player()
    player_response = \
    random_player.communicate(b'init' + os.linesep.encode() + b'opponent 0,0;1,2' + os.linesep.encode())[
        0].decode().strip()
    _assertValidMove(player_response)


def _assertValidMove(move):
    move_pattern = re.compile(r'^\d,\d;\d,\d')
    assert (move_pattern.match(move).group() == move)
