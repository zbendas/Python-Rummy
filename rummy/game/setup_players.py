# -*- coding: utf-8 -*-

from rummy.player.ai import AI
from rummy.player.human import Human
from rummy.game.validator import Validator
from rummy.game.user_input import UserInput


class SetupPlayers:
    players = []
    number_of_players = -1
    number_of_opponents = -1

    def __init__(self):
        self.choose_players()

    def choose_players(self):
        number_of_players = -1
        while number_of_players not in [i for i in range(0, 5)]:
            number_of_players = UserInput.get_input("Enter number of players (0-4)? ")
            number_of_players = Validator.valid_number_check(number_of_players)
        if number_of_players in [0, 1]:
            self.setup_ai(number_of_players)
        self.number_of_players = number_of_players

    def setup_ai(self, number_of_players):
        if number_of_players == 0:
            self.choose_number_of_ai_opponents(4)
        elif number_of_players == 1:
            self.choose_number_of_ai_opponents(3)
        else:
            raise ValueError("Invalid number of players supplied to setup AI opponents.")

    def choose_number_of_ai_opponents(self, max_opponents):
        number_of_opponents = -1
        while number_of_opponents not in [i for i in range(max_opponents - 2, max_opponents + 1)]:
            number_of_opponents = UserInput.get_input(
                "Enter number of opponents ({0}-{1})? ".format(max_opponents - 2, max_opponents))
            number_of_opponents = Validator.valid_number_check(number_of_opponents)
        self.number_of_opponents = number_of_opponents

    def create_players(self):
        i = 0
        players = []
        for j in range(self.number_of_players):
            i += 1
            players.append(Human(i))
        for j in range(self.number_of_opponents):
            i += 1
            players.append(AI(i))
        return players
