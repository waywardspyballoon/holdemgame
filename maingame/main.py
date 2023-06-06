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
    
    def mainGameLoop(firstToAct = 0):
        x = input('Begin?')
        if x == 'n':
            exit()
       
        deckForGame = Deck()
        flop = (deckForGame.deck.pop(0),
                deckForGame.deck.pop(0),
                deckForGame.deck.pop(0)) 
        players = [Player(Board(flop, HoleCards(deckForGame))),
                   Player(Board(flop, HoleCards(deckForGame)))]
        total_players = players[:]
        setupAndAnalyze(total_players)
        game = Game(total_players, deckForGame)
        start = GameRound(game, 0, firstToAct)
        start.setup_action()
        start.bettingAction()

        for player in total_players:
            print(player.board.initRank)

        turn = deckForGame.deck.pop(0)
        addstreet(turn, total_players)
        setupAndAnalyze(total_players)
    
        print(total_players[0].isAllIn, total_players[0].isAllIn)

        start = GameRound(game, 1, firstToAct)
        start.setup_action()
        start.bettingAction()

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
        
        mainGameLoop(firstToAct)
    
    mainGameLoop()
        

