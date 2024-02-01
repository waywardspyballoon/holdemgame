import os

class GameRound:
    def __init__(self, game, street, first, board):
        self.currentBet = 0
        self.game = game
        self.street = street
        self.firstToAct = first
        self.endRoundEvent = 0
        self.board = board

    def setup_action(self):
        if self.street == 0:
            if self.firstToAct % 2 == 0:
                self.firstToAct = 1
            else:
                self.firstToAct = 0
            
            bet(self, .5)
            bet(self, 1)

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
        os.system('cls')
        print(f'player {self.game.players[self.firstToAct % 2].name} \n\
              remaining stack {self.game.players[self.firstToAct % 2].stack}\
              size of pot {self.game.pot}')
        print('\n')

        if self.firstToAct % 2 == 1:
            oppstack = self.game.players[0].stack
        else:
            oppstack = self.game.players[1].stack

        round_info = ''
        round_info = str(oppstack) + '*' + \
        str(self.game.players[self.firstToAct % 2].stack) + '*' + str(self.game.pot) + '*' \
        + str(self.street) + '*' + str(self.currentBet) + '*'
        hand_rank = self.game.players[self.firstToAct % 2].board.initRank
        
                      
        print('Board : ', end = ' ')
        counter = 0
        for card in self.board:
            print(f'| {card} |', end = '')
            counter += 1
            if counter > 2:
                print('', end = '  ')

## representation
                
        str_to_send = ''
        for card in self.board:
            str_to_send += str(card.rank) + '*' + str(card.suit) + '*'
        self.game.netConn.connections[self.firstToAct % 2][0].send(f'{str_to_send}'.encode('ascii'))
        print(str_to_send)

## end block for representation

        print('\nHole Cards : ', end = '')

        for card in self.game.players[self.firstToAct % 2].board.holeCards.holecards:
            print(f'| {card} |', end = '')

        hole_cards_to_send = ''
        for card in self.game.players[self.firstToAct % 2].board.holeCards.holecards:
            hole_cards_to_send += str(card.rank) + '*' + str(card.suit) + '*'
        
        opponent_action = None
        if self.game.players[self.firstToAct % 2] == 1:
            opp = 0
        else:
            opp = 1
        
        self.game.netConn.connections[self.firstToAct % 2][0].send(f'{hole_cards_to_send}'.encode('ascii'))
        self.game.netConn.connections[self.firstToAct % 2][0].send(f'{round_info}'.encode('ascii'))
        self.game.netConn.connections[self.firstToAct % 2][0].send(f'{hand_rank}'.encode('ascii'))
        
        print(f'\n{self.game.players[self.firstToAct % 2].board.initRank}')
        
    
    def checkOrRaise(self):
        # action = input('\n[c]heck or [r]aise ')
        self.game.netConn.connections[self.firstToAct % 2][0].send('ISTURN'.encode('ascii'))
        self.print_action()
        print('\n[c]heck or [r]aise ')
        self.game.netConn.connections[self.firstToAct % 2][0].send('CR'.encode('ascii'))
        action = self.game.netConn.connections[self.firstToAct % 2][0].recv(1024).decode('ascii').lower()
        if action == 'c':
            self.game.players[self.firstToAct % 2].hasChecked = True
            self.firstToAct += 1
            return None
        
        if action == 'r':
            raiseBet(self)

    def checkOrBet(self):
        self.game.netConn.connections[self.firstToAct % 2][0].send('ISTURN'.encode('ascii'))
        self.print_action()
        self.game.netConn.connections[self.firstToAct % 2][0].send('CB'.encode('ascii'))
        print(f'\n[c]heck, [b]et (amount 0 - {self.game.players[self.firstToAct % 2].stack}\n')

        action = self.game.netConn.connections[self.firstToAct % 2][0].recv(1024).decode('ascii').lower()

        if action == 'c':

            self.game.players[self.firstToAct % 2].hasChecked = True
            self.firstToAct += 1
            return None

        if action == 'b':
            stack_size = self.game.players[self.firstToAct % 2].stack
            self.game.netConn.connections[self.firstToAct % 2][0].send(f'{stack_size}'.encode('ascii'))

            bet_val = self.game.netConn.connections[self.firstToAct % 2][0].recv(1024).decode('ascii')
            print('getting here')
            print('proceeding to bet...')
            bet_val = float(bet_val)
            bet(self, bet_val)
                
    def callRaiseOrFold(self):
        self.game.netConn.connections[self.firstToAct % 2][0].send('ISTURN'.encode('ascii'))
        self.print_action()
        self.game.netConn.connections[self.firstToAct % 2][0].send('CRF'.encode('ascii'))
        action = self.game.netConn.connections[self.firstToAct % 2][0].recv(1024).decode('ascii').lower()
        if self.street == 0 and self.game.pot == 2:
            self.checkOrRaise()

        
        print(f'\n[c]all (amount : {self.currentBet}, [r]aise, or [f]old \n')


        if not action:
            print('try again, empty field is not valid response')
            self.callRaiseOrFold()

        if action == 'f':
            self.game.players[self.firstToAct % 2].didFold = True
            return None
        
        if action == 'r':

            raiseBet(self)

        if action == 'c':

            if self.street == 0:
                if self.game.players[self.firstToAct % 2].playerLastBet == .5:
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
        self.game.netConn.connections[self.firstToAct % 2][0].send('ISTURN'.encode('ascii'))
        self.print_action()
        self.game.netConn.connections[self.firstToAct % 2][0].send('CF'.encode('ascii'))
        action = self.game.netConn.connections[self.firstToAct % 2][0].recv(1024).decode('ascii').lower()
        print(f'\n[c]all bet (bet amount : {self.currentBet} with remaining stack : \
                       {self.game.players[self.firstToAct % 2].stack}\n or [f]old?')


        if action == 'c':

            if self.game.players[self.firstToAct % 2].stack < self.currentBet:
                amount_to_replace = self.game.players[(self.firstToAct + 1) % 2].playerLastBet - (self.game.players[self.firstToAct % 2].playerLastBet + self.game.players[self.firstToAct % 2].stack)
                self.currentBet = self.game.players[self.firstToAct % 2].stack + self.game.players[self.firstToAct % 2].playerLastBet
                self.game.players[(self.firstToAct + 1) % 2].stack += amount_to_replace
                self.game.pot -= amount_to_replace

            self.betDifference = (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)
            self.game.players[self.firstToAct % 2].stack -= self.betDifference    
            self.game.pot += (self.currentBet - self.game.players[self.firstToAct % 2].playerLastBet)

            if self.game.players[self.firstToAct % 2].stack == 0:

                self.game.players[self.firstToAct % 2].isAllIn = True
            
            self.game.players[self.firstToAct % 2].hasCalled = True
            self.endRoundEvent = 1
            return None
        
        if action == 'f':
            self.game.players[self.firstToAct % 2].didFold = True
            return None
        

    def bettingAction(self):

        while not self.endRoundEvent:

            if self.game.players[0].hasChecked and self.game.players[1].hasCalled:
                break

            if self.game.players[1].hasChecked and self.game.players[0].hasCalled:
                break

            if self.game.players[0].isAllIn and self.game.players[1].isAllIn:
                break

            if not self.game.players[0].hasBet and not self.game.players[0].hasBet:
                for player in self.game.players:
                    if player.isAllIn:
                        return None
                self.checkOrBet()
           
            if self.currentBet:
                if self.game.players[0].isAllIn or self.game.players[1].isAllIn:
                    self.callOrFold()
                    if self.game.players[self.firstToAct % 2].hasCalled:
                        self.game.players[self.firstToAct % 2].isAllIn = True
                        break
                    elif self.game.players[self.firstToAct % 2].didFold == True:
                        break
                
                elif self.currentBet >= (self.game.players[self.firstToAct % 2].stack + \
                                            self.game.players[self.firstToAct % 2].playerLastBet):
                    self.callOrFold()
                    self.endRoundEvent = 1
                elif (self.game.players[self.firstToAct % 2].playerLastBet + self.game.players[self.firstToAct % 2].stack <= \
                      self.currentBet):
                    self.callOrFold()
                    if self.game.players[self.firstToAct % 2].didFold == True:
                        break
                elif self.street == 0 and self.game.pot == 2:
                    self.checkOrRaise()
                else:
                    self.callRaiseOrFold()
                    if self.game.players[self.firstToAct % 2].didFold == True:
                        break

            if self.game.players[0].hasChecked and self.game.players[1].hasChecked:
                self.endRoundEvent = 1

            if self.game.players[0].didFold or self.game.players[1].didFold:
                self.endRoundEvent = 1

            if self.game.pot != 2.0:
                if self.game.players[0].hasCalled or self.game.players[1].hasCalled:
                    self.endRoundEvent = 1

        

