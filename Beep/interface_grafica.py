import numpy as np
import pyaudio
from pyqtgraph.Qt import QtCore, QtWidgets
import pyqtgraph as pg
from scipy.signal import hilbert
import sys
import bluetooth  # Para lidar com dispositivos Bluetooth
from bluetooth_handler import enviar_bips_para_celular, listar_dispositivos_pareados
from PyQt5.QtCore import QTimer
import threading
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Importar para exibir VLibras

# Configurações de áudio
fs = 44100
chunk = 1024
n_windows = 180

# Inicializar PyAudio com tratamento de erro
def iniciar_stream_audio():
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=chunk)
        return audio, stream
    except Exception as e:
        print(f"Erro ao iniciar stream de áudio: {e}")
        sys.exit(1)

audio, stream = iniciar_stream_audio()

# Função para capturar dados do microfone
def capturar_audio():
    try:
        data = stream.read(chunk, exception_on_overflow=False)
        return np.frombuffer(data, dtype=np.int16)
    except Exception as e:
        print(f"Erro ao capturar áudio: {e}")
        return np.zeros(chunk, dtype=np.int16)

# Fechar o stream e áudio corretamente
def encerrar_stream():
    if stream.is_active():
        stream.stop_stream()
    stream.close()
    audio.terminate()

# Função para listar dispositivos Bluetooth
def listar_dispositivos(atualizar_painel):
    dispositivos = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
    dispositivos_filtrados = [(endereco, nome) for endereco, nome, classe in dispositivos if (classe & 0x1F00) in [0x100, 0x500, 0x200, 0x300]]
    
    if not dispositivos_filtrados:
        atualizar_painel("Nenhum dispositivo encontrado.")
    return dispositivos_filtrados

# Função para enviar padrões de vibração para o dispositivo
def enviar_vibracao(padrao_vibracao, atualizar_painel):
    try:
        enviar_bips_para_celular(padrao_vibracao, atualizar_painel)
    except Exception as e:
        atualizar_painel(f"Erro ao enviar vibração: {e}")

# Função para exibir a tradução em Libras com VLibras
def exibir_vlibras(padrao):
    vlibras_view.setUrl(QtCore.QUrl(f"https://www.vlibras.gov.br/translate?text={padrao}"))

# Interface PyQtGraph
app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
central_widget = QtWidgets.QWidget()
win.setCentralWidget(central_widget)
layout = QtWidgets.QHBoxLayout(central_widget)

# Barra de menu com opções de configuração
menu_bar = win.menuBar()
config_menu = menu_bar.addMenu('Configurações')

# Opção para alternar a exibição das escalas (grade)
toggle_scale_action = QtWidgets.QAction('Alternar Exibição das Escalas', win)
toggle_scale_action.setCheckable(True)
toggle_scale_action.setChecked(False)  # Começa com escalas desabilitadas

# Função para iniciar sem mostrar linhas de grade ou escalas
def iniciar_sem_linhas_escala():
    for plot in [waveform_plot, fft_plot, envelope_plot, spectrogram_plot]:
        plot.showGrid(x=False, y=False)
        plot.getAxis('bottom').hide()
        plot.getAxis('left').hide()

# Função para alternar a exibição das escalas (grade e linhas)
def toggle_scales(checked):
    for plot in [waveform_plot, fft_plot, envelope_plot, spectrogram_plot]:
        if checked:
            plot.showGrid(x=True, y=True)
            plot.getAxis('bottom').show()
            plot.getAxis('left').show()
        else:
            plot.showGrid(x=False, y=False)
            plot.getAxis('bottom').hide()
            plot.getAxis('left').hide()

# Conectar a ação de alternar escalas ao menu de configuração
toggle_scale_action.triggered.connect(lambda: toggle_scales(toggle_scale_action.isChecked()))
config_menu.addAction(toggle_scale_action)

# Painel esquerdo
panel_widget = QtWidgets.QWidget()
panel_widget.setFixedWidth(300)
panel_widget.setStyleSheet("background-color: black;")
panel_layout = QtWidgets.QVBoxLayout(panel_widget)

# Label para mensagens
panel_label = QtWidgets.QLabel("Iniciando o programa.")
panel_label.setStyleSheet("color: white; font-size: 18px;")
panel_label.setWordWrap(True)
panel_layout.addWidget(panel_label)

# Função para atualizar o painel de mensagens
def atualizar_painel(mensagem):
    panel_label.setText(mensagem)

