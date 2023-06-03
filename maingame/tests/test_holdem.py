import unittest
from unittest.mock import MagicMock
from holdemmain.holdem import Card
from holdemmain.holdem import HoleCards
from holdemmain.holdem import Deck
from holdemmain.holdem import Player
from holdemmain.board import Board

class HoldemTest(unittest.TestCase):

    def test_deck_is_52_cards_in_length(self):
        deck = Deck()
        self.assertEqual(len(deck.deck),52)

    def test_correctly_assigning_rank(self):
        def setupAndAnalyze(total_players):
            for player in total_players:
                player.board.createSortable()
                player.board.getRank()
                player.board.storeFiveCardHand()
            return None
        deckForGame = MagicMock()
        deckForGame.builder = [(4,1),(5,1),(6,1),(10,1),(8,1),(2,1),(3,1),(9,1)]
        deckForGame.deck = []
        for item in deckForGame.builder:
            deckForGame.deck.append(Card(item))
        
        flop = (deckForGame.deck.pop(0),
            deckForGame.deck.pop(0),
            deckForGame.deck.pop(0))
    
        players = [Player(Board(flop, HoleCards(deckForGame)))]
            
        total_players = players[:]
        setupAndAnalyze(total_players)

        self.assertEqual(total_players[0].board.handRank, 5)


        





    
