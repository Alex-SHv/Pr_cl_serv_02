import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 4000

print("--- Клиент запущен и ищет сервер ---")

def send_message():
    message = entry_msg.get()
    if not message:
        return

    if message.lower() == 'exit':
        window.destroy()
        return

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        client.send(message.encode('utf-8'))
        log_area.insert(tk.END, f"Вы: {message}\n")
        entry_msg.delete(0, tk.END)

        data = client.recv(1024).decode('utf-8')
        if data:
            log_area.insert(tk.END, f"Сервер ответил: {data}\n")

        client.close()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Связь потеряна или сервер спит...\n{e}")


window = tk.Tk()
window.title("Клиент")
window.geometry("400x450")

tk.Label(window, text="Лог общения:").pack(pady=5)
log_area = scrolledtext.ScrolledText(window, width=45, height=15)
log_area.pack(pady=5)

tk.Label(window, text="Введите сообщение (или 'exit' для выхода):").pack(pady=2)
entry_msg = tk.Entry(window, width=40)
entry_msg.pack(pady=5)
entry_msg.bind("<Return>", lambda e: send_message())

btn_send = tk.Button(window, text="Отправить", command=send_message, bg="lightblue", width=20)
btn_send.pack(pady=5)

btn_exit = tk.Button(window, text="Выход (exit)", command=window.destroy, bg="#ffcccc", width=20)
btn_exit.pack(pady=5)

window.mainloop()
