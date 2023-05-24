from holdemmain import *


if __name__ == "__main__":

    deckForGame = Deck()

    class Game:

        def __init__(self, players):
            self.players = []
            for player in players:
                self.players.append(player)
            self.pot = 0
    
    flop = (deckForGame.deck.pop(0),
            deckForGame.deck.pop(0),
            deckForGame.deck.pop(0))
    
    players = [Player(Board(flop, HoleCards(deckForGame))),
              Player(Board(flop, HoleCards(deckForGame)))]
            #   Player(Board(flop, HoleCards(deckForGame))),
            #   Player(Board(flop, HoleCards(deckForGame)))]


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
    
    x = input('Begin?')
    if x == 'n':
        exit()
    else:
        total_players = players[:]
        setupAndAnalyze(total_players)
    
    print(f'Preflop\n')
    for player in total_players:
        print(f'{player.board.holeCards.holecards[0]}, {player.board.holeCards.holecards[1]}')
    
    
    game = Game(total_players)
    start = GameRound(game, 0)
    start.setup_action()
    start.betting_action()

    # for player in total_players:
    #     print(player.board.initRank)

    # turn = deckForGame.deck.pop(0)
    # addstreet(turn, total_players)
    # setupAndAnalyze(total_players)

    # for player in total_players:
    #     print(player.board.initRank)
    
    # river = deckForGame.deck.pop(0)
    # addstreet(river, total_players)
    # setupAndAnalyze(total_players)

    # for player in total_players:
    #     print(player.board.initRank)
    

