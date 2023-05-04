import random

ranks = {1: "Deuces", 2: "Threes", 3: "Fours",
         4: "Fives", 5: "Sixes", 6: "Sevens",
         7: "Eights", 8: "Nines", 9: "Tens",
         10: "Jacks", 11: "Queens", 12: "Kings",
         13: "Aces"}

singrank = {1: "Deuce", 2: "Three", 3: "Four",
            4: "Five", 5: "Six", 6: "Seven",
            7: "Eight", 8: "Nine", 9: "Ten",
            10: "Jack", 11: "Queen", 12: "King",
            13: "Ace"}

suits = {1: 'clubs', 2: 'diamonds', 3: 'hearts',
         4: 'spades'}

rank = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
suit = [0, 1, 2, 3]

      
class Card:
    def __init__(self, card):
        self.rank = card[0]
        self.suit = card[1]

    def __str__(self):
        return f'Rank : {singrank[self.rank + 1]} Suit: {suits[self.suit + 1]}'
    
class HoleCards(Card):
    
    def __init__(self, deck):

        self.holecards = [deck.deck.pop(0),
                          deck.deck.pop(0)]
    
class Deck:
    def __init__(self):
        self.builder = [(rnk, sut) for rnk in rank for sut in suit]
        self.deck = []
        ##mock to test functionality.  in this case straight flush logic
        # self.builder = [(4,1),(5,1),(6,1),(10,1),(8,1),(2,1),(3,1),(9,1)]
        # self.deck = []
        for item in self.builder:
            self.deck.append(Card(item))
        random.shuffle(self.deck)

class Player(Card):

    def __init__(self, board):
        self.board = board
        self.fiveCardHand = None
        self.active = True
        self.stack = int(100)
        self.position = 0

class HighCard(Card):

    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.fiveCardHand = []
        self.unpairedElements = self.board.handRankingObject.listUnpaired
        index = 0
        for rank in self.unpairedElements:
            if index < 5:
                self.fiveCardHand.append(rank)
                index += 1
        return self.fiveCardHand

    def __str__(self):
        return f'{singrank[self.fiveCardHand[0] + 1]} high'

class OnePair(Card):

    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.unpairedElements = self.board.handRankingObject.listUnpaired
        self.pair = self.board.handRankingObject.listOfPair
        self.unpairedElements.insert(0, self.pair[0])
        self.unpairedElements.insert(0, self.pair[0])
        self.fiveCardHand = self.unpairedElements[0:5]
        return self.fiveCardHand

    def __str__(self):
        return f'Pair of {ranks[self.fiveCardHand[0] + 1]}'

class TwoPair:
    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.unpairedElements = None
        if self.board.handRankingObject.listUnpaired:
            self.unpairedElements = self.board.handRankingObject.listUnpaired
        self.pairs = self.board.handRankingObject.listOfPair

        if len(self.pairs) == 3 and self.unpairedElements:
            if self.pairs[2] > self.unpairedElements[0]:
                self.fiveCardHand = [self.pairs[0], self.pairs[0],
                                    self.pairs[1], self.pairs[1],
                                    self.pairs[2]]
        elif len(self.pairs) == 3 and not self.unpairedElements:
            self.fiveCardHand = [self.pairs[0], self.pairs[0],
                                self.pairs[1],self.pairs[1],
                                self.pairs[2]]
        else:
            self.fiveCardHand = [self.pairs[0], self.pairs[0],
                                 self.pairs[1], self.pairs[1],
                                 self.unpairedElements[0]]
        return self.fiveCardHand

    def __str__(self):
        return f'Two Pair : {ranks[self.fiveCardHand[0] + 1]} over ' \
               f'{ranks[self.fiveCardHand[2] + 1]}'

