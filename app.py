import streamlit as st
from groq import Groq

st.set_page_config(page_title="Painel Siya Bot", page_icon="💅")
st.title("💅 Painel do Bot Siya")

client = Groq(api_key="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")

msg = st.text_area("Copie a mensagem do cara aqui:")
if st.button("Gerar Resposta Manual"):
    chat = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Responda com sarcasmo nível máximo."},
            {"role": "user", "content": msg}
        ],
        model="llama3-8b-8192",
    )
    st.success(chat.choices[0].message.content)
