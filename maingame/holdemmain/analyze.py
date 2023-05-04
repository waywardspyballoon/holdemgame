from copy import deepcopy
from itertools import groupby

class Analyze:

    def __init__(self, board):
        self.board = board
        self.sortList = self.board.sortable

    def determineRank(self):

        def countNumOfSuit():
            tempSuitStore = {}
            for card in self.board.boardState:
                if card.suit in tempSuitStore:
                    tempSuitStore[card.suit] += 1
                else:
                    tempSuitStore[card.suit] = 1
            return tempSuitStore

        def checkStraight():
            def createIterable():
                tempRankStore = []
                for card in self.board.boardState:
                    tempRankStore.append(card.rank)
                set(tempRankStore)
                return list(tempRankStore)

            sequenceToCheck = createIterable()
            sequenceToCheck.sort()

            gb = groupby(enumerate(sequenceToCheck), key=lambda x: x[0] - x[1])
            all_groups = [[i[1] for i in g] for _, g in gb]
            possStraight = max(all_groups, key=len)
            if self.flushSuit:
                flushSuitToCheck = self.flushSuit[0]
            if len(possStraight) >= 5:
                self.listStraight = possStraight
                print(self.listStraight)
                if len(self.flushSuit) > 0:
                    indcount = 0
                    self.strFlushRanks = []
                    copyOfBoard = deepcopy(self.board.boardState)
                    for card in copyOfBoard:
                        if card.rank in self.listStraight:
                            if card.suit == flushSuitToCheck:
                                self.strFlushRanks.append(card.rank)
                                indcount += 1
                    if len(self.strFlushRanks) >= 5:
                        self.strFlushRanks.sort(reverse=True)
                        return 8
                else:
                    return 4

        print(f'\n')

        self.suits = countNumOfSuit()
        self.listUnpaired = [k for k, v in self.sortList.items() if v == 1]
        self.listOfPair = [k for k, v in self.sortList.items() if v == 2]
        self.listOfTrip = [k for k, v in self.sortList.items() if v == 3]
        self.listOfQuad = [k for k, v in self.sortList.items() if v == 4]
        self.flushSuit = [i for i, x in self.suits.items() if x >= 5]
        if self.flushSuit:
            self.listOfFlushRanks = [card.rank for card in self.board.boardState
                               if card.suit == self.flushSuit[0]]
            self.listOfFlushRanks.sort(reverse=True)
        self.listUnpaired.sort(reverse=True)
        self.listOfPair.sort(reverse=True)
        self.listOfTrip.sort(reverse=True)
        self.listOfTrip.sort(reverse = True)
        self.strFlushRanks = None

        if checkStraight() and self.strFlushRanks:
            return 8

        if self.listOfQuad:
            return 7

        if len(self.listOfTrip) == 2:
            return 6

        if len(self.listOfTrip) and self.listOfPair:
            return 6

        if self.flushSuit:
            return 5

        if checkStraight():
            return checkStraight()

        if self.listOfTrip:
            return 3

        if len(self.listOfPair) > 1:
            return 2

        if self.listOfPair:
            return 1

        return 0
    
class SortForAnalysis:

    def __init__(self, board):
        self._boardObject = board

    def valuelist(self):
        nums = self._boardObject.listElements()
        vals = {}

        for val in nums:
            if val in vals:
                vals[val] += 1
            else:
                vals[val] = 1
        return vals