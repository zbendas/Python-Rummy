# -*- coding: utf-8 -*-

from player.player_action_dialogs import PlayerActionDialogs
from rummy.player.player import Player
from ui.user_input import UserInput
from ui.view import View


class Human(Player):

    def show_turn_start(self):
        return View.template_turn_start(self)

    def show_turn_end(self):
        return View.template_player_turn_end(self)

    def draw_from_deck_or_pick_up(self):
        if self.round.deck.has_discard():
            self.choose_pick_up()
        else:
            self.take_from_deck()

    def choose_pick_up(self):
        user_input = UserInput.create_input(PlayerActionDialogs.pick_up_or_draw())
        if user_input == 'p':
            self.take_from_discard()
        else:
            self.take_from_deck()

    def discard_or_knock(self):
        scores = self.melds.find_discard_scores(self.hand.get_hand())
        user_input = ''
        while user_input not in [str(i) for i in range(1, 9)]:
            if min(scores) <= 10 and not self.round.knocked:
                user_input = UserInput.create_input(PlayerActionDialogs.choose_discard_or_knock())
                if user_input == "k":
                    self.knock()
                    continue
            else:
                user_input = UserInput.create_input(PlayerActionDialogs.choose_discard())
        self.discard(user_input)

    def show_discard(self):
        return 'Discarded: %s' % self.round.deck.inspect_discard()
