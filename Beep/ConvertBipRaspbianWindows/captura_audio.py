# Script para capturar o áudio do microfone usando a biblioteca PyAudio
# Configurações e captura de áudio

import pyaudio
import numpy as np

# Configurações de áudio (definir taxa de amostragem e tamanho do buffer)
taxa_amostragem = 44100  # Taxa de amostragem em Hz
tamanho_buffer = 1024  # Quantidade de amostras a serem capturadas por vez

# Função para capturar o áudio do microfone
def capturar_audio():
    # Inicializa o PyAudio para capturar o som
    py_audio = pyaudio.PyAudio()
    
    # Abre o stream para captura de áudio (usando as configurações definidas)
    stream_audio = py_audio.open(format=pyaudio.paInt16, 
                                 channels=1, 
                                 rate=taxa_amostragem, 
                                 input=True, 
                                 frames_per_buffer=tamanho_buffer)
    
    # Captura os dados de áudio do microfone em tempo real
    dados_capturados = stream_audio.read(tamanho_buffer)

    # Converte os dados de bytes para uma array NumPy (int16 para áudio)
    dados_audio = np.frombuffer(dados_capturados, dtype=np.int16)

    # Fecha o stream de áudio e finaliza a captura
    stream_audio.stop_stream()
    stream_audio.close()
    py_audio.terminate()

    return dados_audio  # Retorna os dados de áudio capturados
