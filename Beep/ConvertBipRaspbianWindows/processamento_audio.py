# Script para processar o áudio capturado e calcular a frequência dominante usando a Transformada de Fourier (FFT)

import numpy as np

# Função para processar os dados de áudio e calcular a frequência dominante
def processar_audio(dados_audio):
    espectro_fft = np.abs(np.fft.fft(dados_audio))
    frequencias = np.fft.fftfreq(len(dados_audio), 1 / 44100)
    # Limitar a análise à faixa de frequências entre 1 kHz e 2 kHz
    mask = (frequencias >= 1000) & (frequencias <= 2000)
    frequencia_dominante = frequencias[mask][np.argmax(espectro_fft[mask])]
    return frequencia_dominante

