import os
import random
import time

from art import logo

win = 0
loss = 0
push = 0
money = 10000


# noinspection PyNoneFunctionAssignment
class Game:
    blank_card = {
        "name": "?",
        "value": "?",
        "suit": " "
    }

    def __init__(self, deck, bet):
        self.card_deck = deck
        self.bet = bet
        self.initialize_bet()
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_value = self.evaluate_hand(self.dealer_hand)
        self.player_value = self.evaluate_hand(self.player_hand)
        self.players_turn = True
        self.natural_blackjack = False
        self.players_visible_hand = None
        self.dealers_visible_hand = None

    def initialize_bet(self):
        global money
        money -= self.bet

    def draw_card(self):
        card = random.choice(self.card_deck)
        self.card_deck.remove(card)
        return card

    def evaluate_hand(self, hand):
        hand_value = 0
        ace_count = 0

        # establish if hand contains an ace
        for card in hand:
            if card["name"] == "ace":
                ace_count += 1

        # establish hand value
        for card in hand:
            if card["name"] == "ace":
                hand_value += card["value"][1]  # 11
            elif card["name"] in ('jack', 'queen', 'king'):
                hand_value += card["value"][0]  # 10
            else:
                hand_value += card["value"]

        while hand_value > 21 and ace_count > 0:
            hand_value -= 10
            ace_count -= 1

        # return value
        if hand_value == 21 and len(hand) == 2:
            self.natural_blackjack = True
            return 'Blackjack!'
        else:
            return hand_value

    @staticmethod
    def draw_card_portrait(hand):
        display = [""] * 9

        for card in hand:
            name, value, suit = (card["name"], card["value"], card["suit"])

            # construct card images
            display[0] += " ┌─────────┐"
            if name == "ace":
                display[1] += " │{}        │".format(value[2].upper())
                display[4] += " │    {}    │".format(suit)
                display[7] += " │        {}│".format(value[2].upper())
            elif type(value) is list:
                display[1] += " │{}        │".format(value[1].upper())
                display[4] += " │    {}    │".format(suit)
                display[7] += " │        {}│".format(value[1].upper())
            elif value == 10:
                display[1] += " │{}       │".format(value)
                display[4] += " │    {}    │".format(suit)
                display[7] += " │       {}│".format(value)
            else:
                display[1] += " │{}        │".format(value)
                display[4] += " │    {}    │".format(suit)
                display[7] += " │        {}│".format(value)
            display[2] += " │         │"
            display[3] += " │         │"
            display[5] += " │         │"
            display[6] += " │         │"
            display[8] += " └─────────┘"

        print("\n".join(display))

    def display_cards(self):
        global win, loss, push
        os.system('cls')
        print(logo)
        if win or loss or push:
            print(f"Wins: {win}, Loss: {loss}, Push: {push}")
        if self.bet:
            print("==========")
            print(f"Your bet: ${self.bet}, total: {money}")
        print("==========")
        if self.players_turn:
            self.draw_card_portrait([self.dealer_hand[0], self.blank_card])
            print(f"Dealer's upcard: {self.dealer_hand[0]['name']}")
            self.draw_card_portrait(self.player_hand)
            print(f"Player's hand value: {self.player_value}")
            print("==========")
            time.sleep(1)
        else:
            self.draw_card_portrait(self.dealer_hand)
            print(f"Dealer's hand value: {self.dealer_value}")
            self.draw_card_portrait(self.player_hand)
            print(f"Player's hand value: {self.player_value}")
            print("==========")

    def hit(self, hand):
        card = self.draw_card()
        hand.append(card)

    def choice(self):
        global win, loss, push, money
        # flags
        # dealer_has_ace = self.dealer_hand[0]["name"] == 'ace' # TODO: This is for insurance, implement this
        # player_can_split = self.player_hand[0]["name"] == self.player_hand[1] # TODO: Implement this
        dealer_has_natural = self.dealer_value == 'Blackjack!'
        player_has_natural = self.player_value == 'Blackjack!'
        if player_has_natural and dealer_has_natural:  # Both naturals
            self.players_turn = False
            self.display_cards()
            print("Dual blackjacks result in a push! Bets are returned.")
            money += self.bet
            push += 1
            return
        elif player_has_natural and not dealer_has_natural:  # Player natural
            self.players_turn = False
            self.display_cards()
            print(f"You got a blackjack and the dealer did not. You win ${self.bet * 1.5}!")
            money += self.bet * 1.5
            win += 1
            return
        elif not player_has_natural and dealer_has_natural:  # Dealer natural
            self.players_turn = False
            self.display_cards()
            print("Dealer has a blackjack and you do not. You lose.")
            loss += 1
            return

        # Player's turn
        while self.player_value <= 21:
            choice = input("Do you want to hit or stand? ")
            if choice not in ('hit', 'stand'):
                print("Invalid choice.")
            elif choice == 'hit':
                self.hit(self.player_hand)
                self.player_value = self.evaluate_hand(self.player_hand)
                self.display_cards()
                if self.player_value > 21:
                    print(f"Bust! You lose.")
                    loss += 1
                    return
            elif choice == 'stand':
                self.players_turn = False
                self.display_cards()
                break

        # Stand
        while self.dealer_value < 17:
            time.sleep(1)
            self.hit(self.dealer_hand)
            self.dealer_value = self.evaluate_hand(self.dealer_hand)
            self.display_cards()
            if self.dealer_value > 21:
                print(f"Dealer busts, you win ${self.bet}!")
                money += self.bet * 2
                win += 1
                return
            elif 21 >= self.dealer_value > self.player_value:
                print(f"Dealer wins. You lose.")
                loss += 1
                return

        # Player stand and dealer drew to 17:
        if self.player_value > self.dealer_value:
            print(f"You win ${self.bet}!")
            money += self.bet * 2
            win += 1
            return
        elif self.player_value == self.dealer_value:
            print("Push! Bets returned.")
            money += self.bet
            push += 1
            return
        else:
            print(f"You lose.")
            loss += 1
            return
