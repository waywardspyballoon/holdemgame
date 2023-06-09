from holdemmain import *


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
    
    def mainGameLoop(firstToAct = 0, p1stack = 100, p2stack = 100):
        if p1stack == 0 or p2stack == 0:
            reload = input('[r]eload or [e]xit')
        x = input('Begin?')
        if x == 'n':
            exit()
        

        deckForGame = Deck()
        flop = (deckForGame.deck.pop(0),
                deckForGame.deck.pop(0),
                deckForGame.deck.pop(0)) 

        players = [Player(Board(flop, HoleCards(deckForGame))),
                Player(Board(flop, HoleCards(deckForGame)))]
        
        players[0].stack = p1stack
        players[1].stack = p2stack

        total_players = players[:]
        setupAndAnalyze(total_players)
        game = Game(total_players, deckForGame)
        start = GameRound(game, 0, firstToAct)
        start.setup_action()
        start.bettingAction()


        for player in total_players:
            print(player.board.initRank)
        
        print('dealing turn')

        turn = deckForGame.deck.pop(0)
        addstreet(turn, total_players)
        setupAndAnalyze(total_players)
    
        start = GameRound(game, 1, firstToAct)
        start.setup_action()
        start.bettingAction()

        print('dealing river')

        for player in total_players:
            print(player.board.initRank)

        river = deckForGame.deck.pop(0)
        addstreet(river, total_players)
        setupAndAnalyze(total_players)

        start = GameRound(game, 2, firstToAct)
        start.setup_action()
        start.bettingAction()

        for player in total_players:
            print(player.board.initRank)
        
        firstToAct += 1

        print(f'pot is {game.pot}')
        print('it is ovah')

        if players[0].board == players[1].board:

            print('tie! split pot!')

            for player in game.players:
                player.stack += (game.pot / 2)
            
        elif players[0].board > players[1].board:
            print('player 0 wins!')

            players[0].stack += game.pot
        
        else:
            print('player 1 wins!')
            players[1].stack += game.pot

        p1stack = players[0].stack
        p2stack = players[1].stack
        
        mainGameLoop(firstToAct, p1stack, p2stack)

    mainGameLoop()
        

