#!/bin/bash

from abc import ABCMeta, abstractmethod

from engine import MainBoardCoords, SubBoardCoords
from engine.main_board import MainBoard


class UltimatePlayer(metaclass=ABCMeta):
    def __init__(self):
        self.board_size = 3
        self.main_board = MainBoard(self.board_size)

    @abstractmethod
    def onMove(self):
        pass
    
    @abstractmethod
    def onOpponent(self, board, move):
        pass

    @abstractmethod
    def gameOver(self, result, board, move):
        pass

    @abstractmethod
    def matchOver(self, result):
        pass
    
    @abstractmethod
    def timeout(self):
        pass

    @property
    def is_game_finished(self) -> bool:
        return self.main_board.is_finished

    def add_my_move(self, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords) -> None:
        self.main_board = self.main_board.add_my_move(main_board_coords, sub_board_coords)

    def add_opponent_move(self, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords) -> None:
        self.main_board = self.main_board.add_opponent_move(main_board_coords, sub_board_coords)
