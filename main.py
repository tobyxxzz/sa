import os
from flask import Flask
from threading import Thread
from bot_staff import bot_staff

app = Flask('')

@app.route('/')
def home():
    return "Bot Staff online 😎"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask, daemon=True)
    t.start()

def run_bot_thread(bot_instance, token):
    try:
        bot_instance.run(token)
    except Exception as e:
        print(f"Erro ao rodar bot: {e}")

def main():
    token_staff = os.getenv('DISCORD_STAFF_BOT_TOKEN')
    
    if not token_staff:
        print("ERRO: Token do Bot de Staff não encontrado!")
        print("Por favor, adicione DISCORD_STAFF_BOT_TOKEN nas Secrets do Replit")
        return
    
    keep_alive()
    
    staff_thread = Thread(target=run_bot_thread, args=(bot_staff, token_staff), daemon=True)
    
    staff_thread.start()
    staff_thread.join()

if __name__ == "__main__":
    main()
