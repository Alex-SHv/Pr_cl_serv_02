import socket
import time

HOST = '127.0.0.1'
PORT = 4000

print("--- Клиент запущен и ищет сервер ---")

def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            return client
        except ConnectionRefusedError:
            print("Сервер пока спит... Пробую еще раз через 2 секунды.")
            time.sleep(2)
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            time.sleep(2)


while True:
    client = connect_to_server()
    print("\n[OK] Подключено к серверу!")

    try:
        message = input("Вы (Клиент): ")
        if message.lower() == 'exit':
            break

        client.send(message.encode('utf-8'))

        data = client.recv(1024).decode('utf-8')
        if not data:
            print("Сервер закрыл соединение.")
        else:
            print(f"Сервер ответил: {data}")

    except (ConnectionResetError, BrokenPipeError):
        print("\n[!] Связь с сервером потеряна. Снова перехожу в режим ожидания...")
    finally:
        client.close()