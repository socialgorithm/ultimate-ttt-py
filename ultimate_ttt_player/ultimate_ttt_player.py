from ultimate_ttt.main_board import MainBoard
from ultimate_ttt.gameplay import *

from abc import ABCMeta, abstractmethod
import sys
import logging
from datetime import datetime


class UltimateTTTPlayer(metaclass=ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger('ultimate_ttt_player')
        logging.basicConfig(filename=datetime.now().strftime('player_%H_%M_%d_%m_%Y.log'),
                            format='%(asctime)s %(message)s',
                            level=logging.DEBUG)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add_opponent_move(self, board, opponent_move):
        pass

    @abstractmethod
    def add_my_move(self, board, move):
        pass

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def get_my_move(self):
        pass

    @property
    @abstractmethod
    def player_name(self):
        pass

    @property
    @abstractmethod
    def is_current_match_finished(self):
        pass

    def process_input(self, line):
        self.logger.debug('ultimate_ttt_player: received input: [%s]' % line)
        if line == "init":
            self.logger.debug('ultimate_ttt_player: initializing...')
            self.initialize()
        elif line == "waiting":
            self.logger.debug('ultimate_ttt_player: waiting...')
            self.wait()
            return
        elif line == "move":
            self.logger.debug('ultimate_ttt_player: computing my move...')
            board_coords, move = self.get_my_move()
            self.add_my_move(board_coords, move)
            self.write_move((board_coords, move))
        elif line.startswith("opponent"):
            self.logger.debug('ultimate_ttt_player: received opponent move...')
            received_move = line.split(" ")[1]
            board_coords_str, opponent_move_str = received_move.split(";")
            board_coords = BoardCoords(*map(int, board_coords_str.split(",")))
            opponent_move = Move(*map(int, opponent_move_str.split(",")))
            self.add_opponent_move(board_coords, opponent_move)
            self.logger.debug('ultimate_ttt_player: processed opponent move...')

            if not self.is_current_match_finished:
                self.write_move(self.get_my_move())
        else:
            self.logger.error('ultimate_ttt_player: received bad input: [%s]' % line)

    def write_move(self, move):
        next_board_coords = move[0]
        next_move = move[1]
        move_str = "%d,%d;%d,%d" % (next_board_coords.row, next_board_coords.col, next_move.row, next_move.col)
        print(move_str)
        sys.stdout.flush()
        self.logger.debug('ultimate_ttt_player: successfully wrote move: ' + move_str)
