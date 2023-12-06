from holdemmain import *
import time
import os
import socket
import threading


if __name__ == "__main__":

    # class NetworkServerThread(threading.Thread):
    #     def __init__(self):
    #         threading.Thread.__init__(self)
    #         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.threads = []
        
    #     def run(self):
    #         self.socket.bind(('127.0.0.1', 1235))
    #         self.socket.listen(2)
    #         while len(self.threads) < 2:
    #             new_conn = Thread(target = self.new_thread())
    #             print(f'connected')
    #             self.threads.append(new_conn)
            
    #     def new_thread(self):
    #         self.socket.accept()

    class NetworkServer:

        def __init__(self):
            self.connections = []
            self.baseport = 1235
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('127.0.0.1', self.baseport))
            self.socket.listen(2)
        
        def run(self):
            print(f'waiting for 2 players...')
            while len(self.connections) < 2:
                conn, addr = self.socket.accept()
                self.connections.append((conn, addr))
                print(f'connected to {conn}{addr}')
                if len(self.connections) == 1:
                    self.connections[0][0].send(b'0')
                else:
                    self.connections[1][0].send(b'1')

    class Game:

        def __init__(self, players, deck, netConn):
            self.players = []
            for player in players:
                self.players.append(player)
            self.pot = 0
            self.deckForGame = deck
            self.netConn = netConn

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
            elif reload == 'e':
                exit()
            else:
                print('invalid response, exiting')
                exit()
        # netConn = NetworkServerThread()
        # netConn.start()
        # netConn.join()

        deckForGame = Deck()
        flop = (deckForGame.deck.pop(0),
                deckForGame.deck.pop(0),
                deckForGame.deck.pop(0))

        send_first_flop = str(flop[0]) 
        print(send_first_flop)
        players = [Player(Board(flop, HoleCards(deckForGame))),
                Player(Board(flop, HoleCards(deckForGame)))]
    
        
        
        players[0].stack = p1stack
        players[1].stack = p2stack

        if not p1name:
            print('getting here')
            p1name = netConn.connections[0][0].recv(1024).decode('ascii')
            print(p1name)
        players[0].name = p1name
        if not p2name:
            p2name = netConn.connections[1][0].recv(1024).decode('ascii')
            print(p2name)
        players[1].name = p2name


        BOARD = [card for card in flop]

        total_players = players[:]
        setupAndAnalyze(total_players)
        game = Game(total_players, deckForGame, netConn)
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
        print('Board : ', end = ' ')
        counter = 0
        for card in BOARD:
            print(f'| {card} |', end = '')
            counter += 1
            if counter > 2:
                print('', end = '  ')

        for player in total_players:
            print('')
            print(f'\nHole Cards for {player.name}: ', end = '')

            for card in player.board.holeCards.holecards:
                print(f'| {card} |', end = '')
            print('')
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
            print(f'\n{players[1].name} wins!')
            players[1].stack += game.pot


        p1stack = players[0].stack
        p2stack = players[1].stack

        time.sleep(5)
        
        mainGameLoop(firstToAct, p1stack, p2stack, p1name, p2name)

    netConn = NetworkServer()
    netConn.run()
    mainGameLoop()
        