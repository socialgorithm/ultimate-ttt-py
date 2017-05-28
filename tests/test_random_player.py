import pytest

import subprocess
import os
import re

player_name = "random"

def init_random_player():
    samples_path = os.path.realpath(os.path.join(os.path.abspath(__file__), '../../samples'))
    player_path = os.path.join(samples_path, player_name + "_player.py")
    _args = ("python3 " + player_path).split(" ")
    return subprocess.Popen(args=_args,\
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def test_whenPlayerIsSentInitAndMoveThenPlayerRespondsWithMove():
    random_player = init_random_player()
    player_response = random_player.communicate(b'init\nmove\n')[0].decode().strip()
    _assertValidMove(player_response)

def test_whenPlayerIsSentWaitingThenPlayerDoesNothing():
    random_player = init_random_player()
    player_response = random_player.communicate(b'init\nwaiting\n')[0].decode().strip()
    assert(player_response == '')

def test_whenPlayerIsSentOpponentMoveThenPlayerRespondsWithValidMove():
    random_player = init_random_player()
    player_response = random_player.communicate(b'init\nopponent 0,0;1,2\n')[0].decode().strip()
    _assertValidMove(player_response)

def _assertValidMove(move):
    move_pattern = re.compile(r'^\d,\d;\d,\d')
    assert(move_pattern.match(move).group() == move)
