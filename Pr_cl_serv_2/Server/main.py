import socket
import threading
import logging
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 4000

print("--- Сервер чата запущен ---")
print("Ожидание сообщений от клиента...")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename="server_history.log",
    filemode='a',
    encoding='utf-8'
)

server = None
current_conn = None
current_addr = None
is_running = False


def log_to_gui_and_file(msg, level="info"):
    log_area.insert(tk.END, msg + "\n")
    log_area.yview(tk.END)
    if level == "info":
        logging.info(msg)
    else:
        logging.error(msg)


def listen_for_clients():
    global server, current_conn, current_addr, is_running

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        is_running = True

        log_to_gui_and_file("--- Сервер запущен и ждет сообщения ---")

        while is_running:
            try:
                conn, addr = server.accept()
                current_conn = conn
                current_addr = addr

                data = conn.recv(1024).decode('utf-8')
                if data:
                    msg = f"Запрос от {addr}: '{data}'"
                    log_to_gui_and_file(msg)
            except socket.error:
                break
    except Exception as e:
        if is_running:
            log_to_gui_and_file(f"Критическая ошибка: {e}", "error")


def stop_server():
    global server, is_running, current_conn
    is_running = False
    if current_conn:
        current_conn.close()
    if server:
        server.close()

    try:
        logging.info("Сервер остановлен пользователем.")
    except:
        pass

    root.destroy()


def send_reply():
    global current_conn, current_addr
    if current_conn:
        reply = entry_reply.get()
        if reply:
            try:
                current_conn.send(reply.encode('utf-8'))
                log_to_gui_and_file(f"Ответ для {current_addr}: {reply}")

                entry_reply.delete(0, tk.END)
                current_conn.close()
                current_conn = None
            except Exception as e:
                log_to_gui_and_file(f"Ошибка при отправке: {e}", "error")
    else:
        log_area.insert(tk.END, "[!] Нет активного клиента для ответа\n")


root = tk.Tk()
root.title("Сервер")
root.geometry("450x550")

root.protocol("WM_DELETE_WINDOW", stop_server)

tk.Label(root, text="История (пишется также в server_history.log):").pack(pady=5)
log_area = scrolledtext.ScrolledText(root, width=50, height=15)
log_area.pack(padx=10, pady=5)

tk.Label(root, text="Ваш ответ (Сервер):").pack(pady=5)
entry_reply = tk.Entry(root, width=40)
entry_reply.pack(padx=10, pady=5)
entry_reply.bind("<Return>", lambda e: send_reply())

btn_reply = tk.Button(root, text="Отправить ответ", command=send_reply, bg="#ccffcc")
btn_reply.pack(pady=5)

btn_stop = tk.Button(root, text="Остановить сервер и выйти", command=stop_server, bg="#ffcccc")
btn_stop.pack(pady=10)

threading.Thread(target=listen_for_clients, daemon=True).start()

root.mainloop()