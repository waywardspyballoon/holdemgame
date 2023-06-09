import unittest
from unittest.mock import MagicMock
from holdemmain.holdem import Card
from holdemmain.holdem import HoleCards
from holdemmain.holdem import Deck
from holdemmain.holdem import Player
from holdemmain.board import Board

class TestBoard(unittest.TestCase):


    def test_correctly_evaluating_tie(self):
        deckForGame = Deck()
        flop = (deckForGame.deck.pop(0),
                deckForGame.deck.pop(0),
                deckForGame.deck.pop(0)) 
        first = Board(flop, HoleCards(deckForGame))
        first.fiveCardHand = [12,12,11,2,0]
        first.handRank = 1

        other = Board(flop, HoleCards(deckForGame))
        other.fiveCardHand = [12,12,11,2,0]
        other.handRank = 1

        self.assertTrue(first == other)


         