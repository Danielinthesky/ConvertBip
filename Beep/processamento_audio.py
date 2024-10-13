# Script para processar o áudio capturado e calcular a frequência dominante usando a Transformada de Fourier (FFT)

import numpy as np

# Função para processar os dados de áudio e calcular a frequência dominante
def processar_audio(dados_audio):
    # Aplica a Transformada de Fourier no áudio para obter o espectro de frequências
    espectro_fft = np.abs(np.fft.fft(dados_audio))

    # Gera uma lista de frequências correspondentes ao espectro
    frequencias = np.fft.fftfreq(len(dados_audio), 1 / 44100)

    # Localiza a frequência dominante (o maior pico no espectro)
    frequencia_dominante = frequencias[np.argmax(espectro_fft[:len(frequencias)//2])]

    # Retorna a frequência dominante para posterior análise
    return frequencia_dominante
