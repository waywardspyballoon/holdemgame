import unittest
from holdemmain.holdem import Card
from holdemmain.holdem import Deck

class HoldemTest(unittest.TestCase):

    def test_deck_is_52_cards_in_length(self):
        deck = Deck()
        self.assertEqual(len(deck.deck),52)

    
