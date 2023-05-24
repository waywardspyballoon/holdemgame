class GameRound:
    def __init__(self, game, street):
        self.currentBet = 0
        self.game = game
        self.street = street
        self.firstToAct = 0
        self.endRoundEvent = 0
        self.activePlayer = 0

    def setup_action(self):
        if self.street == 0:
            if self.firstToAct == 0:
                self.firstToAct = 1
            else:
                self.firstToAct = 0
            self.game.pot += 1.5
        
    # def increment_position(self):
    #     for player in self.players:
    #         if player.position == len(self.players) - 1:
    #             player.position = 0
    #         else:
    #             player.position += 1

    def betting_action(self):

        count = self.firstToAct
        while not self.endRoundEvent:
            action = input('[c]heck, [b]et (amount)')
            if action == 'c':
                self.game.players[count % 2].hasChecked = True
                count += 1
        
            if self.game.players[0].hasChecked and self.game.players[1].hasChecked:
                self.endRoundEvent = 1
        
        print('it is ovah')
        

    




    


        