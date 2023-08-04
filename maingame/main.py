from holdemmain import *
import time
import os


if __name__ == "__main__":

    class Game:

        def __init__(self, players, deck):
            self.players = []
            for player in players:
                self.players.append(player)
            self.pot = 0
            self.deckForGame = deck

    def setupAndAnalyze(total_players):
        for player in total_players:
            player.board.createSortable()
            player.board.getRank()
            player.board.storeFiveCardHand()
        return None

    def addstreet(street, total_players):
        for player in total_players:
            player.board.add(street)
        return None
    
    def mainGameLoop(firstToAct = 0, p1stack = 100, p2stack = 100, p1name = 0, p2name = 0):
        if p1stack == 0 or p2stack == 0:
            reload = input('[r]eload or [e]xit')
            if reload == 'r':
                if not p1stack:
                    p1stack = 100
                else:
                    p2stack = 100


        deckForGame = Deck()
        flop = (deckForGame.deck.pop(0),
                deckForGame.deck.pop(0),
                deckForGame.deck.pop(0)) 

        players = [Player(Board(flop, HoleCards(deckForGame))),
                Player(Board(flop, HoleCards(deckForGame)))]
        
        
        players[0].stack = p1stack
        players[1].stack = p2stack

        if not p1name:
            p1name = input('Select player 1 name : ')
        players[0].name = p1name
        if not p2name:
            p2name = input('Select player 2 name : ')
        players[1].name = p2name


        BOARD = [card for card in flop]

        total_players = players[:]
        setupAndAnalyze(total_players)
        game = Game(total_players, deckForGame)
        start = GameRound(game, 0, firstToAct, BOARD)
        start.setup_action()
        start.bettingAction()
        
        print('dealing turn')

        turn = deckForGame.deck.pop(0)

        BOARD.append(turn)

        
        addstreet(turn, total_players)
        setupAndAnalyze(total_players)

        if players[0].didFold == False and players[1].didFold == False:
    
            start = GameRound(game, 1, firstToAct, BOARD)
            start.setup_action()
            start.bettingAction()

        print('dealing river')
        river = deckForGame.deck.pop(0)

        BOARD.append(river)

        addstreet(river, total_players)
        setupAndAnalyze(total_players)

        if players[0].didFold == False and players[1].didFold == False:

            start = GameRound(game, 2, firstToAct, BOARD)
            start.setup_action()
            start.bettingAction()


        firstToAct += 1

        print(f'pot is {game.pot}')
        for player in total_players:
            print(player.board.initRank)
        

        if players[0].didFold == True or players[1].didFold == True:
            if players[0].didFold:
                players[1].stack += game.pot
                p1stack = players[0].stack
                p2stack = players[1].stack
                print('pot awarded to player 1, player 0 folded!')
                time.sleep(5)
                mainGameLoop(firstToAct, p1stack, p2stack, p1name, p2name)
                return None
            players[0].stack += game.pot
            p1stack = players[0].stack
            p2stack = players[1].stack
            print('pot awarded to player 0, player 1 folded!')
            time.sleep(5)
            mainGameLoop(firstToAct, p1stack, p2stack, p1name, p2name)
            return None
                

        if players[0].board == players[1].board:

            print('tie! split pot!')

            for player in game.players:
                player.stack += (game.pot / 2)
            
        elif players[0].board > players[1].board:
            print(f'{players[0].name} wins!')

            players[0].stack += game.pot
        
        else:
            print(f'{players[1].name} wins!')
            players[1].stack += game.pot


        p1stack = players[0].stack
        p2stack = players[1].stack

        time.sleep(5)
        
        mainGameLoop(firstToAct, p1stack, p2stack, p1name, p2name)

    mainGameLoop()
        

