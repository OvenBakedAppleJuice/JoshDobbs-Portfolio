import random

class BlackJack:
    
    def __init__(self, start_money = 100, bj_payout = 1.5, dealer_soft_cap = 17):
        self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        if not isinstance(start_money, (int, float)):
            raise TypeError
        self.player_money = start_money
        self.bet = 0
        self.bj_payout = bj_payout
        self.dealer_soft_cap = dealer_soft_cap
        self.player_hand = []
        self.dealer_hand = []
        self.stored_hands = []

    def deal_card(self):
        return [self.cards[random.randint(0, 12)]]

    def hit(self) -> str:
        self.player_hand += self.deal_card()
        if self.reconcile_hand(self.player_hand) == []:
            return 'PLAYER BUST OVER 21'
        if min(self.reconcile_hand(self.player_hand)) > 21:
            self.bet = 0
            return f'PLAYER BUST WITH {min(self.reconcile_hand(self.player_hand))}'
        return '--HIT--'

    def start(self):
        self.dealer_hand += self.deal_card()
        self.player_hand += self.deal_card() + self.deal_card()
        if max(self.reconcile_hand(self.player_hand)) == 21:
            print(self.player_bj())


    def place_bet(self, bet_amount: str):
        bet_amount = str(bet_amount)
        if bet_amount.isalpha():
            return 'retry'
        bet_amount = int(bet_amount)
        if bet_amount < 1:
            return 'retry'
        if bet_amount > self.player_money:
            return 'INSUFICENT FUNDS'
        self.player_money -= bet_amount
        self.bet = bet_amount
        return f'You bet {bet_amount}'

    def reconcile_hand(self, nums: list):
        total_As = 0
        new_nums = []
        results = []
        for n in range(len(nums)):
            if nums[n] == 1:
                total_As += 1
            else:
                new_nums.append(nums[n])
        if total_As == 0:
            return [sum(nums)]
        else:
            for i in range(total_As + 1):
                els = i * 11
                ones = total_As - i
                results.append(sum(new_nums) + els + ones)
        final_results = []
        for r in results:
            if r <= 21:
                final_results.append(r)
        return final_results

    def new_stand(self, hand: list, bet: int) -> None:
        self.stored_hands.append([hand, bet])
        print(f'+++DEBUG (stored a hand) -> {self.stored_hands} with {[hand, bet]}')
        self.player_hand = []

    def dealer_turn(self) -> int:
        self.dealer_hand += self.deal_card()
        print(f'+++DEBUG (RANDOM DEALER STAND BUG) -> {self.dealer_hand}')
        dealer_total = max(self.reconcile_hand(self.dealer_hand))
        if dealer_total > 21:
            return dealer_total
        elif dealer_total < self.dealer_soft_cap:
            return self.dealer_turn()
        return dealer_total

    def compare_dealer_hand(self, hand: list, dealer_total):
        print(f'++++DEBUG (hand contains): {hand}')
        hand_total = max(self.reconcile_hand(hand[0]))
        if dealer_total > 21:
            self.player_money += 2 * hand[1]
            return f'DEALER BUST WITH {dealer_total}'
        if hand_total > dealer_total:
            self.player_money += 2 * hand[1]
            return f'PLAYER WINS WITH {hand_total} TO {dealer_total}'
        elif hand_total == dealer_total:
            self.player_money += hand[1]
            return 'EQUAL'
        else:
            hand[1] = 0
            return f'DEALER WINS WITH {dealer_total} TO {hand_total}'

        
    def player_bj(self):
        self.new_stand(self.player_hand, self.bet)
        if self.compare_dealer_hand(self.stored_hands[0], self.dealer_turn()) == 'EQUAL':
            return 'EQUAL'
        self.player_money += self.bj_payout * self.bet
        self.reset_hands()
        return 'PLAYER BLACKJACK WINS'
    
    def double_down(self):
        if self.bet > self.player_money:
            return 'no funds'
        self.player_hand += self.deal_card()
        self.player_money -= self.bet
        if min(self.reconcile_hand(self.player_hand)) > 21:
            self.bet = 0
            return 'PLAYER BUST'
        self.new_stand(self.player_hand, self.bet * 2)
        return '--DOUBLE DOWN--'




    def reset_hands(self):
        self.dealer_hand = []
        self.player_hand = []
        self.stored_hands = []
        self.start()

    def split(self):
        if self.player_hand[0] != self.player_hand[1]:
            return 'CANNOT SPLIT'
        if self.player_money < self.bet:
            return 'INSUFICENT FUNDS'
        self.player_money -= self.bet
        self.stored_hands.append([[self.player_hand.pop(1)], self.bet])
        self.player_hand += self.deal_card()
        self.stored_hands[-1][0] += self.deal_card()
        self.stored_hands.append([self.player_hand, self.bet])

        return '--SPLIT--'

    def use_split_hand(self):
        self.player_hand = self.stored_hands[0]
        self.stored_hands.pop(0)



