
# Integração com ChatGPT para interpretação de frequências desconhecidas com mais contexto

import openai
import os

def consultar_chatgpt(frequencia, contexto_padroes_detectados):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Adicionando contexto sobre padrões previamente identificados
        prompt = f"A frequência {frequencia} Hz foi detectada e não corresponde a nenhum bip conhecido. "
        prompt += f"Os padrões de bips anteriormente detectados foram: {contexto_padroes_detectados}. "
        prompt += "O que essa frequência desconhecida pode representar?"

        resposta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return resposta.choices[0].text.strip()
    
    except Exception as e:
        return f"Erro ao consultar ChatGPT: {e}"
