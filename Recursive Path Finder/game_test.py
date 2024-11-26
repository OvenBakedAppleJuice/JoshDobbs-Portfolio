import unittest
from llstack import *
from game import *


class MyTestCase(unittest.TestCase):
    def test_llstack_attributes(self):
        test_ll = LLStack()
        self.assertEqual(test_ll.size, 0)
        self.assertEqual(test_ll.__str__(), '')

    def test_llstack_push(self):
        test_ll = LLStack()
        self.assertEqual(test_ll.size, 0)
        self.assertEqual(test_ll.__str__(), '')
        # Push (1, 1)
        test_ll.push((1, 1))
        self.assertEqual(test_ll.size, 1)
        self.assertEqual(test_ll.__str__(), '(1, 1)')
        # Push (1, 0)
        test_ll.push((1, 0))
        self.assertEqual(test_ll.size, 2)
        self.assertEqual(test_ll.__str__(), '(1, 1) -> (1, 0)')

        # Test fails
        # Non tuple data
        with self.assertRaises(TypeError):
            test_ll.push(5)
        # Tuple with more than and less than 2 values
        with self.assertRaises(ValueError):
            test_ll.push((1, 1, 1))
        with self.assertRaises(ValueError):
            test_ll.push(tuple([2]))
        # Non-integers in tuple
        with self.assertRaises(TypeError):
            test_ll.push((1.5, 1.0))
        # Negative numbers in tuple
        with self.assertRaises(ValueError):
            test_ll.push((-1, 0))


    def test_ll_stack_pop(self):
        test_ll = LLStack()
        self.assertEqual(test_ll.size, 0)
        # Add some data
        test_ll.push((0, 1))
        test_ll.push((1, 1))
        test_ll.push((2, 1))
        # Pop
        p = test_ll.pop()
        self.assertEqual(test_ll.size, 2)
        self.assertEqual(test_ll.__str__(), '(0, 1) -> (1, 1)')
        # Check p (popped data)
        self.assertEqual((2, 1), p)

        # Test fails
        # Pop rest of data
        test_ll.pop()
        test_ll.pop()
        # self.__head is None
        with self.assertRaises(IndexError):
            test_ll.pop()

    # Testing Map class from game.py

    def setUp(self):
        # Uses sample grid from prarielearn
        self.sample_grid = [['ocean', 'grass', 'grass', 'grass'],
        ['grass', 'grass', 'grass', 'grass', 'grass'],
        ['grass', 'grass', 'grass', 'ocean', 'grass'],
        ['grass', 'ocean', 'grass', 'ocean', 'grass', 'grass'],
        ['ocean', 'grass', 'grass', 'grass', 'grass'],
        ['grass', 'grass', 'ocean', 'grass']]
        self.sample_map = Map(self.sample_grid, (1, 1), (3, 5))

        # Random no path map from path_gui
        self.r_no_path_grid = [['grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass'], ['grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'ocean'], ['ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'ocean', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'ocean', 'grass', 'grass'], ['ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass'], ['grass', 'ocean', 'grass', 'grass', 'grass']]
        self.random_no_path = Map(self.r_no_path_grid, (5, 10), (10, 8))

        # Random solvable map from path_gui
        self.r_grid = [['grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'ocean', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'ocean'], ['grass', 'ocean', 'grass', 'grass', 'ocean', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'grass'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'ocean', 'grass', 'ocean', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass']]
        self.random_map = Map(self.r_grid, (8, 2), (5, 10))

    def test_init_map(self):
        # Check instance variables
        # Sample
        self.assertEqual(self.sample_map.grid, self.sample_grid)
        self.assertEqual(self.sample_map.start_coords, (1, 1))
        self.assertEqual(self.sample_map.end_coords, (3, 5))
        # no path
        self.assertEqual(self.random_no_path.grid, self.r_no_path_grid)
        self.assertEqual(self.random_no_path.start_coords, (5, 10))
        self.assertEqual(self.random_no_path.end_coords, (10, 8))
        # Random path
        self.assertEqual(self.random_map.grid, self.r_grid)
        self.assertEqual(self.random_map.start_coords, (8, 2))
        self.assertEqual(self.random_map.end_coords, (5, 10))

        # Invalid Instance variables
        with self.assertRaises(TypeError):
            faulty_grid = Map(['grass', 'grass', 'grass'], (1, 1), (2, 2))
            faulty_start_coord = Map(self.sample_grid, (0, 0), (3, 5))
            faulty_end_coord = Map(self.sample_grid, (3, 5), (3, 3))
            invalid_coord_type = Map(self.sample_grid, 5, (3, 3))
            faulty_value_grid = Map([[1, 1, 1], [1, 0, 1]], (0, 0), (1, 0))

        with self.assertRaises(ValueError):
            non_grass_ocean = Map([['grass', 'ocean', 'grass'], ['invalid_name', 'grass', 'grass']], (0, 0), (3, 5))
            negative_num_coord = Map(self.sample_grid, (-1, 0), (3, 5))
            not_two_coord = Map(self.sample_grid, (1, 2, 3), (3, 5))

    def test_find_path(self):
        # Ensure result is llstack, then check stack

        # Sample
        result = self.sample_map.find_path()
        self.assertEqual(type(result), LLStack)
        self.assertEqual(str(result), '(1, 1) -> (2, 1) -> (2, 2) -> (3, 2) -> (4, 2) -> (4, 3) -> (5, 3) -> (4, 4) -> (3, 4) -> (3, 5)')
        # No path
        result = self.random_no_path.find_path()
        self.assertEqual(result, None)
        # Random path
        result = self.random_map.find_path()
        self.assertEqual(type(result), LLStack)
        self.assertEqual(str(result), '(8, 2) -> (9, 2) -> (10, 2) -> (11, 2) -> (12, 2) -> (12, 3) -> (12, 1) -> (11, 1) -> (10, 1) -> (10, 0) -> (11, 0) -> (12, 0) -> (9, 0) -> (8, 0) -> (8, 1) -> (7, 1) -> (7, 2) -> (7, 3) -> (8, 3) -> (9, 3) -> (10, 3) -> (10, 4) -> (11, 4) -> (10, 5) -> (10, 6) -> (10, 7) -> (11, 7) -> (10, 8) -> (10, 9) -> (10, 10) -> (11, 10) -> (11, 11) -> (11, 12) -> (11, 13) -> (11, 14) -> (11, 15) -> (10, 15) -> (10, 14) -> (10, 13) -> (10, 11) -> (9, 10) -> (8, 10) -> (8, 11) -> (8, 12) -> (7, 11) -> (7, 10) -> (8, 9) -> (9, 9) -> (9, 8) -> (8, 8) -> (7, 8) -> (6, 8) -> (6, 7) -> (7, 7) -> (8, 7) -> (8, 6) -> (9, 6) -> (9, 5) -> (8, 5) -> (7, 5) -> (7, 6) -> (6, 6) -> (5, 6) -> (5, 7) -> (4, 7) -> (4, 8) -> (4, 9) -> (5, 9) -> (5, 10)')

        # Edge cases
        # Start Coord and End Coord on corners
        test_grid = [['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass'], ['grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'ocean', 'grass'], ['ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'ocean', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass']]
        corner_map = Map(test_grid, (0, 0), (12, 16))
        self.assertEqual(type(corner_map.find_path()), LLStack)
        self.assertEqual(str(corner_map.find_path()), '(0, 0) -> (1, 0) -> (2, 0) -> (3, 0) -> (4, 0) -> (5, 0) -> (6, 0) -> (7, 0) -> (8, 0) -> (9, 0) -> (9, 1) -> (10, 1) -> (11, 1) -> (12, 1) -> (12, 2) -> (12, 3) -> (12, 4) -> (12, 5) -> (12, 6) -> (12, 7) -> (12, 8) -> (12, 9) -> (12, 10) -> (12, 11) -> (12, 12) -> (12, 13) -> (12, 14) -> (12, 15) -> (12, 16)')

        # Worst Case, goes through all grass before hitting end_location
        worst_grid = [['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean'], ['ocean', 'ocean', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass']]
        worst_map = Map(worst_grid, (12, 7), (0, 0))
        self.assertEqual(type(worst_map.find_path()), LLStack)
        self.assertEqual(str(worst_map.find_path()), '(12, 7) -> (12, 8) -> (12, 9) -> (12, 10) -> (12, 11) -> (12, 12) -> (12, 13) -> (12, 14) -> (12, 15) -> (12, 16) -> (12, 17) -> (12, 18) -> (11, 8) -> (10, 8) -> (10, 9) -> (10, 10) -> (10, 11) -> (10, 12) -> (10, 7) -> (11, 7) -> (9, 7) -> (10, 6) -> (10, 5) -> (11, 5) -> (12, 5) -> (12, 4) -> (11, 4) -> (10, 4) -> (9, 4) -> (9, 5) -> (8, 5) -> (8, 6) -> (7, 6) -> (7, 7) -> (7, 8) -> (7, 9) -> (7, 10) -> (7, 11) -> (6, 6) -> (5, 6) -> (5, 7) -> (4, 7) -> (4, 8) -> (4, 9) -> (4, 10) -> (4, 11) -> (3, 11) -> (3, 12) -> (3, 13) -> (3, 14) -> (3, 15) -> (3, 16) -> (3, 10) -> (3, 9) -> (3, 7) -> (3, 6) -> (4, 6) -> (4, 5) -> (3, 5) -> (2, 5) -> (1, 5) -> (1, 6) -> (1, 7) -> (1, 8) -> (1, 9) -> (1, 10) -> (1, 11) -> (1, 12) -> (1, 13) -> (1, 14) -> (1, 15) -> (1, 16) -> (1, 17) -> (1, 18) -> (1, 19) -> (0, 7) -> (0, 6) -> (0, 5) -> (0, 4) -> (0, 3) -> (1, 3) -> (2, 3) -> (2, 4) -> (3, 4) -> (4, 4) -> (5, 4) -> (6, 4) -> (7, 4) -> (8, 4) -> (8, 3) -> (9, 3) -> (10, 3) -> (11, 3) -> (12, 3) -> (11, 2) -> (10, 2) -> (9, 2) -> (9, 1) -> (10, 1) -> (11, 1) -> (12, 1) -> (12, 0) -> (11, 0) -> (10, 0) -> (9, 0) -> (8, 0) -> (8, 1) -> (7, 1) -> (7, 2) -> (7, 3) -> (6, 3) -> (5, 3) -> (4, 3) -> (4, 2) -> (5, 2) -> (6, 2) -> (6, 1) -> (6, 0) -> (7, 0) -> (5, 0) -> (4, 0) -> (4, 1) -> (3, 1) -> (3, 2) -> (2, 1) -> (2, 0) -> (3, 0) -> (6, 5) -> (1, 2) -> (0, 2) -> (0, 1) -> (0, 0)')

    def test_shortest_path(self):
        # Ensure result is llstack, then check stack
        # Sample
        result = self.sample_map.find_shortest_path()
        self.assertEqual(type(result), LLStack)
        self.assertEqual(str(result), '(1, 1) -> (1, 2) -> (1, 3) -> (1, 4) -> (2, 4) -> (3, 4) -> (3, 5)')
        # No path
        result = self.random_no_path.find_shortest_path()
        self.assertEqual(result, None)
        # Random path
        result = self.random_map.find_shortest_path()
        self.assertEqual(type(result), LLStack)
        self.assertEqual(str(result), '(8, 2) -> (7, 2) -> (6, 2) -> (5, 2) -> (5, 3) -> (5, 4) -> (5, 5) -> (4, 5) -> (4, 6) -> (4, 7) -> (4, 8) -> (4, 9) -> (4, 10) -> (5, 10)')

        # Edge cases
        # Start Coord and End Coord on corners
        test_grid = [
            ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
            ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
            ['grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean', 'ocean', 'grass',
             'grass', 'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass'],
            ['grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'ocean',
             'grass', 'ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
            ['grass', 'grass', 'grass', 'grass', 'grass'],
            ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass',
             'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
            ['grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'ocean', 'grass'],
            ['ocean', 'grass', 'grass', 'grass', 'ocean', 'grass', 'ocean', 'ocean', 'ocean', 'grass', 'grass', 'grass',
             'ocean', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass'],
            ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass',
             'grass', 'grass', 'grass', 'grass', 'grass']]
        corner_map = Map(test_grid, (0, 0), (12, 7))
        self.assertEqual(type(corner_map.find_shortest_path()), LLStack)
        self.assertEqual(str(corner_map.find_shortest_path()), '(0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2) -> (3, 2) -> (4, 2) -> (5, 2) -> (6, 2) -> (7, 2) -> (8, 2) -> (9, 2) -> (10, 2) -> (10, 3) -> (11, 3) -> (12, 3) -> (12, 4) -> (12, 5) -> (12, 6) -> (12, 7)')

        # Worst Case, has to track all possible spots before hitting the last possible location to go to
        worst_grid = [['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass']]
        worst_map = Map(worst_grid, (0, 0), (12, 18))
        self.assertEqual(type(worst_map.find_shortest_path()), LLStack)
        self.assertEqual(str(worst_map.find_shortest_path()), '(0, 0) -> (0, 1) -> (0, 2) -> (0, 3) -> (0, 4) -> (0, 5) -> (0, 6) -> (1, 6) -> (2, 6) -> (3, 6) -> (4, 6) -> (5, 6) -> (6, 6) -> (7, 6) -> (8, 6) -> (9, 6) -> (9, 7) -> (9, 8) -> (10, 8) -> (11, 8) -> (12, 8) -> (12, 9) -> (12, 10) -> (12, 11) -> (12, 12) -> (12, 13) -> (12, 14) -> (12, 15) -> (12, 16) -> (12, 17) -> (12, 18)')

    def test_minimum_len_path_helper(self):
        # helper function for find_shortest path, returns key
        # Make sure last (x, y) of value is the key
        test_dict = {(3, 2): [(1, 1), (2, 1), (2, 2), (3, 2)], (2, 1): [(1, 0), (1, 1), (2, 1)], (2, 2): [(3, 3), (2, 3), (2, 2)]}
        # looks for smallest len value, does not replace min if same size | uses self.random map need for a self, function does not use self
        self.assertEqual(Map.get_minimum_len_path(self.random_map, list(test_dict.values())), (2, 1))

    def test_enclosed_start(self):
        # Tests a tight starting coord
        enclosed_grid = [['ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['ocean', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'ocean'], ['grass', 'grass', 'grass', 'ocean', 'ocean', 'grass', 'grass', 'grass', 'grass', 'ocean', 'ocean', 'grass', 'grass', 'ocean', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass']]
        enclosed_start_map = Map(enclosed_grid, (1, 12), (5, 11))
        self.assertEqual(type(enclosed_start_map.find_path()), LLStack)
        self.assertEqual(str(enclosed_start_map.find_path()), '(1, 12) -> (1, 13) -> (1, 14) -> (1, 15) -> (1, 16) -> (1, 17) -> (1, 11) -> (1, 10) -> (1, 9) -> (1, 8) -> (2, 8) -> (2, 7) -> (2, 6) -> (1, 6) -> (0, 6) -> (0, 7) -> (0, 5) -> (1, 5) -> (2, 5) -> (2, 4) -> (1, 4) -> (0, 4) -> (0, 3) -> (1, 3) -> (2, 3) -> (3, 3) -> (4, 3) -> (4, 4) -> (4, 5) -> (5, 5) -> (5, 6) -> (5, 7) -> (5, 8) -> (4, 8) -> (4, 9) -> (4, 10) -> (4, 11) -> (5, 11)')

if __name__ == '__main__':
    unittest.main()
