#!/usr/bin/env python3

import sys
from players import Random, Defensive, FirstAvailable


def main():
    line = sys.stdin.readline()
    while line:
        player.process_input(line.strip())
        line = sys.stdin.readline()


if __name__ == "__main__":
    if 2>len(sys.argv):
        player = Random()
    else:
        name=sys.argv[1]
        if name == 'Random':
            player = Random()
        elif name == 'FirstAvailable':
            player = FirstAvailable()
        elif name == 'Defensive':
            player = Defensive()
        else:
            raise Exception('unknown player')
    main()
