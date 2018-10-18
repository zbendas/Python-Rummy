# coding=utf-8

from rummy.player.ai import AI
from rummy.player.hand import Hand
from rummy.deck.card import Card
from rummy.deck.deck import Deck
from rummy.game.melds import Melds
from rummy.game.view import View


class TestAI:
    # This test suite leaves out functions that primarily serve to render templates/text

    def test_choose_to_discard_or_pick_up(self, mocker):
        mocker.patch.object(View, 'render')
        mocker.patch.object(View, 'template_turn_start')
        mocker.spy(AI, 'choose_pick_up')
        mocker.spy(Hand, 'draw_card')
        ai = AI(1)
        ai.round = mocker.MagicMock()
        ai.round.deck.take_card.return_value = Card("A", "♥")
        # self.ai_only = False
        ai.round.deck.has_discard.return_value = True
        ai.choose_to_discard_or_pick_up()
        assert AI.choose_pick_up.call_count == 1
        assert Hand.draw_card.call_count == 1
        ai.round.deck.has_discard.return_value = False
        ai.choose_to_discard_or_pick_up()
        assert AI.choose_pick_up.call_count == 1
        assert Hand.draw_card.call_count == 2
        # Reset call counter to be sure ai_only mode calls render appropriately
        View.render.call_count = 0
        ai.hand.hand = [Card(x, y) for x, y in [("A", "H"), ("2", "S")]]
        # self.ai_only = True
        ai.round.deck.has_discard.return_value = True
        mocker.patch.object(Melds, 'find_discard_scores', return_value=[10, 8])
        ai.ai_only = True
        ai.choose_to_discard_or_pick_up()
        assert View.render.call_count == 6
        ai.round.deck.has_discard.return_value = False
        ai.choose_to_discard_or_pick_up()
        assert View.render.call_count == 8

    def test_choose_pick_up(self, mocker):
        mocker.patch.object(View, 'render')
        mocker.patch.object(Hand, 'get_score', return_value=45)
        mocker.patch.object(Hand, 'draw_card')
        mocker.patch.object(Melds, 'find_discard_scores', side_effect=[[50, 60, 30], [12, 9, 15], [70],
                                                                       [50, 60, 30]])
        ai = AI(1)
        ai.round = mocker.MagicMock()
        ai.round.deck.take_discard.return_value = Card("A", "♥")
        ai.round.deck.take_card.return_value = Card("2", "♥")
        # self.ai_only = False
        # Test for min(scores) < current score, but > 10
        ai.choose_pick_up()
        assert ai.round.deck.take_discard.call_count == 1
        assert ai.round.deck.take_card.call_count == 0
        assert ai.hand.draw_card.call_count == 1
        # Test for min(scores) < current_score - 4 and <=10
        ai.choose_pick_up()
        assert ai.round.deck.take_discard.call_count == 2
        assert ai.round.deck.take_card.call_count == 0
        assert ai.hand.draw_card.call_count == 2
        # Test for min(scores) >= current_score - 4 and > 10
        ai.choose_pick_up()
        assert ai.round.deck.take_discard.call_count == 2
        assert ai.round.deck.take_card.call_count == 1
        assert ai.hand.draw_card.call_count == 3
        # Reset call counter to be sure ai_only mode calls render appropriately
        View.render.call_count = 0
        # self.ai_only = True
        # Test for min(scores) < current score, but > 10
        ai.ai_only = True
        ai.choose_pick_up()
        assert ai.round.deck.take_discard.call_count == 3
        assert ai.round.deck.take_card.call_count == 1
        assert ai.hand.draw_card.call_count == 4
        assert View.render.call_count == 4

    def test_discard_or_knock(self, mocker):
        mocker.patch.object(View, 'render')
        # Mock random.choice to assure that the last item from our array of scores is chosen,
        # to make this test predictable/consistent
        mocker.patch('rummy.player.ai.choice',
                     return_value=(2, 8))
        mocker.patch.object(Melds, 'find_discard_scores', side_effect=[[10, 8, 8], [11], [12]])
        mocker.patch.object(Hand, 'discard_card')
        mocker.patch.object(Deck, 'discard_card')
        ai = AI(1)
        ai.round = mocker.MagicMock()
        ai.hand.hand = [Card("A", "♥"), Card("2", "♥")]
        # self.ai_only = False
        ai.round.knocked = False
        ai.discard_or_knock()
        assert ai.round.knocked
        ai.hand.discard_card.assert_called_with(2)
        assert ai.round.deck.discard_card.call_count == 1
        ai.discard_or_knock()
        assert ai.round.knocked
        ai.hand.discard_card.assert_called_with(0)
        assert ai.round.deck.discard_card.call_count == 2
        # Reset call counter to be sure ai_only mode calls render appropriately
        View.render.call_count = 0
        # self.ai_only = True
        ai.ai_only = True
        ai.round.knocked = False
        ai.discard_or_knock()
        assert View.render.call_count == 4

