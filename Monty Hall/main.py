# Josh Dobbs, Monty Hall Problem, 1/26/2025
# ~ 3 Hours to complete
# Consider a Game Show were a host presents 3 doors to a contestant, behind 2 doors are goats but behind 1 is a brand new
# sports car. Originally the contestant has a 33.33% chance of guessing correctly, but before revealing the host reveals
# one of the other doors to be a goat. The contestant is now given the option to stay at their first guess or switch to the
# other unrevealed door.

import random


class Door:

    def __init__(self, dn):
        self.contains_car = False
        self.door_num = dn

class GameShow:

    def __init__(self, n_doors: int):
        self.n_doors = n_doors
        self.doors = []
        self.__correct_door = random.randint(1, self.n_doors)
        self.start_game()

    def start_game(self):
        for i in range(1, self.n_doors+1):
            self.doors.append(Door(i))
            if i == self.__correct_door:
                correct_door: Door = self.doors[i-1]
                correct_door.contains_car = True

    def takeaway_door(self, first_guess: int):
        if first_guess == self.__correct_door:
            # Selects a random door to remove if the first guess was correct
            wrong_door = random.randint(1, self.n_doors)
            if wrong_door == first_guess:
                wrong_door += random.randint(2,self.n_doors-1)
                wrong_door = wrong_door % self.n_doors
            if self.doors[self.__correct_door - 1].door_num > self.doors[wrong_door - 1].door_num:
                self.doors = [self.doors[self.__correct_door - 1], self.doors[wrong_door - 1]]
            else:
                self.doors = [self.doors[wrong_door - 1], self.doors[self.__correct_door - 1]]

            # print(f'It is not door -> {removed_door_num}')

        else:
            if self.doors[self.__correct_door - 1].door_num > self.doors[first_guess - 1].door_num:
                self.doors = [self.doors[self.__correct_door - 1], self.doors[first_guess - 1]]
            else:
                self.doors = [self.doors[first_guess - 1], self.doors[self.__correct_door - 1]]
            # print(f'It is not door {doors[0]}')

    def confirm_answer(self, second_guess: Door) -> bool:
        if second_guess.contains_car:
            # print('CORRECT')
            return True
        else:
            # print('Wrong')
            return False

class Contestant:

    def __init__(self, n_doors):
        self.first_guess = random.randint(1, n_doors)
        self.first_guess_door = None
        self.win_count = 0

class StatKeeper:

    def __init__(self, n_doors):
        self.n_doors = n_doors
        self.__game = GameShow(n_doors)
        self.__player_switch = Contestant(n_doors)
        self.__player_switch.first_guess_door = self.__game.doors[self.__player_switch.first_guess - 1]

        self.__player = Contestant(n_doors)
        self.__player.first_guess_door = self.__game.doors[self.__player.first_guess - 1]


    def print_switch_results(self, n_runs: int):
        for run in range(n_runs):
            # Takeaway switch player first guess
            self.__game.takeaway_door(self.__player_switch.first_guess)

            # Switch guesses
            second_guess = None
            for d in self.__game.doors:
                if d is not self.__player_switch.first_guess_door and d is not None:
                    second_guess = d
                    break

            # Debug
            if second_guess is None:
                print('second guess not picked')
                break

            if self.__game.confirm_answer(second_guess):
                self.__player_switch.win_count += 1

            # Reset run
            self.reset_game()

        print(f'switch player won {(self.__player_switch.win_count / n_runs) * 100:.0f}% of the time')

    def print_stay_results(self, n_runs: int):
        for run in range(n_runs):
            # Takeaway switch player first guess
            self.__game.takeaway_door(self.__player.first_guess)

            if self.__game.confirm_answer(self.__player.first_guess_door):
                self.__player.win_count += 1

            # Reset run
            self.reset_game()

        print(f'stay player won {(self.__player.win_count / n_runs) * 100:.0f}% of the time')


    def reset_game(self):
        # Resets the game
        self.__game = GameShow(self.n_doors)
        # Resets the players first guess
        self.__player_switch.first_guess = random.randint(1, self.n_doors)
        self.__player_switch.first_guess_door = self.__game.doors[self.__player_switch.first_guess - 1]

        self.__player.first_guess = random.randint(1, self.n_doors)
        self.__player.first_guess_door = self.__game.doors[self.__player.first_guess - 1]

# # TRY PROGRAM HERE # #
# Change # of doors
number_of_doors = 3

# Change number of times game is played (default 5000)
attempts = 5000

sk = StatKeeper(number_of_doors)
# Calculates the amount of times the contestant who stayed with their original guess after the other door(s) were taken away won
sk.print_stay_results(attempts)
# Calculates the amount of times the contestant who changed their answer after the other door(s) were taken away won
sk.print_switch_results(attempts)
