#Funcionalidades.py

import numpy as np
import matplotlib.pyplot as plt

def gerar_espectrograma_interface(ax, audio_data, sr):
    ax.specgram(audio_data, NFFT=1024, Fs=sr, noverlap=512, cmap='inferno')
    ax.set_title('Espectrograma')
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Frequência (Hz)")

def gerar_envelope_interface(ax, audio_data, sr):
    envelope = np.abs(audio_data)
    envelope_suavizado = np.convolve(envelope, np.ones(1000) / 1000, mode='same')
    tempo = np.arange(len(envelope_suavizado)) / sr
    ax.plot(tempo, envelope_suavizado)
    ax.set_title('Envelope do Som')
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Amplitude")

def gerar_waveform_interface(ax, audio_data, sr):
    tempo = np.arange(len(audio_data)) / sr
    ax.plot(tempo, audio_data)
    ax.set_title('Waveform')
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Amplitude")

# Outras funções de análise podem ser adicionadas aqui
