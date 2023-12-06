import socket
import struct

def send_message(server_socket, message):
    # Prefix the message with a 4-byte header indicating the message length
    header = struct.pack("!I", len(message))
    server_socket.sendall(header + message)

def receive_message(server_socket):
    # Receive the 4-byte header
    header = server_socket.recv(4)
    if not header:
        return None

    # Unpack the header to get the message length
    message_length = struct.unpack("!I", header)[0]

    # Receive the actual message based on the calculated length
    message = server_socket.recv(message_length)
    return message.decode("utf-8")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))

    while True:
        # Get user input and encode as bytes
        message = input("Enter a message (or 'exit' to quit): ").encode("utf-8")

        if message.lower() == b'exit':
            break

        # Send the message to the server
        send_message(client_socket, message)

        # Receive and print the server's response
        response = receive_message(client_socket)
        print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    main()
