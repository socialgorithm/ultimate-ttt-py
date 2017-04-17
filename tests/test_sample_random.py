import pytest

import subprocess

def whenPlayerIsSentInitThenPlayerRespondsWithMove():
    p = subprocess.Popen(_args, shell = withShell,\
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    p.stdin.write('init')
    stdout, stderr = p.communicate()
    print(stdout)

def whenPlayerIsSentWaitingThenPlayerDoesNothing():
    assert False

def whenPlayerIsSentMoveRequestThenPlayerRespondsWithMove():
    assert False

def whenPlayerIsSentOpponentMoveThenPlayerRespondsWithValidMove():
    assert False
