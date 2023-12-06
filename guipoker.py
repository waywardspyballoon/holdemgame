import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class PokerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("No-Limit Texas Hold'em")
        
        self.load_card_images()
        
        self.player1_money = 1000
        self.player2_money = 1000
        
        self.player1_label = tk.Label(root, text="Player 1: $1000")
        self.player2_label = tk.Label(root, text="Player 2: $1000")
        
        self.player1_label.pack()
        self.player2_label.pack()
        
        self.pot_label = tk.Label(root, text="Pot: $0")
        self.pot_label.pack()
        
        self.table_frame = tk.Frame(root)
        self.table_frame.pack()
        
        self.flop_label = tk.Label(self.table_frame, text="Flop:")
        self.flop_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.turn_label = tk.Label(self.table_frame, text="Turn:")
        self.turn_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.river_label = tk.Label(self.table_frame, text="River:")
        self.river_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.card_images = []
        self.load_card_images()
        
        self.flop_images = [None, None, None]
        self.turn_image = None
        self.river_image = None
        
        self.player1_hole_images = [None, None]
        self.player2_hole_images = [None, None]
        
        self.player1_cards_label = tk.Label(root)
        self.player2_cards_label = tk.Label(root)
        
        self.player1_cards_label.pack()
        self.player2_cards_label.pack()
        
        self.bet_button = tk.Button(root, text="Bet", command=self.bet)
        self.bet_button.pack()
        
        self.fold_button = tk.Button(root, text="Fold", command=self.fold)
        self.fold_button.pack()
        
        self.quit_button = tk.Button(root, text="Quit", command=self.root.quit)
        self.quit_button.pack()
        
        self.current_player = 1
        self.pot = 0
        self.current_bet = 0
        
    def load_card_images(self):
        self.card_images = []
        suits = ['C', 'D', 'H', 'S']
        for suit in suits:
            for rank in range(1, 14):
                image_path = os.path.join('cards', f'{rank}{suit}.png')
                image = Image.open(image_path)
                image = ImageTk.PhotoImage(image)
                self.card_images.append(image)
        
    def display_card(self, label, card):
        if card is None:
            label.config(image=None)
        else:
            label.config(image=self.card_images[card])
        
    def bet(self):
        bet_amount = int(input("Enter your bet amount: "))  # Get the bet amount from user
        if self.current_player == 1:
            if bet_amount <= self.player1_money:
                self.player1_money -= bet_amount
                self.pot += bet_amount
                self.current_bet = bet_amount
                self.player1_label.config(text=f"Player 1: ${self.player1_money}")
            else:
                messagebox.showinfo("Error", "Not enough money to bet!")
                return
        else:
            if bet_amount <= self.player2_money:
                self.player2_money -= bet_amount
                self.pot += bet_amount
                self.current_bet = bet_amount
                self.player2_label.config(text=f"Player 2: ${self.player2_money}")
            else:
                messagebox.showinfo("Error", "Not enough money to bet!")
                return
        
        self.pot_label.config(text=f"Pot: ${self.pot}")
        self.current_player = 3 - self.current_player  # Switch player turn
        
    def fold(self):
        winner = 1 if self.current_player == 2 else 2
        self.pot += self.current_bet
        self.pot_label.config(text=f"Pot: ${self.pot}")
        
        messagebox.showinfo("Fold", f"Player {self.current_player} folds. Player {winner} wins ${self.pot}!")
        
        self.player1_money += self.pot
        self.player2_money += self.pot
        self.player1_label.config(text=f"Player 1: ${self.player1_money}")
        self.player2_label.config(text=f"Player 2: ${self.player2_money}")
        
        self.pot = 0
        self.pot_label.config(text="Pot: $0")
        self.current_bet = 0
        
        self.current_player = 1
    
    def set_community_cards(self, flop, turn, river):
        for i, card in enumerate(flop):
            self.display_card(self.flop_label, card, i)
        self.display_card(self.turn_label, turn)
        self.display_card(self.river_label, river)
    
    def set_player1_hole_cards(self, cards):
        for i, card in enumerate(cards):
            self.display_card(self.player1_cards_label, card, i)
    
    def set_player2_hole_cards(self, cards):
        for i, card in enumerate(cards):
            self.display_card(self.player2_cards_label, card, i)

def main():
    root = tk.Tk()
    game = PokerGame(root)
    
    # Replace these lists with actual card indices
    flop = [0, 1, 2]
    turn = 3
    river = 4
    player1_hole_cards = [5, 6]
    player2_hole_cards = [7, 8]
    
    game.set_community_cards(flop, turn, river)
    game.set_player1_hole_cards(player1_hole_cards)
    game.set_player2_hole_cards(player2_hole_cards)
    
    root.mainloop()

if __name__ == "__main__":
    main()
