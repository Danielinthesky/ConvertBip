
# Script para integrar o ChatGPT e interpretar padrões de bips desconhecidos

import openai
import os

# Função para consultar o ChatGPT, explicando o padrão de frequência desconhecido
def consultar_chatgpt(frequencia):
    try:
        # Chave de API do ChatGPT
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Mensagem para o ChatGPT interpretar a frequência desconhecida
        prompt = f"Eu detectei uma frequência de {frequencia} Hz que não corresponde a um bip comum. O que pode ser isso?"

        # Consulta ao modelo do ChatGPT
        resposta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        # Retorna a resposta interpretada pelo ChatGPT
        return resposta.choices[0].text.strip()

    except Exception as e:
        return f"Erro ao consultar ChatGPT: {e}"
