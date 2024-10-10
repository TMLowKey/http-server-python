import socket
import threading
import sys
import os


def handle_client(client: socket.socket):
    data: str = client.recv(1024).decode()
    request_data: list[str] = data.split("\r\n")


    if not data:
        print("Data is missing")
        client.close()
        return

    type: str = request_data[0].split(" ")[0]
    path: str = request_data[0].split(" ")[1]

    body: str = request_data[7]

    # DEBUG
    print(request_data)

    if path == "/":
        response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif path.startswith("/echo/"):
        value = request_data[0].split(" ")[1].partition("/echo/")[2]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
    elif path.startswith("/user-agent"):
        user_agent = request_data[3].split(": ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
    elif path.startswith("/files"):
        directory = sys.argv[2]
        # DEBUG
        #print(f"Requested: {directory} {filename}")
        if type == "GET":
            filename = path[7:]
            try:
                with open(f"./{directory}/{filename}", "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            except Exception as e:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
        if type == "POST":
            filename = path[6:]
            print(filename)
            #try:
            with open(f"./files/{filename}", "w") as f:
                f.write(body)
            response = f"HTTP/1.1 201 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            #except Exception as e:
            #    response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

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