def card_printer(hand):
    tens = [10, 'K ', 'Q ', 'J ']
    p = ''
    p += ' ___   ' * len(hand)
    p += '\n'
    rns = []
    for num in hand:
        if num == 1:
            p += f'|A  |  '
        elif num == 10:
            rn = random.randint(0, 3)
            rns.append(rn)
            p += f'|{tens[rn]} |  '
        else:
            p += f'|{num}  |  '
    p += '\n'
    for num in hand:
        if num == 1:
            p += f'|  A|  '
        elif num == 10:
            if type(tens[rns[0]]) == str:
                p += f'|  {tens[rns[0]].strip()}|  '
            else:
                p += f'| 10|  '
            rns.pop(0)
        else:
            p += f'|  {num}|  '
    p += '\n'
    p += ' ---   ' * len(hand)
    return p




def start_game():
    game = BlackJack()
    print('Welcome to Blackjack!')
    print('To end the game type end or e')
    print('Type help for controls')
    round: int = 1
    GA = True
    print(game.start())

    def print_table():
        print('\nPLAYER:\n')
        print(card_printer(game.player_hand))

    def calculate_winnings(hand) -> None:           #method, prints which hands won and reconciles the bets
        current_round_dealer_total = game.dealer_turn()
        hand_num = 1
        print(game.compare_dealer_hand(hand, current_round_dealer_total))



    def UI_validator(comment: str, response_type = 'action'):
        UI = input(comment)
        if response_type == 'bet':
            if not UI.isdigit():
                if UI.lower() in ['e', 'end', 'end game']:
                    end_game()
                elif UI.lower() in ['help']:
                    print('Goal is to get to 21 without going over\n'
                          'Your options are:'
                          '\n\t1. Hit'
                          '\n\t2. Stand'
                          '\n\t3. Double down'
                          '\n\t4. Split'
                          '\nType in your action when ready\n')
                    return UI_validator(comment, response_type)
                print('INVALID INPUT')
                return UI_validator(comment, response_type)
            UI = int(UI)
            return UI

        elif response_type == 'action':
            if UI in ['help', 'Help', 'HELP', 'HElp']:
                print('Goal is to get to 21 without going over\n'
                      'Your options are:'
                      '\n\t1. Hit'
                      '\n\t2. Stand'
                      '\n\t3. Double down'
                      '\n\t4. Split'
                      '\nType in your action when ready\n')
                return UI_validator(comment, response_type)

            if UI in ['1', 'hit', 'h']:
                result = game.hit()
                if result == '--HIT--':
                    print(result)
                    print_table()
                    return UI_validator(comment)
                print_table()
                return result

            elif UI in ['2', 'stand', 'stan', 's']:
                game.new_stand(game.player_hand, game.bet)
                return '--STAND--'

            elif UI in ['3', 'double down', 'dd', 'd', 'double', 'double d', 'doubl d']:
                ddr = game.double_down()
                if ddr == 'no funds':
                    print('NOT ENOUGH FUNDS TO DOUBLE DOWN')
                    return UI_validator(comment)
                print_table()
                return ddr

            elif UI in ['4', 'split', 'splt', 'sp', 'spli']:
                spltr = game.split()
                if spltr == 'CANNOT SPLIT':
                    print(spltr)
                    return UI_validator(comment)
                elif spltr == 'INSUFICENT FUNDS':
                    print(spltr)
                    return UI_validator(comment)
                return spltr
            else:
                print('INVALID RESPONSE')
                return UI_validator(comment)


    def end_game():
        print(f'LEAVING TABLE\nYou cashed out with {game.player_money}')
        GA = False
        pass


    def start_round(round) -> None:
        print(f'=============ROUND: {round}================')
        print(f'Place your bet, you have {game.player_money}')
        Bet_UI = UI_validator('Bet Amount: ', 'bet')
        print(game.place_bet(Bet_UI))
        print('-------BET PLACED--------')
        print(card_printer(game.dealer_hand + ['X']))
        play_round()


    def play_round() -> None:
        outputs = []
        hand_num = 1
        number_of_hands = len(game.stored_hands)
        if number_of_hands > 1:
            for hand in range(number_of_hands):         #iterates for number of hands
                print(f"====HAND: {hand_num}====")
                print_table()
                result = UI_validator('Your turn: ')
                print(result)
                print(f'+++DEBUG in play_rounds(), for loop hand index is {hand}')
                outputs.append(calculate_winnings(game.stored_hands[hand]))
                hand_num += 1
                game.use_split_hand()               #rotates in next stored hand
        else:
            print_table()
            result = UI_validator('Your turn: ')
            print(result)
            if len(game.stored_hands) > 1:
                print('++DEBUG: This Ran')
                play_round()
            else:
                outputs.append(calculate_winnings(game.stored_hands[0]))

        hand_num = 1
        for output in outputs:
            if number_of_hands > 1:
                print(f'====HAND: {hand_num}====')
            if output != None:
                print(output)

        print('FINAL DEALER HAND:')
        print(card_printer(game.dealer_hand))
        game.reset_hands()
        if game.player_money > 0 and GA:
            start_round(round + 1)
        else:
            end_game()

    # game.player_hand = [9, 9]
    # game.split()
    # print(game.stored_hands)
    start_round(round)
    #calculate_winnings()



start_game()

        
                
        



