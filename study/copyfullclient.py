import os
import socket
from time import sleep


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

    def active_turn_representation(self, option):
        def CR():
            selection = input('[c]heck or [r]aise? : ')
            if selection.lower() == 'c':
                self.send('C')
            elif selection.lower == 'r':
                self.send('R')
            else:
                print('invalid selection')
                CR()
        def CB():
            pass
        def CRF():
            pass
        def CF():
            pass

        if option == 'CR':
            return CR()
                            
    def recv(self):
        while 1:
            try:
                data = self.socket.recv(1024).decode('ascii')
                if data == 'ISTURN':
                    option = self.socket.recv(1024).decode('ascii')
                    action = self.active_turn_representation(option)
            except:
                print('something went wrong')
                break

    def print_current_gamestate_on_turn(self):
        print('board, cards, pot...')
                
    def send(self, message):
        self.socket.send(f'{message}'.encode('ascii'))

    def select_name(self):
        return input('select name : ')

cl = Client('127.0.0.1', 1235)
cl.connect()
cl.recv()



        
    