# Tabela para dispositivos
tabela_dispositivos = QtWidgets.QTableWidget()
tabela_dispositivos.setColumnCount(2)
tabela_dispositivos.setHorizontalHeaderLabels(['Endereço', 'Nome'])
panel_layout.addWidget(tabela_dispositivos)

# Função para atualizar a tabela
def atualizar_tabela(dispositivos):
    tabela_dispositivos.setRowCount(len(dispositivos))
    for idx, (endereco, nome) in enumerate(dispositivos):
        tabela_dispositivos.setItem(idx, 0, QtWidgets.QTableWidgetItem(endereco))
        tabela_dispositivos.setItem(idx, 1, QtWidgets.QTableWidgetItem(nome))

# Botão para listar dispositivos e conectar
def conectar_dispositivo():
    dispositivos = listar_dispositivos(atualizar_painel)
    atualizar_tabela(dispositivos)

tabela_dispositivos.cellClicked.connect(lambda row, _: conectar_dispositivo())

botao_conectar = QtWidgets.QPushButton("Conectar Bluetooth")
botao_conectar.clicked.connect(conectar_dispositivo)
panel_layout.addWidget(botao_conectar)

# Botão para enviar vibração
botao_vibrar = QtWidgets.QPushButton("Enviar Vibração")
botao_vibrar.clicked.connect(lambda: enviar_vibracao("long,short", atualizar_painel))
panel_layout.addWidget(botao_vibrar)

layout.addWidget(panel_widget)

# Gráficos
plot_layout = QtWidgets.QGridLayout()
layout.addLayout(plot_layout)

waveform_plot = pg.PlotWidget(title="Waveform")
fft_plot = pg.PlotWidget(title="Frequência Dominante")
envelope_plot = pg.PlotWidget(title="Envelope")
spectrogram_plot = pg.PlotWidget(title="Espectrograma")

plot_layout.addWidget(waveform_plot, 0, 0)
plot_layout.addWidget(fft_plot, 0, 1)
plot_layout.addWidget(envelope_plot, 1, 0)
plot_layout.addWidget(spectrogram_plot, 1, 1)

waveform_curve = waveform_plot.plot()
fft_curve = fft_plot.plot()
envelope_curve = envelope_plot.plot()
spectrogram_image = pg.ImageItem()
spectrogram_plot.addItem(spectrogram_image)

spectrogram_data = np.zeros((chunk // 2, n_windows))

# Função para atualizar o espectrograma
def update_spectrograma():
    audio_data = capturar_audio()
    fft_spectrum = np.abs(np.fft.fft(audio_data))
    global spectrogram_data
    spectrogram_data[:, 1:] = spectrogram_data[:, :-1]
    spectrogram_data[:, 0] = fft_spectrum[:chunk // 2]
    spectrogram_image.setImage(np.flipud(spectrogram_data.T), autoRange=False)

# Função para atualizar outros gráficos
def update_outros_graficos():
    audio_data = capturar_audio()
    waveform_curve.setData(audio_data)

    freqs = np.fft.fftfreq(len(audio_data), 1 / fs)
    fft_spectrum = np.abs(np.fft.fft(audio_data))
    fft_curve.setData(freqs[:len(freqs) // 2], fft_spectrum[:len(fft_spectrum) // 2])

    envelope_data = np.abs(hilbert(audio_data))
    envelope_curve.setData(envelope_data)

# Timers para atualizar gráficos
timer_spectrograma = QtCore.QTimer()
timer_spectrograma.timeout.connect(update_spectrograma)
timer_spectrograma.start(50)

timer_outros = QtCore.QTimer()
timer_outros.timeout.connect(update_outros_graficos)
timer_outros.start(100)

# Seção VLibras à direita dos gráficos
vlibras_view = QWebEngineView()
vlibras_view.setUrl(QtCore.QUrl("https://www.vlibras.gov.br/"))
layout.addWidget(vlibras_view)

# Finalizando
win.resize(1900, 800)  # Aumentando a tela para acomodar o VLibras
win.setWindowTitle('ConvertBip - Com VLibras em Tempo Real')
win.show()

# Fechar corretamente ao sair
def close_app():
    encerrar_stream()
    app.quit()

win.closeEvent = lambda event: close_app()

# Agora chamar a função para não mostrar linhas e escalas
iniciar_sem_linhas_escala()

app.exec_()
