import os

from art import logo, deck
from game import Game

os.system('cls')
print(logo)
local_deck = []
deck_choice = input("How many decks would you like to play with? ")
try:
    for _ in range(int(deck_choice)):
        for card in deck:
            local_deck.append(card)
except TypeError:
    print("Invalid, defaulting to one deck.")
    for card in deck:
        local_deck.append(card)

bet_choice = input("What would you like to set your default bet at? ")
try:
    bet = int(bet_choice)
except TypeError:
    print("Invalid bet, defaulting to $100 hands")
    bet = 100

while True:
    game = Game(local_deck, bet)
    game.display_cards()
    result = game.choice()
    while True:
        game_choice = input("Would you like to play again? (y/n): ")
        if game_choice not in ('y', 'n'):
            print("Invalid choice")
        elif game_choice == 'y':
            break
        else:
            quit()
