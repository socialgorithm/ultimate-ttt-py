#!/usr/bin/env python3

import sys
from players import Random


def main():
    line = sys.stdin.readline()
    while line:
        random_player.process_input(line.strip())
        line = sys.stdin.readline()


if __name__ == "__main__":
    random_player = Random()
    main()
