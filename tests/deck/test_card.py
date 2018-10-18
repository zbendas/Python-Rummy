# coding=utf-8

from pytest import raises

from rummy.deck.card import Card


class TestCard:

    def test_str(self):
        card = Card("A", "♥")
        assert str(card) == "A♥"
        card = Card("2", "C")
        assert str(card) == "2♣"

    def test_eq(self):
        card1 = Card("A", "♥")
        card2 = Card("A", "♥")
        card3 = Card("2", "♥")
        card4 = Card("2", "♣")
        assert card1 == card2
        assert not card1 == card3
        assert not card3 == card4

    def test_get_card_colour(self):
        card1 = Card("A", "H")
        card2 = Card("3", "S")
        card3 = Card("3", "M")
        assert 'A\x1b[0;31m♥\x1b[0m' == card1.get_card_colour()
        assert '3♠' == card2.get_card_colour()
        with raises(ValueError, message="Expecting ValueError passed on card3.suit"):
            card3.get_card_colour()

    def test_value_ace(self):
        card = Card("A", "♥")
        assert "A" == card.value

    def test_value_number(self):
        card = Card("7", "♥")
        assert "7" == card.value

    def test_suit_plain(self):
        card = Card("A", "H")
        assert card.suit == "♥"

    def test_red_card_plain_text(self):
        card = Card("A", "H")
        assert 'A\x1b[0;31m♥\x1b[0m' == card.get_card_colour()

    def test_diamond_glyph(self):
        card = Card("8", "♦")
        assert '8\x1b[0;31m♦\x1b[0m' == card.get_card_colour()

    def test_heart_glyph(self):
        card = Card("T", "♥")
        assert 'T\x1b[0;31m♥\x1b[0m' == card.get_card_colour()

    def test_club_glyph(self):
        card = Card("K", "♣")
        assert 'K♣' == card.get_card_colour()

    def test_spade_glyph(self):
        card = Card("A", "♠")
        assert 'A♠' == card.get_card_colour()

    def test_red_card_no_unicode(self, mocker):
        mocker.patch('rummy.deck.card.UNICODE_SUPPORT', False)
        card = Card("A", "♥")
        assert card.red_card() == "A♥"
