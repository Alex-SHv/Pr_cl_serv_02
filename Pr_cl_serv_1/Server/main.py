import socket
import sys

HOST = '127.0.0.1'
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("--- Сервер чата запущен ---")
print("Ожидание сообщений от клиента...")

try:
    while True:
        client_socket, address = server.accept()

        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"\n[Клиент {address}]: {data}")

                reply = input("Ваш ответ (Сервер): ")
                client_socket.send(reply.encode('utf-8'))

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            client_socket.close()

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server.close()
    sys.exit(0)