def bet(roundObject, amount = 0):

    def bettingLogic(amount):
        roundObject.currentBet = amount
        roundObject.game.pot += roundObject.currentBet
        roundObject.game.players[roundObject.firstToAct % 2].playerLastBet = roundObject.currentBet
        roundObject.game.players[roundObject.firstToAct % 2].stack -= roundObject.currentBet
        roundObject.game.players[roundObject.firstToAct % 2].hasBet = True
        if roundObject.game.players[roundObject.firstToAct % 2].stack == 0:
            roundObject.game.players[roundObject.firstToAct % 2].isAllIn = True

        roundObject.firstToAct += 1
        return None
    
    if amount > 0:
        bettingLogic(amount)
        return None
    
    if current == '':
        print('invalid selection, field cannot be blank')
        bet(roundObject)
        return None
    current = float(current)

    if current > roundObject.game.players[roundObject.firstToAct % 2].stack:
        print('invalid selection, value must be lower than or equal to stack size')
        current = 0
        bet(roundObject)
        return None

    elif current < 0:
        print('invalid selection, value must be greater than 0')
        current = 0    
        bet(roundObject)
        return None
    
    bettingLogic(current)
    return None
    

def raiseBet(roundObject):
    upperBound = int(roundObject.game.players[roundObject.firstToAct % 2].stack + roundObject.game.players[roundObject.firstToAct % 2].playerLastBet)
    range_for_bet = f'{roundObject.currentBet}*{upperBound}'
    roundObject.game.netConn.connections[roundObject.firstToAct % 2][0].send(f'{range_for_bet}'.encode('ascii'))

    new_value = roundObject.game.netConn.connections[roundObject.firstToAct % 2][0].recv(1024).decode('ascii')
    new_value = float(new_value)

    if new_value:
        roundObject.currentBet = new_value
        roundObject.betDifference = (roundObject.currentBet - roundObject.game.players[roundObject.firstToAct % 2].playerLastBet)
        roundObject.game.players[roundObject.firstToAct % 2].stack -= roundObject.betDifference
        roundObject.game.pot += roundObject.betDifference
        roundObject.game.players[roundObject.firstToAct % 2].hasBet = True
        roundObject.game.players[roundObject.firstToAct % 2].playerLastBet = roundObject.currentBet
        if roundObject.game.players[roundObject.firstToAct % 2].stack == 0:
            roundObject.game.players[roundObject.firstToAct % 2].isAllIn = True
        
        for player in roundObject.game.players:
            player.hasCalled = False

        roundObject.firstToAct += 1

    return None
