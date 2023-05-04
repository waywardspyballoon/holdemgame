from holdemmain import *



if __name__ == "__main__":

    deckForGame = Deck()

    class Game:

        def __init__(self, players):
            self.players = []
            for player in players:
                self.players.append(player)
            self.dealerPos = 0

        def init_preflop(self):
            Preflop(self)
    
    class Preflop:
        pass

    class Flop:
        pass

    class Turn:
        pass

    class River:
        pass


    flop = (deckForGame.deck.pop(0),
            deckForGame.deck.pop(0),
            deckForGame.deck.pop(0))
    
    players = [Player(Board(flop, HoleCards(deckForGame))),
              Player(Board(flop, HoleCards(deckForGame))),
              Player(Board(flop, HoleCards(deckForGame))),
              Player(Board(flop, HoleCards(deckForGame)))]


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
    
    x = input('How many players? (2-4)')
    x = int(x)
    if x > 4 or x < 2:
        print('must be between 2 and 4')
    else:
        total_players = players[0:x]
        setupAndAnalyze(total_players)

    # gameRound = GameRound(total_players)
    # gameRound.setup_action()
    # for player in total_players:
    #     print(player.position)
    # gameRound.increment_position()
    # print(f'\n')
    # for player in total_players:
    #     print(player.position)
    # gameRound.increment_position()
    # print(f'\n')
    # for player in total_players:
    #     print(player.position)
    # print(f'\n') 
    # gameRound.remove_player(gameRound.players[0])
    # for player in total_players:
    #     print(player.position)
    
    
    print(f'Preflop\n')
    for player in total_players:
        print(f'{player.board.holeCards.holecards[0]}, {player.board.holeCards.holecards[1]}')

    for player in total_players:
        print(player.board.initRank)

    turn = deckForGame.deck.pop(0)
    addstreet(turn, total_players)
    setupAndAnalyze(total_players)

    for player in total_players:
        print(player.board.initRank)

