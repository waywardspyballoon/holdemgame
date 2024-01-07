import os
import socket
from time import sleep

suits = {1: '♣', 2: '♦', 3: '♥',
         4: '♠'}

singrank = {1: "Deuce", 2: "Three", 3: "Four",
            4: "Five", 5: "Six", 6: "Seven",
            7: "Eight", 8: "Nine", 9: "Ten",
            10: "Jack", 11: "Queen", 12: "King",
            13: "Ace"}


class Client:

    def __init__(self, servip, servport):
        
        self.name = None
        self.id = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (servip, servport)
        
    
    def connect(self):
        self.name = self.select_name()
        ret = self.socket.connect_ex((self.address))
        if ret != 0:
            print(f'connection error')
            return
        print(f'connected')
        self.id = cl.id = cl.socket.recv(1024)
        self.send(self.name)

    def raise_func(self, current_bet, upper_bound):
        current_bet = float(current_bet)
        upper_bound = float(upper_bound)
        print(current_bet, upper_bound)
        print(f'choose size between {current_bet} and {upper_bound}')
        while 1:
            raise_size = float(input())
            if raise_size > upper_bound:
                print('invalid selection, value must be lower than or equal to stack size')
                continue
            elif raise_size < 0:
                print('invalid selection, value must be greater than 0')
                continue
            elif raise_size <= current_bet:
                print('invalid selection, value must exceed current raise size')
                continue
            else:
                break
        return raise_size

    def bet_func(self, stack_size):
        
        stack_size = float(stack_size)
        while True:
            current = input('choose value')
            if current == '':
                print('input cannot be empty')
                continue
            
            current = float(current)
            
            if current > stack_size:
                print('val too large')
                continue

            if current < 0:
                print('bet must be larger than 0')
                continue

            else:
                break
        
        return current

    def fold_function(self):
        round_info = self.socket.recv(1024).decode('ascii').split('*')
        round_info.pop()
        opp_name, pot_size = round_info
        print(f'{opp_name} has folded, you win pot! ({pot_size})')

    def reload_func(self):
        print(f'[r]eload? or [e]xit')
        while 1:
                
            action = input()
            if action.lower() == 'r':
                self.send(action)
                break
            elif action.lower() == 'e':
                exit()
            else:
                print('invalid selection')

    def round_end(self):
        round_end_str = self.socket.recv(1024).decode('ascii')
        print(f'{round_end_str}')
        round_end_str = round_end_str.split('*')
        board = round_end_str[:10]
        hole_cards = round_end_str[10:14]
        hole_cards_2 = round_end_str[15:19]
        hand_rank_1 = round_end_str[20]
        hand_rank_2 = round_end_str[21]
        winner = round_end_str[22]
        round_info = '10*10*10*'
        round_info = round_info.split('*')
        print(f'{winner}')
        print(f'{board}')
        print(f'{hole_cards} , {hole_cards_2}')
        print(f'{hand_rank_1} , {hand_rank_2}')
        

        self.print_current_gamestate_on_turn(board, \
                                             hole_cards, hand_rank_1, round_info,\
                                             hole_cards_2, hand_rank_2, winner)


    def active_turn_representation(self, option):
        def CR():
            selection = input('[c]heck or [r]aise? : ')
            if selection.lower() == 'c':
                self.send('C')
                return
            if selection.lower() == 'r':
                self.send('R')
                raise_info = self.socket.recv(1024).decode('ascii').split('*')
                raise_transmit = self.raise_func(raise_info[0], raise_info[1])
                self.send(raise_transmit)
                return
                
            else:
                print('invalid selection')
                CR()
        def CB():
            selection = input('[c]heck or [b]et? : ')
            if selection.lower() == 'c':
                self.send('C')
                return
            if selection.lower() == 'b':
                self.send('B')
                bet_info = self.socket.recv(1024).decode('ascii')
                print('before function')
                bet_transmit = self.bet_func(bet_info)
                print('after function')
                self.socket.send(f'{bet_transmit}'.encode('ascii'))
                return
            else:
                print('invalid selection')
                CB()
            
        def CRF():
            
