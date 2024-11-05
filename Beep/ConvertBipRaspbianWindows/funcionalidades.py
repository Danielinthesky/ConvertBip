#Funcionalidades.py

import numpy as np
import matplotlib.pyplot as plt
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Label, Button
import threading



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

def gerar_qr_code(texto):
    """
    Gera um QR Code a partir do texto fornecido e o exibe.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.show()  # Abre a imagem gerada
    return img

def abrir_janela_qr_code():
    janela_qr = tk.Toplevel()
    janela_qr.title("QR Code para Conexão")

    # Gerar o QR Code
    texto_qr = "http://convertbip-pc.local"  # Substitua pelo endereço necessário
    qr = qrcode.make(texto_qr)
    img = ImageTk.PhotoImage(qr)

    label_qr = Label(janela_qr, image=img)
    label_qr.pack(pady=10)

    label_timer = Label(janela_qr, text="O QR Code expira em 15 segundos")
    label_timer.pack(pady=5)

    def fechar_janela():
        label_timer.config(text="QR Code expirado")
        janela_qr.after(1000, janela_qr.destroy)

    # Iniciar um timer de 15 segundos
    threading.Timer(15, fechar_janela).start()

    janela_qr.mainloop()
# Outras funções de análise podem ser adicionadas aqui
