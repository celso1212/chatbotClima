import tkinter as tk
from tkinter import scrolledtext
from bot import initial_training
from utils import safe_chatbot_response, get_weather, export_to_json

bot = initial_training()

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")

        self.chat_display = scrolledtext.ScrolledText(root, width=40, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)

        self.input_label = tk.Label(root, text="Digite sua mensagem:")
        self.input_label.grid(row=1, column=0, padx=10, pady=5)

        self.input_entry = tk.Entry(root, width=30)
        self.input_entry.grid(row=1, column=1, padx=10, pady=5)

        self.send_button = tk.Button(root, text="Enviar", command=self.send_message)
        self.send_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.awaiting_city = False

    def send_message(self):
        message = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        if message:
            self.add_to_chat("Você: " + message)
            if message.lower() == 'sair':
                response = 'Bot: Tchau'
                self.add_to_chat(response)
                self.export_and_close()
            elif 'clima' in message.lower():
                self.awaiting_city = True
                response_clima = 'Bot: Para qual cidade você gostaria de saber o clima?'
                self.add_to_chat(response_clima)
            elif self.awaiting_city:
                response = 'Bot: ' + get_weather(message)
                self.add_to_chat(response)
                self.awaiting_city = False
            else:
                chatbot_response_text = safe_chatbot_response(bot, message)
                response = f'Bot: {chatbot_response_text}'
                self.add_to_chat(response)

    def export_and_close(self):
        export_to_json(bot, 'aprendizado.json')
        self.root.destroy()

    def add_to_chat(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
