from captura_audio import capturar_audio
from processamento_audio import processar_audio
from comparacao_frequencias import comparar_frequencias
from interface_grafica import atualizar_interface_com_resultado
from chatgptopenai import consultar_chatgpt  # Integração com ChatGPT
from bluetooth_handler import enviar_bips_para_celular  # Integração com Bluetooth

def processar_bips(resultado):
    if resultado == "Problema de Vídeo":
        padrao = "long,short,short,short"
        enviar_bips_para_celular(padrao)
    elif resultado == "Erro de RAM":
        padrao = "long,short,short"
        enviar_bips_para_celular(padrao)


def main():
    while True:
        # Captura o áudio do microfone
        dados_audio = capturar_audio()  

        # Processa o áudio para encontrar a frequência dominante
        frequencia = processar_audio(dados_audio)  

        # Compara a frequência dominante com padrões de bips conhecidos
        resultado = comparar_frequencias(frequencia)  

        # Se o algoritmo identificar o bip corretamente, atualiza a interface e envia via Bluetooth
        if resultado != "Frequência desconhecida":
            atualizar_interface_com_resultado(resultado)
            processar_bips(resultado)  # Enviar padrão via Bluetooth
        else:
            # Se o algoritmo não identificar o bip, chama o ChatGPT para tentar interpretar
            print("Consultando ChatGPT para interpretar o bip...")
            resposta_chatgpt = consultar_chatgpt(frequencia)
            
            # Exibe o resultado do ChatGPT
            atualizar_interface_com_resultado(resposta_chatgpt)
            
            # Se o ChatGPT fornecer um padrão, enviar via Bluetooth
            if "long" in resposta_chatgpt or "short" in resposta_chatgpt:
                enviar_bips_para_celular(resposta_chatgpt)

if __name__ == "__main__":
    main()
