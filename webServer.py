from socket import *

import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    serverSocket.bind(("", port))

    serverSocket.listen(1)

    while True:
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024).decode()
            if not message:
                connectionSocket.close()
                continue

            filename = message.split()[1]
            path = filename.lstrip('/') or 'index.html'

            with open(path, 'rb') as f:
                body = f.read()

            header = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/html; charset=UTF-8\r\n"
                b"Server: PythonWebServer/1.0\r\n"
                b"Connection: close\r\n"
                + f"Content-Length: {len(body)}\r\n".encode()
                + b"\r\n"
            )

            connectionSocket.sendall(header + body)

        except FileNotFoundError:
            body = b"<html><body><h1>404 Not Found</h1></body></html>"
            header = (
                b"HTTP/1.1 404 Not Found\r\n"
                b"Content-Type: text/html; charset=UTF-8\r\n"
                b"Server: PythonWebServer/1.0\r\n"
                b"Connection: close\r\n"
                + f"Content-Length: {len(body)}\r\n".encode()
                + b"\r\n"
            )
            connectionSocket.sendall(header + body)

        except Exception:
            try:
                connectionSocket.shutdown(SHUT_RDWR)
            except Exception:
                pass

        finally:

            connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)