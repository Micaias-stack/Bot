import os
import time
from groq import Groq
from playwright.sync_api import sync_playwright

# Sua chave que você me passou
GROQ_API_KEY = "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"
URL_SIYA = "https://siya.ai" # Site do App

client = Groq(api_key=GROQ_API_KEY)

def gerar_patada(texto):
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Você é uma usuária do app Siya, muito sarcástica. Responda mensagens de homens chatos com patadas curtas e inteligentes. Acabe com a graça deles."},
            {"role": "user", "content": texto}
        ],
        model="llama3-8b-8192",
    )
    return completion.choices[0].message.content

def rodar_automacao():
    with sync_playwright() as p:
        # Simulando um iPhone para o App não bloquear
        iphone = p.devices['iPhone 13']
        browser = p.chromium.launch(headless=True)
        
        # Tenta carregar o seu login salvo
        if os.path.exists("auth.json"):
            context = browser.new_context(storage_state="auth.json", **iphone)
        else:
            context = browser.new_context(**iphone)

        page = context.new_page()
        page.goto(URL_SIYA)
        time.sleep(10) # Espera o app carregar

        try:
            # Procura a última mensagem recebida no chat
            elemento_msg = page.query_selector(".message-text") or page.query_selector(".chat-item")
            
            if elemento_msg:
                msg_recebida = elemento_msg.inner_text()
                print(f"📩 Recebi: {msg_recebida}")
                
                resposta = gerar_patada(msg_recebida)
                
                # Digita e envia no campo de texto do App
                page.fill("input[type='text']", resposta)
                page.keyboard.press("Enter")
                print(f"✅ Patada enviada: {resposta}")
        except Exception as e:
            print(f"Aviso: Sem mensagens novas ou erro no site: {e}")

        browser.close()

if __name__ == "__main__":
    rodar_automacao()
