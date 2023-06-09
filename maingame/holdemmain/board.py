from holdemmain import Analyze, SortForAnalysis
from holdemmain import (HighCard, OnePair, TwoPair,
                    Trips, Straight, Flush, 
                    FullHouse, Quads, StraightFlush)
from holdemmain import *
from copy import deepcopy


class Board(Card):
    """sets up flop, and appends hole cards
    to create initial board state.  Allows
    for additional cards to be passed in,
    for the cards to be stored in a sortable
    state, and for their order to be modified"""

    def __init__(self, flop: tuple, holeCards):
        self.handRankDict = {0: HighCard, 1: OnePair,
                             2: TwoPair, 3: Trips,
                             4: Straight, 5: Flush,
                             6: FullHouse, 7: Quads,
                             8: StraightFlush}
        self.boardState = []
        self.sortable = None
        self.handRank = 0
        for item in flop:
            self.boardState.append(item)
        self.holeCards = holeCards
        for item in self.holeCards.holecards:
            self.boardState.append(item)

    def listElements(self):
        countedElements = []
        for item in self.boardState:
            countedElements.append(item.rank)
        return countedElements

    def createSortable(self):
        tempSort = SortForAnalysis(self)
        self.sortable = tempSort.valuelist()

    def getRank(self):
        self.handRankingObject = Analyze(self)
        self.handRank = self.handRankingObject.determineRank()

    def storeFiveCardHand(self):
        self.initRank = self.handRankDict[self.handRank](self)
        self.fiveCardHand = self.initRank.create_5card_Hand_Obj()
        # print(self.fiveCardHand)

    def add(self, card: Card):
        self.boardState.append(card)
        self.sortable = self.createSortable()

    def exportedBoard(self):
        return deepcopy(self.boardState)
    
    def __gt__(self, other):

        if self.handRank > other.handRank:
            return True
        elif self.handRank < other.handRank:
            return False
        
        for _ in self.fiveCardHand:
            first = self.fiveCardHand.pop(0)
            second = other.fiveCardHand.pop(0)
            if first > second:
                return True
            elif first < second:
                return False
            else:
                continue

    def __eq__(self, other):

        if self.handRank > other.handRank:
            return False
        elif self.handRank < other.handRank:
            return False
        
        for _ in range(0, len(self.fiveCardHand)):
            first = self.fiveCardHand.pop(0)
            second = other.fiveCardHand.pop(0)
            if first > second:
                return False
            elif first < second:
                return False
            else:
                continue
        return True
        
