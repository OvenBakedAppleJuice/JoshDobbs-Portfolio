from llstack import LLStack
import time

class InvalidCoordinateError(Exception):
  pass

class OutOfBoundaries(Exception):
  pass

class Map:

    def __init__(self, grid: [[str]], start_loc: tuple, end_loc: tuple):
        # Checks for correct variable type of grid
        if not isinstance(grid, list):
            raise TypeError
        for l in grid:
            if not isinstance(l, list):
                raise TypeError
            for i in l:
                if not isinstance(i, str):
                    raise TypeError
                if i is not 'ocean' and i is not 'grass':
                    raise ValueError
        self.__grid = grid
        # Sets start and end with proper checks
        self.start_coords = start_loc
        self.end_coords = end_loc



    @property
    def start_coords(self):
        return self.__start

    @start_coords.setter
    def start_coords(self, new_start: tuple):
        if not isinstance(new_start, tuple):
            raise TypeError
        n = 0
        for i in new_start:
            n += 1
            if not isinstance(i, int):
                raise TypeError
            if i < 0:
                raise ValueError
        # n is number of values in tuple
        if n != 2:
            raise ValueError
        # Checks to see if ocean is on new_start and if it is a valid location on grid
        try:
            if self.grid[new_start[0]][new_start[1]] is 'ocean':
                raise InvalidCoordinateError
        except IndexError:
            raise OutOfBoundaries
        self.__start = new_start


    @property
    def end_coords(self):
        return self.__end

    @end_coords.setter
    def end_coords(self, new_end):
        if not isinstance(new_end, tuple):
            raise TypeError
        n = 0
        for i in new_end:
            n += 1
            if not isinstance(i, int):
                raise TypeError
            if i < 0:
                raise ValueError
        # n is number of values in tuple
        if n != 2:
            raise ValueError
        # Checks to see if ocean is on new_end, if it is a valid location on grid, and if new_end == start_coords coord
        if new_end[0] == self.start_coords[0] and new_end[1] == self.start_coords[1]:
            raise ValueError
        try:
            if self.grid[new_end[0]][new_end[1]] is 'ocean':
                raise InvalidCoordinateError
        except IndexError:
            raise OutOfBoundaries
        self.__end = new_end

    @property
    def grid(self):
        return self.__grid

    def find_path(self):

        stack = []
        # Create bounds check, same for in solve
        # Down Check
        if 0 <= self.start_coords[1] - 1:
            stack.append((self.start_coords[0], self.start_coords[1] - 1))
        # Left Check
        if 0 <= self.start_coords[0] - 1 and self.start_coords[1] < len(self.grid[self.start_coords[0] - 1]):
            stack.append((self.start_coords[0] - 1, self.start_coords[1]))
        # Up Check
        if len(self.grid[self.start_coords[0]]) > self.start_coords[1] + 1:
            stack.append((self.start_coords[0], self.start_coords[1] + 1))
        # Right check
        if self.start_coords[0] + 1 < len(self.grid):
            if self.start_coords[1] < len(self.grid[self.start_coords[0] + 1]):
                stack.append((self.start_coords[0] + 1, self.start_coords[1]))

        out = self.solve(self.grid, stack, {self.start_coords: [self.start_coords]}, [self.start_coords])
        if not out:
            return None
        ll = LLStack()
        return self.find_path_helper(out, ll)

    # puts out list from solve into LLstack
    def find_path_helper(self, lst: list, ll: LLStack):
        if len(lst) < 1:
            return ll

        ll.push(lst[0])
        return self.find_path_helper(lst[1:], ll)

    def solve(self, grid, stack: list, visited: dict, path: list) -> list:
        # Visited format: (x, y) : [(start_coords, start_coords), (n, n), (n, n), ..., (end, end)]
        if len(stack) < 1:
            return []
        if self.end_coords in visited:
            return visited[self.end_coords]
        # Depth first search influence
        # Pattern, Right, Up, left, down
        current_pos = stack[-1]
        # print('stack: ', stack)
        # print('visited: ', visited)

        stack = stack[:-1]
        if current_pos not in visited:
            if self.grid[current_pos[0]][current_pos[1]] is 'grass':
                visited[current_pos] = path + [current_pos]
                # Checks bounds before adding next areas
                # Down
                if 0 <= current_pos[1] - 1:
                    stack.append((current_pos[0], current_pos[1] - 1))

                # Left
                if 0 <= current_pos[0] - 1:
                    if current_pos[1] < len(self.grid[current_pos[0] - 1]):
                        stack.append((current_pos[0] - 1, current_pos[1]))

                # Up
                if len(self.grid[current_pos[0]]) > current_pos[1] + 1:
                    stack.append((current_pos[0], current_pos[1] + 1))

                # Right
                if current_pos[0] + 1 < len(self.grid):
                    if current_pos[1] < len(self.grid[current_pos[0] + 1]):
                        stack.append((current_pos[0] + 1, current_pos[1]))

                return self.solve(grid, stack, visited, path + [current_pos])

        return self.solve(grid, stack, visited, path)


    def find_shortest_path(self):
        # Dijkstras Algo
        visited = {}
        out = self.solve_shortest(self.grid, {self.start_coords: [self.start_coords]}, visited, [self.start_coords])
        ll = LLStack()
        if not out:
            return None
        return self.find_path_helper(out, ll)

    def solve_shortest(self, grid,  table: dict, visited: dict, path: list) -> list:
        # table format: (x, y): shortest route (replace if len(path) < len(visited[(x, y)])
        if self.end_coords in visited:
            return visited[self.end_coords]
        if len(list(table.values())) < 1:
            return []

        # Get the smallest route in table of paths, so min(in list of len(path)'s from dictionary)
        lst_table_vals = list(table.values())
        smallest_route = self.get_minimum_len_path(list(table.values()))
        # Updates visited list with its path + its end point
        visited[smallest_route] = table[smallest_route]
        path = visited[smallest_route]
        table.pop(smallest_route)

        # Checks (x, y-1)
        check_location = (smallest_route[0], smallest_route[1] - 1)
        if 0 <= check_location[1]:
            if check_location not in visited and check_location not in table:
                if self.grid[check_location[0]][check_location[1]] is 'grass':
                    table[check_location] = path + [check_location]
        # Checks (x-1, y)
        check_location = (smallest_route[0] - 1, smallest_route[1])
        if 0 <= check_location[0] and check_location[1] < len(self.grid[check_location[0]]):
            if check_location not in visited and check_location not in table:
                if self.grid[check_location[0]][check_location[1]] is 'grass':
                    table[check_location] = path + [check_location]
        # Checks (x, y+1)
        check_location = (smallest_route[0], smallest_route[1] + 1)
        if len(self.grid[check_location[0]]) > check_location[1]:
            if check_location not in visited and check_location not in table:
                if self.grid[check_location[0]][check_location[1]] is 'grass':
                    table[check_location] = path + [check_location]
        # Checks (x+1, y)
        check_location = (smallest_route[0] + 1, smallest_route[1])
        if check_location[0] < len(self.grid) and check_location[1] < len(self.grid[check_location[0]]):
            if check_location not in visited and check_location not in table:
                if self.grid[check_location[0]][check_location[1]] is 'grass':
                    table[check_location] = path + [check_location]

        # print(f'--Table--')
        # for k in table:
        #     print(f' {k} | {table[k]}')
        # print(f'\n--Visited--')
        # for k in visited:
        #     print(f' {k} | {visited[k]}')
        # print('======================')
        # wait = input('continue: ')
        return self.solve_shortest(grid, table, visited, path)

    def get_minimum_len_path(self, table_values, min: list = -1):
        if min == -1:
            min = table_values[0]
        elif len(table_values[0]) < len(min):
            min = table_values[0]
        if len(table_values) <= 1:
            return min[-1]

        return self.get_minimum_len_path(table_values[1:], min)

