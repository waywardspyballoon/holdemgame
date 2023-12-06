import socket
import threading
import random

# Function to handle a single client
def handle_client(client_socket, player_id):
    # Send a welcome message to the client
    client_socket.send("Welcome to the card game!".encode('utf-8'))

    # Example game logic: Shuffle and deal cards
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    # Deal two cards to each player
    player_cards = [deck.pop(), deck.pop()]
    client_socket.send(f"Your cards: {', '.join(player_cards)}".encode('utf-8'))

    # Main game loop
    while True:
        # Wait for the player's move (drawing a card)
        client_socket.send("Your move: (type 'draw' to draw a card)".encode('utf-8'))
        move = client_socket.recv(1024).decode('utf-8')

        if move.lower() == 'draw':
            # Draw a card and update player's hand
            drawn_card = deck.pop()
            player_cards.append(drawn_card)
            
            # Display the player's move on the server
            print(f"Player {player_id} drew: {drawn_card}")

            # Send messages to the client
            client_socket.send(f"You drew: {drawn_card}. Your hand: {', '.join(player_cards)}".encode('utf-8'))
            total_value = sum([int(card) if card.isdigit() else 10 for card in player_cards])
            client_socket.send(f"Total value of your hand: {total_value}".encode('utf-8'))

            # Example: Check for game end condition (e.g., total value exceeds a certain limit)
            if total_value >= 21:
                client_socket.send("Game over! You busted.".encode('utf-8'))
                break
        else:
            client_socket.send("Invalid move. Type 'draw' to draw a card.".encode('utf-8'))

    # Close the connection when the game is over
    print(f"Player {player_id} disconnected.")
    client_socket.close()

# Function to start the server
def start_server():
    # Set up the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Use your desired host and port
    server.listen(2)  # Maximum 2 connections (for 2 players)

    print("Server listening for incoming connections...")

    player_id = 1

    # Accept connections and start a new thread for each client
    while True:
        client_socket, addr = server.accept()
        print(f"Player {player_id} connected from {addr}")
        
        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, player_id))
        client_handler.start()

        # Increment player ID for the next client
        player_id += 1

# Start the server
start_server()