class Trips(Card):

    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.unpairedElements = self.board.handRankingObject.listUnpaired
        self.trips = self.board.handRankingObject.listOfTrip
        self.fiveCardHand = []
        self.fiveCardHand.append(self.trips[0])
        self.fiveCardHand.append(self.trips[0])
        self.fiveCardHand.append(self.trips[0])
        self.fiveCardHand.append(self.unpairedElements[0])
        self.fiveCardHand.append(self.unpairedElements[1])
        return self.fiveCardHand

    def __str__(self):
        return f'Three of a kind, {ranks[self.fiveCardHand[0] + 1]}'

class Straight:
    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.fiveCardHand = []
        index = 0
        self.board.handRankingObject.listStraight.sort(reverse=True)
        for rank in self.board.handRankingObject.listStraight:
            if index < 5:
                print(rank)
                self.fiveCardHand.append(rank)
                index += 1
        return self.fiveCardHand

    def __str__(self):
        return f'Straight, {singrank[self.fiveCardHand[0] + 1]} high'

class Flush:
    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.fiveCardHand = []
        self.flushRanks = self.board.handRankingObject.listOfFlushRanks
        index = 0
        for rank in self.flushRanks:
            if index < 5:
                self.fiveCardHand.append(rank)
                index += 1
        return self.fiveCardHand

    def __str__(self):
        return f'Flush, {singrank[self.fiveCardHand[0] + 1]} high.'

class FullHouse:
    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.trips = self.board.handRankingObject.listOfTrip
        self.pairs = self.board.handRankingObject.listOfPair
        self.fiveCardHand = []

        if len(self.trips) == 2:
            self.fiveCardHand.append(self.trips[0])
            self.fiveCardHand.append(self.trips[0])
            self.fiveCardHand.append(self.trips[0])
            self.fiveCardHand.append(self.trips[1])
            self.fiveCardHand.append(self.trips[1])

        if len(self.trips) == 1 and len(self.pairs):
            self.fiveCardHand.append(self.trips[0])
            self.fiveCardHand.append(self.trips[0])
            self.fiveCardHand.append(self.trips[0])
            self.fiveCardHand.append(self.pairs[0])
            self.fiveCardHand.append(self.pairs[0])

        return self.fiveCardHand

    def __str__(self):
        return f'Full House, {ranks[self.fiveCardHand[0] + 1]} ' \
               f'over {ranks[self.fiveCardHand[3] + 1]}'

class Quads:
    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.fiveCardHand = []
        self.quads = self.board.handRankingObject.listOfQuad
        if self.board.handRankingObject.listOfTrip:
            self.trips = self.board.handRankingObject.listOfTrip
        if self.board.handRankingObject.listUnpaired:
            self.unpaired = self.board.handRankingObject.listUnpaired
        if self.board.handRankingObject.listOfPair:
            self.pairs = self.board.handRankingObject.listOfPair

        index = 0
        while index < 4:
            self.fiveCardHand.append(self.quads[0])
            index += 1
        if self.board.handRankingObject.listOfTrip:
            self.fiveCardHand.append(self.trips[0])
        if self.board.handRankingObject.listOfPair \
                and self.board.handRankingObject.listUnpaired:
            if self.pairs[0] > self.unpaired[0]:
                self.fiveCardHand.append(self.pairs[0])
            else:
                self.fiveCardHand.append(self.unpaired[0])
        if not self.board.handRankingObject.listOfPair \
                and self.board.handRankingObject.listUnpaired:
            self.fiveCardHand.append(self.unpaired[0])
        if self.board.handRankingObject.listOfPair and \
            not self.board.handRankingObject.listUnpaired:
                self.fiveCardHand.append(self.pairs[0])

        return self.fiveCardHand

    def __str__(self):
        return f'Four of a kind, {ranks[self.fiveCardHand[0] + 1]}'

class StraightFlush:
    def __init__(self, board):
        self.board = board

    def create_5card_Hand_Obj(self):
        self.fiveCardHand = []
        self.strFlush = self.board.handRankingObject.strFlushRanks
        index = 0
        for item in self.strFlush:
            if index < 5:
                self.fiveCardHand.append(item)
                index += 1
        return self.fiveCardHand

    def __str__(self):
        return f'Straight Flush, {rank[self.fiveCardHand[0] + 1]} high'
