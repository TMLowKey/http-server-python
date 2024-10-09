import socket
import threading


def handle_client(client: socket.socket):
    data: str = client.recv(1024).decode()
    request_data: list[str] = data.split("\r\n")


    if not data:
        print("Data is missing")
        client.close()
        return

    path: str = request_data[0].split(" ")[1]

    # DEBUG
    #print(request_data)

    if path == "/":
        response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif path.startswith("/echo/"):
        value = request_data[0].split(" ")[1].partition("/echo/")[2]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
    elif path.startswith("/user-agent"):
        user_agent = request_data[3].split(": ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    client.send(response)
    client.close()

def main():
        print("Server is running")

        # Create server
        server_socket: socket.socket = socket.create_server(
            ("localhost", 4221), reuse_port=True
        )

        while True:
            # Create client handler
            client: socket.socket
            client, addr = server_socket.accept()

            client_thread = threading.Thread(target=handle_client(client), args=(client,))
            client_thread.start()

if __name__ == "__main__":
    main()
