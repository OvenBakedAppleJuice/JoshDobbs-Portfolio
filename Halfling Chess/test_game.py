import unittest
from dungeon import *
from creatures import *
from character import *
import random


class TestAll(unittest.TestCase):

    def test_dungeon_initialization(self):
        # Test with valid height, width, and villains
        villains = [Goblin(), Skeleton()]
        dungeon = Dungeon(height=6, width=6, villains=villains)
        self.assertEqual(dungeon.height, 6)
        self.assertEqual(dungeon.width, 6)
        self.assertEqual(len(dungeon.villains), 2)

        # Test with minimum and maximum values for height and width
        with self.assertRaises(ValueError):
            Dungeon(3, 4)  # height below minimum
        with self.assertRaises(ValueError):
            Dungeon(4, 13)  # width above maximum

    def test_board_property(self):
        dungeon = Dungeon(6, 6)
        new_board = [[None] * 6 for _ in range(6)]

        # Set and get board property
        dungeon.board = new_board
        self.assertEqual(dungeon.board, new_board)

        # Test with invalid board dimensions
        with self.assertRaises(ValueError):
            dungeon.board = [[None] * 13 for _ in range(6)]

    def test_heroes_property(self):
        dungeon = Dungeon(6, 6)

        # Valid heroes list
        new_heroes = [Warrior(), Mage()]
        dungeon.heroes = new_heroes
        self.assertEqual(dungeon.heroes, new_heroes)

        # Invalid heroes list (not all instances of Hero)
        with self.assertRaises(ValueError):
            dungeon.heroes = [Warrior(), Goblin()]

    def test_villains_property(self):
        dungeon = Dungeon(6, 6)

        # Valid villains list
        new_villains = [Goblin(), Skeleton()]
        dungeon.villains = new_villains
        self.assertEqual(dungeon.villains, new_villains)

        # Invalid villains list (not all instances of Villain)
        with self.assertRaises(ValueError):
            dungeon.villains = [Goblin(), Warrior()]

    def test_generate_villains(self):
        dungeon = Dungeon(6, 6, villains=[])
        dungeon.generate_villains()
        self.assertTrue(len(dungeon.villains) > 0)  # Villains generated
        for v in dungeon.villains:
            r = isinstance(v, Villain)
            self.assertEqual(True, r)  # Ensures each villain is Villain

    def test_is_valid_move(self):
        dungeon = Dungeon(6, 6)

        # Valid and invalid coordinates for movement
        valid_coords = [Coord(0, 0), Coord(1, 1)]
        self.assertTrue(dungeon.is_valid_move(valid_coords))

        invalid_coords = [Coord(7, 0), Coord(0, 6)]
        with self.assertRaises(IndexError):
            dungeon.is_valid_move(invalid_coords)

    def test_is_valid_attack(self):
        dungeon = Dungeon(6, 6)
        attacker = Warrior()
        target = Goblin()
        out_of_range_target = Goblin()

        # Set characters on board
        dungeon.set_character_at(attacker, 0, 0)
        dungeon.set_character_at(target, 1, 1)
        dungeon.set_character_at(out_of_range_target, 5, 5)

        # Valid attack range for Warrior
        self.assertTrue(dungeon.is_valid_attack([Coord(0, 0), Coord(1, 1)]))

        # Invalid attack range for Warrior
        self.assertFalse(dungeon.is_valid_attack([Coord(0, 0), Coord(5, 5)]))

    def test_character_at(self):
        dungeon = Dungeon(6, 6)
        warrior = Warrior()
        dungeon.set_character_at(warrior, 2, 2)
        self.assertEqual(dungeon.character_at(2, 2), "Warrior")
        self.assertIsNone(dungeon.character_at(0, 0))  # Empty cell returns nothing (None)

    def test_move_character(self):
        dungeon = Dungeon(6, 6)
        warrior = Warrior()
        dungeon.set_character_at(warrior, 0, 0)

        # Valid move
        dungeon.move(Coord(0, 0), Coord(1, 1))
        self.assertEqual(dungeon.character_at(1, 1), "Warrior")
        self.assertIsNone(dungeon.character_at(0, 0))

        # Invalid move
        dungeon.move(Coord(1,1), Coord(0,0))  # Moves Warrior back to 0,0
        dungeon.move(Coord(0, 0), Coord(4, 4))
        self.assertEqual(dungeon.character_at(0, 0), "Warrior")

    def test_attack(self):
        dungeon = Dungeon(6, 6)
        attacker = Warrior()
        target = Goblin()
        dungeon.set_character_at(attacker, 0, 0)
        dungeon.set_character_at(target, 1, 1)

        # Attack target within range
        initial_health = target.temp_health
        dungeon.attack(Coord(0, 0), Coord(1, 1))
        self.assertLessEqual(target.temp_health, initial_health)

    def test_set_next_player(self):
        dungeon = Dungeon(6, 6)

        # Toggle player
        self.assertEqual(dungeon.player, Player.HERO)
        dungeon.set_next_player()
        self.assertEqual(dungeon.player, Player.VILLAIN)
        dungeon.set_next_player()
        self.assertEqual(dungeon.player, Player.HERO)

    def test_is_dungeon_clear(self):
        dungeon = Dungeon(6, 6, villains=[Goblin(), Skeleton()])
        dungeon.place_villains()
        for v in dungeon.villains:  # Sets all villains health to 0
            v.temp_health = 0

        self.assertTrue(dungeon.is_dungeon_clear())  # All villains defeated

    def test_adventurer_defeat(self):
        dungeon = Dungeon(6, 6)
        dungeon.place_heroes()
        for v in dungeon.heroes:  # Sets all heroes health to 0
            v.temp_health = 0

        self.assertTrue(dungeon.adventurer_defeat())  # All heroes defeated

    def test_place_heroes_and_villains(self):
        dungeon = Dungeon(6, 6)
        dungeon.place_heroes()
        dungeon.place_villains()
        num_heroes = sum(1 for row in dungeon.board for cell in row if isinstance(cell, Hero))
        num_villains = sum(1 for row in dungeon.board for cell in row if isinstance(cell, Villain))
        self.assertEqual(num_heroes, len(dungeon.heroes))
        self.assertEqual(num_villains, len(dungeon.villains))

    def setUp(self):
        self.hero = Hero()
        self.villain = Villain()
        self.goblin = Goblin()
        self.skeleton = Skeleton()
        self.necromancer = Necromancer()
        self.hero = Hero()
        self.warrior = Warrior()
        self.mage = Mage()
        self.paladin = Paladin()
        self.ranger = Ranger()
        self.board = [[None] * 5 for _ in range(5)]
        self.board[0][0] = self.goblin

    def test_player_property(self):
        self.assertEqual(self.hero.player, Player.HERO)
        self.hero.player = Player.VILLAIN
        self.assertEqual(self.hero.player, Player.VILLAIN)
        with self.assertRaises(TypeError):
            self.hero.player = "NotAPlayer"

    def test_health_property(self):
        self.assertEqual(self.hero.health, 5)
        self.hero.health = 10
        self.assertEqual(self.hero.health, 10)
        with self.assertRaises(TypeError):
            self.hero.health = "NotAnInt"
        with self.assertRaises(ValueError):
            self.hero.health = -5

    def test_temp_health_property(self):
        self.assertEqual(self.hero.temp_health, 5)
        self.hero.temp_health = 3
        self.assertEqual(self.hero.temp_health, 3)
        with self.assertRaises(TypeError):
            self.hero.temp_health = "NotAnInt"
        with self.assertRaises(CharacterDeath):
            self.hero.temp_health = -1

    def test_combat_property(self):
        self.assertEqual(self.hero.combat, [3, 3])
        self.hero.combat = [5, 2]
        self.assertEqual(self.hero.combat, [5, 2])
        with self.assertRaises(TypeError):
            self.hero.combat = "NotAList"
        with self.assertRaises(ValueError):
            self.hero.combat = [-1, 2]
        with self.assertRaises(ValueError):
            self.hero.combat = [2, -1]

    def test_range_property(self):
        self.assertEqual(self.hero.range, 1)
        self.hero.range = 3
        self.assertEqual(self.hero.range, 3)
        with self.assertRaises(TypeError):
            self.hero.range = "NotAnInt"
        with self.assertRaises(ValueError):
            self.hero.range = -3

    def test_move_property(self):
        self.assertEqual(self.hero.move, 3)
        self.hero.move = 4
        self.assertEqual(self.hero.move, 4)
        with self.assertRaises(TypeError):
            self.hero.move = "NotAnInt"
        with self.assertRaises(ValueError):
            self.hero.move = -4

    def char_test_is_valid_move(self):
        board = [[None] * 5 for _ in range(5)]
        from_coord = Coord(0, 0)
        to_coord = Coord(0, 1)
        board[0][0] = self.hero
        self.assertTrue(self.hero.is_valid_move(from_coord, to_coord, board))
        board[0][1] = self.villain
        self.assertFalse(self.hero.is_valid_move(from_coord, to_coord, board))

    def char_test_is_valid_attack(self):
        board = [[None] * 5 for _ in range(5)]
        from_coord = Coord(0, 0)
        to_coord = Coord(0, 1)
        board[0][0] = self.hero
        board[0][1] = self.villain
        self.assertTrue(self.hero.is_valid_attack(from_coord, to_coord, board))
        board[0][1] = None
        self.assertFalse(self.hero.is_valid_attack(from_coord, to_coord, board))

    def test_calculate_dice_attack(self):
        damage = self.hero.calculate_dice(attack=True, lst=[5, 6, 1, 2])
        self.assertEqual(damage, 2)

    def test_calculate_dice_defense(self):
        defense = self.hero.calculate_dice(attack=False, lst=[4, 5, 1, 3])
        self.assertEqual(defense, 2)

    def test_deal_damage(self):
        # Strange testing, was told when temp_health == 0 don't raise the exception
        self.hero.deal_damage(self.villain, 6)
        self.assertEqual(self.villain.temp_health, 0)

    def test_villain_initialization(self):
        self.assertEqual(self.goblin.health, 3)
        self.assertEqual(self.skeleton.health, 2)
        self.assertEqual(self.necromancer.combat, [1, 2])
        self.assertEqual(self.necromancer.range, 3)

    def creatures_test_is_valid_attack(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(0, 1)
        self.board[0][1] = self.hero
        self.assertTrue(self.goblin.is_valid_attack(from_coord, to_coord, self.board))

    def creatures_test_calculate_dice_attack(self):
        damage = self.goblin.calculate_dice(attack=True, lst=[5, 6, 2])
        self.assertEqual(damage, 2)
        damage = self.skeleton.calculate_dice(attack=True)
        self.assertTrue(0 <= damage <= 2)

    def creatures_test_calculate_dice_defense(self):
        defense = self.skeleton.calculate_dice(attack=False, lst=[4, 5, 1, 3])
        self.assertEqual(defense, 2)

    def creatures_test_deal_damage_to_character(self):
        initial_health = self.hero.temp_health
        self.goblin.deal_damage(self.hero, 2)
        self.assertEqual(self.hero.temp_health, initial_health - 2)

    def test_move_validation(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(0, 1)
        self.board[0][1] = None
        self.assertTrue(self.goblin.is_valid_move(from_coord, to_coord, self.board))
        self.board[0][1] = self.hero
        self.assertFalse(self.goblin.is_valid_move(from_coord, to_coord, self.board))

    def test_necromancer_raise_dead(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(1, 1)
        self.board[0][0] = self.necromancer
        self.board[1][1] = self.hero
        self.hero.temp_health = 0
        self.necromancer.raise_dead(self.hero, from_coord, to_coord, self.board)
        self.assertEqual(self.hero.player, Player.VILLAIN)
        self.assertEqual(self.hero.temp_health, self.hero.health // 2)

    def test_paladin_revive(self):
        self.board[2][2] = self.paladin
        self.board[3][3] = self.mage
        self.mage.temp_health = 0
        from_coord = Coord(2, 2)
        to_coord = Coord(3, 3)
        self.paladin.revive(self.mage, from_coord, to_coord, self.board)
        self.assertEqual(self.mage.temp_health, self.mage.health // 2)
        self.assertFalse(self.paladin.heal)

    def test_mage_deal_damage(self):
        self.mage.deal_damage(self.skeleton, 2)
        self.assertEqual(self.skeleton.temp_health, 0)  # +1 for all damage

    def test_ranger_deal_damage(self):
        self.ranger.deal_damage(self.skeleton, 3)
        self.assertEqual(self.skeleton.temp_health, 0)  # -1 for Skeleton adjustment










