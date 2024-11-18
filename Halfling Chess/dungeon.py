from creatures import *
from character import *


class Dungeon:

    def __init__(self, height: int, width: int, villains: List[Villain] = None):
        if villains is None:
            villains = []
        if not isinstance(height, int):
            raise TypeError
        if not isinstance(width, int):
            raise TypeError
        if not isinstance(villains, list):
            raise TypeError
        for vil in villains:
            if not isinstance(vil, Villain):
                raise ValueError

        if not 4 <= height <= 12:
            raise ValueError
        self.__height = height
        if not 4 <= width <= 12:
            raise ValueError
        self.__width = width
        self.__board = []
        for x in range(self.__width):
            self.__board.append([])
        for y in range(self.__height):
            for _ in range(self.__height):
                self.__board[y].append(None)
        self.__villains = []
        self.__player = Player.HERO
        self.__heroes = [Warrior(), Mage(), Paladin(), Ranger()]
        if len(villains) < 1:
            self.generate_villains()
        else:
            nec_in_list = False
            for v in villains:
                if nec_in_list:
                    raise ValueError
                self.__villains.append(v)
                if isinstance(v, Necromancer):
                    nec_in_list = True

    # properties
    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, new_board: List[List]):
        if not isinstance(new_board, list):
            raise TypeError
        if not 4 <= len(new_board) <= 12:
            raise ValueError
        if not isinstance(new_board[0], list):
            raise ValueError
        if not 4 <= len(new_board[0]) <= 12:
            raise ValueError
        self.__board = new_board

    @property
    def player(self):
        return self.__player

    @property
    def heroes(self):
        return self.__heroes

    @heroes.setter
    def heroes(self, new_heroes):
        if not isinstance(new_heroes, list):
            raise TypeError
        if len(new_heroes) < 1:
            raise ValueError
        for hero in new_heroes:
            if not isinstance(hero, Hero):
                raise ValueError
        self.__heroes = new_heroes

    @property
    def villains(self):
        return self.__villains

    @villains.setter
    def villains(self, new_villains):
        if not isinstance(new_villains, list):
            raise TypeError
        if len(new_villains) < 1:
            raise ValueError
        for vil in new_villains:
            if not isinstance(vil, Villain):
                raise ValueError
        self.__villains = new_villains

    def generate_villains(self):
        self.__villains = []
        necromancer_on_board = False
        # random height or width number gen
        num_villains = random.randint(1, self.__width)
        if self.height > self.width:
            num_villains = random.randint(1, self.height)
        for _ in range(num_villains):
            random_villains_selector = random.randint(1, 10)
            if 1 <= random_villains_selector <= 5:
                self.__villains.append(Goblin())
            elif 6 <= random_villains_selector <= 8 or necromancer_on_board:
                self.__villains.append(Skeleton())
            else:
                self.__villains.append(Necromancer())
                necromancer_on_board = True

    def is_valid_move(self, coords: List[Coord]) -> bool:
        for coord in coords:
            if not 0 <= coord.x <= len(self.board) and not 0 <= coord.y <= len(self.board[0]):
                return False
            if not 0 <= coord.x <= len(self.board) and not 0 <= coord.y <= len(self.board[0]):
                return False
            if not self.board[coord.x][coord.y] == None:
                return False
        return True
        # (++QUESTION)

    def is_valid_attack(self, coords: List[Coord]) -> bool:
        from_coord = []
        for coord in coords:
            if not 0 <= coord.x <= len(self.board) and not 0 <= coord.y <= len(self.board[0]):
                return False
            if not 0 <= coord.x <= len(self.board) and not 0 <= coord.y <= len(self.board[0]):
                return False
            if self.board[coord.x][coord.y] == None:
                return False
            if from_coord == []:
                from_coord = coord
            else:
                if from_coord.x != coord.x or from_coord.y != coord.y:
                    if self.board[from_coord.x][from_coord.y] is not None:
                        if self.board[coord.x][coord.y] is not None:
                            distance_from_to = ((coord.x - from_coord.x) ** 2 + (coord.y - from_coord.y) ** 2) ** (1 / 2)  # point distance formula, to determine range of attack
                            distance_from_to = math.floor(distance_from_to)
                            char: Character = self.board[from_coord.x][from_coord.y]
                            if distance_from_to <= char.range:
                                return True
                            else:
                                return False
        return True
        # (++QUESTION) same thing here

    def character_at(self, x: int, y: int) -> Character:
        if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]):
            if self.board[x][y] is not None:
                char = self.board[x][y]
                return char.__class__.__name__
        # (++QUESTION) ensure range of the character is implemented?

    def move(self, from_coord: Coord, to_coord: Coord):
        place = None
        if self.board[from_coord.x][from_coord.y] != None:
            place: Character = self.board[from_coord.x][from_coord.y]
        if place:
            if place.is_valid_move(from_coord, to_coord, self.board):
                self.board[to_coord.x][to_coord.y] = self.board[from_coord.x][from_coord.y]
                self.board[from_coord.x][from_coord.y] = None

    def set_character_at(self, target: Character, x: int, y: int):
        if not isinstance(target, Character):
            raise TypeError
        if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]):
            if self.board[x][y] is None:
                self.board[x][y] = target

    def attack(self, from_coord: Coord, to_coord: Coord):
        if 0 <= to_coord.x <= len(self.board) and 0 <= to_coord.y <= len(self.board[0]):
            if 0 <= from_coord.x <= len(self.board) and 0 <= from_coord.y <= len(self.board[0]):
                if self.board[from_coord.x][from_coord.y] is not None:
                    char: Character = self.board[from_coord.x][from_coord.y]
                    if char.is_valid_attack(from_coord, to_coord, self.board):
                        target: Character = self.board[to_coord.x][to_coord.y]
                        dmg = char.calculate_dice(target=target)
                        if dmg > 0:
                            char.deal_damage(target, dmg)
                        else:
                            print(f'{target.__class__.__name__} to no damage from {char.__class__.__name__}')

                # char: Character = self.board[from_coord.x][from_coord.y]
                # attacked_char: Character = self.board[to_coord.x][to_coord.y]
                # if char != None and attacked_char != None:
                #     if char.is_valid_attack(from_coord, to_coord, self.board):
                #         char_attack_dmg = char.calculate_dice(target=attacked_char)     #attacking char attacking roll
                #         attacked_char_def = attacked_char.calculate_dice(False) #defeneding character defense roll
                #         total_dmg = char_attack_dmg - attacked_char_def
                #         if total_dmg > 0:
                #             attacked_char.temp_health -= total_dmg
                #         else:
                #             print(f'{attacked_char} to no damage from {char}')

    def set_next_player(self):
        if self.__player == Player.HERO:
            self.__player = Player.VILLAIN
        else:
            self.__player = Player.HERO

    def print_board(self):
        st = ' \t'
        st += '_____' * len(self.board)
        st += '\n'
        for i in range(len(self.board)):
            st += f'{i}\t'
            for j in range(len(self.board[i])):
                if self.board[i][j] is None:
                    st += '|___|'
                else:
                    st += f'|{self.board[i][j].__class__.__name__[:3]}|'
            st += '\n'
        st += '\t'
        for i in range(len(self.board[0])):
            st += f'  {i}  '
        print(st)

    def is_dungeon_clear(self) -> bool:
        for X in self.board:
            for spotY in X:
                if spotY == None:
                    continue
                if isinstance(spotY, Villain):
                    if spotY.temp_health > 0:
                        return False
                    continue
        return True

    def adventurer_defeat(self) -> bool:
        for X in self.board:
            for spotY in X:
                if spotY == None:
                    continue
                if isinstance(spotY, Hero):
                    if spotY.temp_health > 0:
                        return False
                    continue
        return True

    def place_heroes(self):
        middleX = len(self.board) // 2
        if not middleX % 1 > 0:
            middleX -= 1
        #(+QUESTION) board is not mapped out at x,y but instead y, len(board) - x
        # layout for x,y
        # self.board[middleX][1] = self.heroes[0]
        # self.board[middleX + 1][1] = self.heroes[1]
        # self.board[middleX][0] = self.heroes[2]
        # self.board[middleX + 1][0] = self.heroes[3]
        # layout for whatever monstrosity the board really is
        self.board[len(self.board) - 2][middleX] = self.heroes[0]
        self.board[len(self.board) - 1][middleX] = self.heroes[1]
        self.board[len(self.board) - 2][middleX + 1] = self.heroes[2]
        self.board[len(self.board) - 1][middleX + 1] = self.heroes[3]

    def place_villains(self):
        num_villains = len(self.__villains)
        i = 0
        while num_villains > 0:
            lb = len(self.board)
            lby = len(self.board[0])
            random_coordX = random.randint(0, len(self.board) - 1)
            random_coordY = random.randint(3, len(self.board[0]) - 1)
            if self.board[random_coordX][random_coordY] is None:
                self.board[random_coordX][random_coordY] = self.__villains[i]
                i += 1
                num_villains -= 1

    def generate_new_board(self, height: int = -1, width: int = -1):
        if height < 0:
            self.__height = random.randint(4, 12)
        if width < 0:
            self.__width = random.randint(4, 12)

        self.board = []

        for x in range(self.__width):
            self.board.append([])
        for y in range(self.__height):
            self.board[y].append(None)

        if self.__villains == []:
            self.generate_villains()
        self.place_villains()
        self.place_heroes()