##            call_info = self.socket.recv(1024).decode('ascii').split('*')
##            call_info = str(call_info)
            print(f'[c]all, [r]aise, or [f]old?')
            selection = input()
            if selection.lower() == 'c':
                self.send('C')
                return
            if selection.lower() == 'r':
                self.send('R')
                raise_info = self.socket.recv(1024).decode('ascii').split('*')
                raise_transmit = self.raise_func(raise_info[0], raise_info[1])
                self.send(raise_transmit)
                return
            if selection.lower() == 'f':
                self.send('F')
                return
            else:
                print('invalid selection')
                CRF()
                        
        def CF():
            selection = input('[c]all or [f]old?')
            if selection.lower() == 'c':
                self.send('C')
                return
            if selection.lower() == 'f':
                self.send('F')
                return
            else:
                print('invalid selection')
                CF()
                

        if option == 'CR':
            return CR()
        if option == 'CB':
            return CB()
        if option == 'CRF':
            return CRF()
        if option == 'CF':
            return CF()
                            
    def recv(self):
        while 1:
            try:
                data = self.socket.recv(1024).decode('ascii')
                if data == 'ISTURN':
                    representation = self.socket.recv(1024).decode('ascii')
                    hole_cards = self.socket.recv(1024).decode('ascii')
                    round_info = self.socket.recv(1024).decode('ascii')
                    hand_rank = self.socket.recv(1024).decode('ascii')
                    representation = representation.split('*')
                    hole_cards = hole_cards.split('*')
                    round_info = round_info.split('*')
                    representation.pop()
                    hole_cards.pop()
                    self.print_current_gamestate_on_turn(representation, hole_cards, \
                                                         hand_rank, round_info)
                    option = self.socket.recv(1024).decode('ascii')
                    action = self.active_turn_representation(option)
                elif data == 'ROUNDEND':
                    print('round end')
                    self.round_end()
                elif data == 'OPPFOLD':
                    self.fold_function()
                elif data == 'RELOAD':
                    self.reload_func()
            except:
                print('something went wrong')
                break

    def print_current_gamestate_on_turn(self, representation, hole_cards, \
                                        hand_rank, round_info = None, hole_cards2 = None, \
                                        hand_rank2 = None, winner = None):
        print('progressing this far')
        hand_rank = str(hand_rank)
        round_info.pop()
        print(round_info)
        os.system('cls')
        representation = [int(item) for item in representation]
        hole_cards = [int(item) for item in hole_cards]
        if hole_cards2:
            hole_cards2 = [int(item) for item in hole_cards2]
        board = ''
        print(f'stack size: {round_info[1]} \n opponent stack: {round_info[0]} \
                \n total pot: {round_info[2]}')
        for _ , item in enumerate(representation):

            if _ % 2 == 0:
                board = board + '| ' + singrank[item + 1]
            
            else:
                board = board + suits[item + 1] + ' |'

        print(board)

        
        def hole_card_string(hole_cards):
            hole_card_str = ''

            for _ , item in enumerate(hole_cards):

                if _ % 2 == 0:
                    hole_card_str = hole_card_str + '| ' + singrank[item + 1]
                else:
                    hole_card_str = hole_card_str + suits[item + 1] + ' |'

            return hole_card_str

        print(f'\n{hole_card_string(hole_cards)}', end = '')
        if hole_cards2:
            print(f'  {hole_card_string(hole_cards2)}')
        print(f'\n {self.name} : {hand_rank}', end = '')
        if hand_rank2:
            print(f'   opponent : {hand_rank2}')

        if winner:
            print(f'\n {winner} wins pot, {round_info[2]}')

        print('')

                
                
    def send(self, message):
        self.socket.send(f'{message}'.encode('ascii'))

    def select_name(self):
        return input('select name : ')

cl = Client('127.0.0.1', 1235)
cl.connect()
cl.recv()
