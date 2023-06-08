class GameRound:
    def __init__(self, game, street, first):
        self.currentBet = 0
        self.game = game
        self.street = street
        self.firstToAct = first
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
        else:
            self.game.players[0].hasCalled = False
            self.game.players[1].hasCalled = False
            self.game.players[0].hasChecked = False
            self.game.players[1].hasChecked = False
            self.game.players[0].hasBet = False
            self.game.players[1].hasBet = False
            self.game.players[0].playerLastBet = 0
            self.game.players[1].playerLastBet = 0
            self.currentBet = 0
            self.endRoundEvent = 0
    
    def print_action(self):
        print(f'player {self.firstToAct % 2} \n\
              remaining stack {self.game.players[self.firstToAct % 2].stack}\
              size of pot {self.game.pot}')
    
    def checkOrRaise(self):
        self.print_action()
        action = input('[c]heck or [r]aise ')
        if action == 'c':
            self.game.players[self.firstToAct % 2].hasChecked = True
            self.firstToAct += 1
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
            if self.game.players[self.firstToAct % 2].stack == 0:
                print('reaching')
                self.game.players[self.firstToAct % 2].isAllIn = True
            
            for player in self.game.players:
                player.hasCalled = False


            self.firstToAct += 1

            return None
        

    def checkOrBet(self):
        self.print_action()
        action = input(f'[c]heck, [b]et (amount 0 - {self.game.players[self.firstToAct % 2].stack}\n')

        if action == 'c':
            print('block 2')
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

        self.print_action()
        if self.street == 0 and self.game.pot == 2:
            self.checkOrRaise()

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
            if self.game.players[self.firstToAct % 2].stack == 0:
                print('reaching')
                self.game.players[self.firstToAct % 2].isAllIn = True

            self.firstToAct += 1

            return None

        if action == 'c':
            print(self.game.players[self.firstToAct % 2].playerLastBet)

            if self.street == 0:
                if self.game.players[self.firstToAct % 2].playerLastBet == .5:
                    print('block 1')
                    new_value = 1
                    self.currentBet = new_value
                    self.betDifference = (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
                    self.game.players[self.firstToAct % 2].stack -= self.betDifference
                    self.game.pot += self.betDifference
                    self.game.players[self.firstToAct % 2].hasBet = True
                    self.game.players[self.firstToAct % 2].hasCalled = True
                    self.game.players[self.firstToAct % 2].playerLastBet = self.currentBet
                    self.firstToAct += 1
                    return None
            
            self.betDifference = (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.players[self.firstToAct % 2].stack -= self.betDifference    
            self.game.pot += (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.players[self.firstToAct % 2].hasCalled = True
            return None

    def callOrFold(self):
        self.print_action()
        action = input(f'[c]all bet (bet amount : {self.currentBet} with remaining stack : \
                       {self.game.players[self.firstToAct % 2].stack}\n or [f]old?')
        if action == 'c':
            # self.game.pot += self.game.players[self.firstToAct % 2].stack
            self.betDifference = (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.players[self.firstToAct % 2].stack -= self.betDifference    
            self.game.pot += (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)

            if self.game.players[self.firstToAct % 2].stack == 0:
                print('reaching')

                self.game.players[self.firstToAct % 2].isAllIn = True
            
            self.game.players[self.firstToAct % 2].hasCalled = True
            return None
        
        if action == 'f':
            self.game.players[self.firstToAct % 2].didFold = True
            return None
        

    def bettingAction(self):

        while not self.endRoundEvent:

            print(self.game.players[0].hasChecked, self.game.players[1].hasCalled)


            if self.game.players[0].hasChecked and self.game.players[1].hasCalled:
                break

            if self.game.players[1].hasChecked and self.game.players[0].hasCalled:
                break


            if self.game.players[0].isAllIn and self.game.players[1].isAllIn:
                break

            if not self.game.players[0].hasBet and not self.game.players[0].hasBet:
                self.checkOrBet()
            
            if self.currentBet:
                if self.game.players[0].isAllIn or self.game.players[1].isAllIn:
                    self.callOrFold()
                    if self.game.players[self.firstToAct % 2].hasCalled:
                        self.game.players[self.firstToAct % 2].isAllIn = True
                    break
                elif self.currentBet >= (self.game.players[self.firstToAct % 2].stack + \
                                            self.game.players[self.firstToAct % 2].playerLastBet):
                    self.callOrFold()
                    self.endRoundEvent = 1
                elif (self.game.players[self.firstToAct % 2].playerLastBet + self.game.players[self.firstToAct % 2].stack <= \
                      self.currentBet):
                    self.callOrFold()
                    self.endRoundEvent = 1
                elif self.street == 0 and self.game.pot == 2:
                    self.checkOrRaise()
                else:
                    self.callRaiseOrFold()

            if self.game.players[0].hasChecked and self.game.players[1].hasChecked:
                self.endRoundEvent = 1

            if self.game.players[0].didFold or self.game.players[1].didFold:
                self.endRoundEvent = 1

            if self.game.pot != 2.0:
                if self.game.players[0].hasCalled or self.game.players[1].hasCalled:
                    self.endRoundEvent = 1

        

def bet(roundObject, amount):
    roundObject.currentBet = amount
    roundObject.game.pot += roundObject.currentBet
    roundObject.game.players[roundObject.firstToAct % 2].playerLastBet = roundObject.currentBet
    roundObject.game.players[roundObject.firstToAct % 2].stack -= roundObject.currentBet
    roundObject.game.players[roundObject.firstToAct % 2].hasBet = True
    return None          