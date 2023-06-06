class GameRound:
    def __init__(self, game, street):
        self.currentBet = 0
        self.game = game
        self.street = street
        self.firstToAct = 0
        self.endRoundEvent = 0

    def setup_action(self):
        if self.street == 0:
            if self.firstToAct == 0:
                self.firstToAct = 1
            else:
                self.firstToAct = 0
            
            bet(self, .5)
            self.firstToAct += 1
            bet(self, 1)
            self.firstToAct += 1
            
            # self.game.pot += 1.5

    def checkOrBet(self):
        action = input(f'[c]heck, [b]et (amount 0 - {self.game.players[self.firstToAct % 2].stack}\n')

        if action == 'c':
            self.game.players[self.firstToAct % 2].hasChecked = True
            self.firstToAct += 1
            return None

        if action == 'b':
            current = input(f'input amount from 1 - {self.game.players[self.firstToAct % 2].stack} \n')
            current = int(current)
            if current > self.game.players[self.firstToAct % 2].stack or 0 >= current:
                print('invalid amount')
                self.checkOrBet()
            self.currentBet = current
            self.game.players[self.firstToAct % 2].hasBet = True
            self.game.pot += self.currentBet
            self.game.players[self.firstToAct % 2].playerLastBet = self.currentBet
            self.game.players[self.firstToAct % 2].stack -= self.currentBet
            print(self.game.players[self.firstToAct % 2].stack, self.game.pot)
            self.firstToAct += 1
            return None
                
    def callRaiseOrFold(self):

        print(f'pot : {self.game.pot} \n \
              stack of player {self.firstToAct % 2}:\
              {self.game.players[self.firstToAct % 2].stack})')
        action = input(f'[c]all (amount : {self.currentBet}, [r]aise, or [f]old \n')

        if not action:
            print('try again, empty field is not valid response')
            self.callRaiseOrFold()

        if action == 'f':
            self.game.players[self.firstToAct % 2].didFold = True
            return None
        
        if action == 'r':

            upperBound = int(self.game.players[self.firstToAct % 2].stack + self.game.players[self.firstToAct % 2].playerLastBet)
            new_value = input(f'raise size (between {self.currentBet} and \
                                {upperBound} \n')
            new_value = int(new_value)
            self.currentBet = new_value
            self.betDifference = (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.players[self.firstToAct % 2].stack -= self.betDifference
            self.game.pot += self.betDifference
            self.game.players[self.firstToAct % 2].hasBet = True
            self.game.players[self.firstToAct % 2].playerLastBet = self.currentBet
            self.firstToAct += 1

            return None

        if action == 'c':
            self.game.pot += (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.players[self.firstToAct % 2].hasCalled = True
            return None

    def callOrFold(self):
        action = input(f'[c]all bet (bet amount : {self.currentBet} with remaining stack : \
                       {self.game.players[self.firstToAct % 2].stack}\n or [f]old?')
        if action == 'c':
            # self.game.pot += (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.pot += self.game.players[self.firstToAct % 2].stack

            if self.game.players[self.firstToAct % 2].stack == 0:
                self.game.players[self.firstToAct % 2].isAllIn = True
            
            self.game.players[self.firstToAct % 2].hasCalled = True
            return None
        if action == 'f':
            self.game.players[self.firstToAct % 2].didFold = True
            return None
        

    def bettingAction(self):

        while not self.endRoundEvent:

            if self.game.players[0].isAllIn and self.game.players[1].isAllIn:
                self.endRoundEvent = 1

            if not self.game.players[0].hasBet and not self.game.players[0].hasBet:
                self.checkOrBet()
            
            if self.currentBet:
                if self.game.players[0].isAllIn or self.game.players[1].isAllIn:
                    self.callOrFold()
                    self.endRoundEvent = 1
                elif self.currentBet >= (self.game.players[self.firstToAct % 2].stack + \
                                            self.game.players[self.firstToAct % 2].playerLastBet):
                    print(self.game.players[self.firstToAct % 2].stack)
                    print(f'current bet {self.currentBet}')
                    print(f'pot {self.game.pot}')
                    print('entering')
                    self.callOrFold()
                    self.endRoundEvent = 1
                elif (self.game.players[self.firstToAct % 2].playerLastBet + self.game.players[self.firstToAct % 2].stack <= \
                      self.currentBet):
                    self.callOrFold()
                    self.endRoundEvent = 1
                else:
                    self.callRaiseOrFold()

            if self.game.players[0].hasChecked and self.game.players[1].hasChecked:
                self.endRoundEvent = 1

            if self.game.players[0].didFold or self.game.players[1].didFold:
                self.endRoundEvent = 1

            if self.game.players[0].hasCalled or self.game.players[1].hasCalled:
                self.endRoundEvent = 1

        print(f'pot is {self.game.pot}')
        print('it is ovah')
        

def bet(roundObject, amount):
    roundObject.currentBet = amount
    roundObject.game.pot += roundObject.currentBet
    roundObject.game.players[roundObject.firstToAct % 2].playerLastBet = roundObject.currentBet
    roundObject.game.players[roundObject.firstToAct % 2].stack -= roundObject.currentBet
    roundObject.game.players[roundObject.firstToAct % 2].hasBet = True
    return None
            