from __future__ import annotations
import math
import random
from abc import ABC, abstractmethod
from typing import Optional, Union, List
from enum import Enum
from random import randint
from coord import Coord


class CharacterDeath(Exception):

    def __init__(self, msg, char: Character):
        self.message = msg
        char.temp_health = 0


class InvalidAttack(Exception):
    pass


class Player(Enum):
    VILLAIN = 0
    HERO = 1


class Character(ABC):

    @abstractmethod
    def __init__(self, player: Player):
        self.__player = player
        self.__health = 5
        self.__temp_health = 5
        self.__attack = 3
        self.__defense = 3
        self.__move = 3
        self.__range = 1


    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, new_player: Player):
        if not isinstance(new_player, Player):
            raise TypeError
        self.__player = new_player

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, new_health):
        if not isinstance(new_health, int):
            raise TypeError
        if new_health <= 0:
            raise ValueError
        self.__health = new_health

    @property
    def temp_health(self):
        return self.__temp_health

    @temp_health.setter
    def temp_health(self, new_temp_health):
        if not isinstance(new_temp_health, int):
            raise TypeError
        self.__temp_health = new_temp_health
        if self.__temp_health == 0:
            print('something died at 0')
        if self.__temp_health < 0:
            raise CharacterDeath('something died', self)

    @property
    def combat(self):
        return [self.__attack, self.__defense]

    @combat.setter
    def combat(self, combat: list):
        if not isinstance(combat, list):
            raise TypeError
        if combat[0] < 0:
            raise ValueError
        if combat[1] < 0:
            raise ValueError
        self.__defense = combat[1]
        self.__attack = combat[0]

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, new_range):
        if not isinstance(new_range, int):
            raise TypeError
        if new_range <= 0:
            raise ValueError
        self.__range = new_range

    @property
    def move(self):
        return self.__move

    @move.setter
    def move(self, new_move):
        if not isinstance(new_move, int):
            raise TypeError
        if new_move <= 0:
            raise ValueError
        self.__move = new_move


    @abstractmethod
    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        if len(board) > 1 and isinstance(from_coord, Coord) and isinstance(to_coord, Coord):
            if 0 <= to_coord.x < len(board) and 0 <= to_coord.y < len(board[0]):
                if 0 <= from_coord.x < len(board) and 0 <= from_coord.y < len(board[0]):
                    if from_coord.x != to_coord.x or from_coord.y != to_coord.y:
                        if board[from_coord.x][from_coord.y] is self:
                            if board[to_coord.x][to_coord.y] is None:
                                return True
        return False

    @abstractmethod
    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        if len(board) > 1 and isinstance(from_coord, Coord) and isinstance(to_coord, Coord):
            if 0 <= to_coord.x < len(board) and 0 <= to_coord.y < len(board[0]):
                if 0 <= from_coord.x < len(board) and 0 <= from_coord.y < len(board[0]):
                    if from_coord.x != to_coord.x or from_coord.y != to_coord.y:
                        if board[from_coord.x][from_coord.y] == self:
                            if board[to_coord.x][to_coord.y] is not None:
                                # distance_from_to = ((to_coord.x - from_coord.x) ** 2 + (to_coord.y - from_coord.y) ** 2) ** (1/2)       #point distance formula, to determine range of attack
                                # distance_from_to = math.floor(distance_from_to)
                                # if distance_from_to <= self.range:
                                return True
        return False



    @abstractmethod
    def calculate_dice(self, attack= True, lst: list = [], *args, **kwargs) -> int:
        #attacking
        if attack:
            dmg_total = 0
            if len(lst) >= 1:
                for i in range(len(lst)):
                    if lst[i] > 4:
                        dmg_total += 1
                return dmg_total
            else:
                for _ in range(self.combat[0]):
                    roll = random.randint(1,6)
                    if roll > 4:
                        dmg_total += 1
                return dmg_total
        #defense
        else:
            def_total = 0
            if len(lst) >= 1:
                for i in range(len(lst)):
                    if lst[i] > 3:
                        def_total += 1
                return def_total
            else:
                for _ in range(self.combat[1]):
                    roll = random.randint(1,6)
                    if roll > 3:
                        def_total += 1
                return def_total

    @abstractmethod
    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        try:
            target.temp_health -= damage
            print(f'```\n{target.__class__.__name__} was dealt {damage} damage!\n```')
        except CharacterDeath as e:
            print(e)
            pass





