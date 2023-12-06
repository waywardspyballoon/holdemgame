import socket
import struct

def send_message(client_socket, message):
    # Prefix the message with a 4-byte header indicating the message length
    header = struct.pack("!I", len(message))
    client_socket.sendall(header + message)

def receive_message(client_socket):
    # Receive the 4-byte header
    header = client_socket.recv(4)
    if not header:
        return None

    # Unpack the header to get the message length
    message_length = struct.unpack("!I", header)[0]

    # Receive the actual message based on the calculated length
    message = client_socket.recv(message_length)
    return message

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)

    print("Server listening on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        while True:
            # Receive a message from the client
            received_message = receive_message(client_socket)

            if received_message is None:
                print("Client disconnected.")
                break

            print(f"Received message from client: {received_message.decode('utf-8')}")

            # Send a response back to the client
            response = f"Server received: {received_message.decode('utf-8')}"
            send_message(client_socket, response)

        client_socket.close()

if __name__ == "__main__":
    main()
