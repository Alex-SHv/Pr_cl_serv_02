import socket

HOST = '127.0.0.1'
PORT = 4000

print("--- Чат-клиент запущен ---")
print("Введите 'exit' для выхода")

while True:
    message = input("Вы (Клиент): ")

    if message.lower() == 'exit':
        break

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        client.send(message.encode('utf-8'))

        data = client.recv(1024).decode('utf-8')
        if not data:
            print("Сервер разорвал соединение.")
            break
        print(f"Сервер ответил: {data}")

    except ConnectionRefusedError:
        print("Ошибка: Сервер не найден.")
        break
    finally:
        client.close()

print("Работа завершена.")