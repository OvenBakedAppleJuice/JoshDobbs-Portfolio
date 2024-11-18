from character import *
import math


class Villain(Character):

    def __init__(self):
        super().__init__(Player.VILLAIN)

    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        return super().is_valid_attack(from_coord, to_coord, board)

    def calculate_dice(self, attack= True, lst: list = [], *args, **kwargs) -> int:
        return super().calculate_dice(attack, lst, *args, **kwargs)

    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        return super().deal_damage(target, damage, *args, **kwargs)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        valid_X_moves = []
        valid_Y_moves = []
        for addx in range(-self.move, self.move + 1):
            if addx == 0:
                continue
            altered_from_coord = Coord(from_coord.x + addx, from_coord.y)
            if super().is_valid_move(from_coord, altered_from_coord, board):
                valid_X_moves.append(altered_from_coord)
            else:
                if addx > 0:
                    break
                if addx < 0:
                    valid_X_moves = []
        for addy in range(-self.move, self.move + 1):
            if addy == 0:
                continue
            altered_from_coord = Coord(from_coord.x, from_coord.y + addy)
            if super().is_valid_move(from_coord, altered_from_coord, board):
                valid_Y_moves.append(altered_from_coord)
            else:
                if addy > 0:
                    break
                if addy < 0:
                    valid_Y_moves = []
        for valid_move in valid_X_moves:
            if valid_move.x == to_coord.x and valid_move.y == to_coord.y:
                return True
        for valid_move in valid_Y_moves:
            if valid_move.x == to_coord.x and valid_move.y == to_coord.y:
                return True
        return False


class Goblin(Villain):

    def __init__(self):
        super().__init__()
        self.health = 3
        self.temp_health = 3
        self.combat = [2, 2]

class Skeleton(Villain):

    def __init__(self):
        super().__init__()
        self.health = 2
        self.temp_health = 2
        self.combat = [2, 1]
        self.move = 2

class Necromancer(Villain):

    def __init__(self):
        super().__init__()
        self.combat = [1, 2]
        self.range = 3

    def raise_dead(self, target: Character, from_coords: Coord, to_coords: Coord, board: List[List[Union[None, Character]]]):
        if Character.is_valid_attack(self, from_coords, to_coords, board):
            distance_from_to = ((to_coords.x - from_coords.x) ** 2 + (to_coords.y - from_coords.y) ** 2) ** (1/2)       #point distance formula, to determine range
            distance_from_to = math.floor(distance_from_to)
            if distance_from_to <= self.range:
                if target.temp_health <= 0:
                    if not isinstance(target, Villain):
                        target.player = Player.VILLAIN
                        target.temp_health = target.health // 2
                    else:
                        target.temp_health = target.health // 2

class Hero(Character):

    def __init__(self):
        super().__init__(Player.HERO)

    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        return super().is_valid_attack(from_coord, to_coord, board)

    def calculate_dice(self, attack= True, lst: list = [], *args, **kwargs) -> int:
        return super().calculate_dice(attack, lst, *args, **kwargs)

    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        return super().deal_damage(target, damage, *args, **kwargs)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        distance_from_to = ((to_coord.x - from_coord.x) ** 2 + (to_coord.y - from_coord.y) ** 2) ** (1 / 2)  # point distance formula, to determine range of attack
        distance_from_to = math.floor(distance_from_to)
        if distance_from_to <= self.move:
            return super().is_valid_move(from_coord, to_coord, board)
        else:
            return False

class Warrior(Hero):

    def __init__(self):
        super().__init__()
        self.health = 7
        self.temp_health = 7
        self.combat = [2, 4]

    def calculate_dice(self, target: Character, attack= True, lst: list = [], gob: list = None) -> int:
        #Goblin adds 2 rolls
        gob_dmg = 0
        if attack:
            if isinstance(target, Goblin):
                if gob is not None:
                    for i in range(len(gob)):
                        if gob[i] > 4:
                            gob_dmg += 1
                else:
                    for _ in range(2):
                        roll = random.randint(1,6)
                        if roll > 4:
                            gob_dmg += 1

        return super().calculate_dice(attack=attack, lst=lst) + gob_dmg




class Mage(Hero):

    def __init__(self):
        super().__init__()
        self.combat = [2, 2]
        self.range = 3
        self.move = 2

    def deal_damage(self, target: Character, damage: int) -> None:
        damage += 1     #all mages +1
        try:
            target.temp_health -= damage
            print(f'```\n{target.__class__.__name__} was dealt {damage} damage!\n```')
        except CharacterDeath as e:
            print(e)
            pass

class Paladin(Hero):

    def __init__(self, heal: bool = True):
        super().__init__()
        self.__heal = True
        self.health = 6
        self.temp_health = 6

    @property
    def heal(self):
        return self.__heal

    @heal.setter
    def heal(self, new_bool: bool):
        if not isinstance(new_bool, bool):
            raise TypeError
        self.__heal = bool

    def revive(self, target: 'Character', from_coord: Coord, to_coord: Coord, board: List[List[Union[None, 'Character']]]):
        if super().is_valid_attack(from_coord, to_coord, board):
            if isinstance(board[to_coord.x][to_coord.y], Hero):
                if self.heal:
                    distance_from_to = ((to_coord.x - from_coord.x) ** 2 + (to_coord.y - from_coord.y) ** 2) ** (1 / 2)  # point distance formula, to determine range
                    distance_from_to = math.floor(distance_from_to)
                    if distance_from_to <= self.range:
                        target.temp_health = target.health // 2
                        self.__heal = False

class Ranger(Hero):

    def __init__(self):
        super().__init__()
        self.range = 3

    def deal_damage(self, target: Character, damage: int) -> None:
        if isinstance(target, Skeleton):
            damage -= 1
        if damage < 0:
            self.temp_health = 0
        else:
            try:
                target.temp_health -= damage
                print(f'```\n{target.__class__.__name__} was dealt {damage} damage!\n```')
            except CharacterDeath as e:
                print(e)
                pass



