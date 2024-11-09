import numpy as np
import pyaudio
from pyqtgraph.Qt import QtCore, QtWidgets
import pyqtgraph as pg
from scipy.signal import hilbert, find_peaks
import sys
import bluetooth  # Para lidar com dispositivos Bluetooth
from bluetooth_handler import enviar_bips_para_celular, listar_dispositivos_pareados
from comparacao_frequencias import comparar_frequencias  # Função para detectar padrão de frequência
from collections import deque

# Configurações de áudio
fs = 44100
chunk = 1024
n_windows = 180
recent_patterns = deque(maxlen=10)  # Armazena as detecções recentes para análise contínua

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

# Interface PyQtGraph
app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
central_widget = QtWidgets.QWidget()
win.setCentralWidget(central_widget)
layout = QtWidgets.QVBoxLayout(central_widget)

# Dedicated panel for graphs
graph_panel = QtWidgets.QWidget()
layout.addWidget(graph_panel)
graph_layout = QtWidgets.QGridLayout(graph_panel)

# Indicador de status
status_label = QtWidgets.QLabel("Aguardando início...")
layout.addWidget(status_label)

# Plots
plot_layout = QtWidgets.QGridLayout()
layout.addLayout(plot_layout)

# Indicador de status da análise
status_label = QtWidgets.QLabel("Analisando...")
layout.addWidget(status_label)

# Barra de menu com opções de configuração
menu_bar = win.menuBar()
config_menu = menu_bar.addMenu('Configurações')

# Adicionar o toggle de exibição de escalas
toggle_scale_action = QtWidgets.QAction('Alternar Exibição das Escalas', win)
toggle_scale_action.setCheckable(True)
toggle_scale_action.setChecked(False)  # Começa com escalas desabilitadas

show_waveform_action = QtWidgets.QAction('Mostrar Waveform', win, checkable=True)
show_fft_action = QtWidgets.QAction('Mostrar Frequência Dominante', win, checkable=True)
show_envelope_action = QtWidgets.QAction('Mostrar Envelope', win, checkable=True)

# Adicionando ações ao menu
config_menu.addAction(show_waveform_action)
config_menu.addAction(show_fft_action)
config_menu.addAction(show_envelope_action)

# Função para reposicionar gráficos com base nas seleções
def update_graphics_layout():
    for i in reversed(range(graph_layout.count())):
        graph_layout.itemAt(i).widget().setParent(None)

    graphs_to_show = [spectrogram_plot]  # Default spectrogram
    if show_waveform_action.isChecked():
        graphs_to_show.append(waveform_plot)
    if show_fft_action.isChecked():
        graphs_to_show.append(fft_plot)
    if show_envelope_action.isChecked():
        graphs_to_show.append(envelope_plot)

    # Dynamically arrange graphs within the panel based on the number of active graphs
    num_graphs = len(graphs_to_show)
    if num_graphs == 1:
        graph_layout.addWidget(graphs_to_show[0], 0, 0, 2, 2)
    elif num_graphs == 2:
        graph_layout.addWidget(graphs_to_show[0], 0, 0, 2, 1)
        graph_layout.addWidget(graphs_to_show[1], 0, 1, 2, 1)
    elif num_graphs == 3:
        graph_layout.addWidget(graphs_to_show[0], 0, 0)
        graph_layout.addWidget(graphs_to_show[1], 0, 1)
        graph_layout.addWidget(graphs_to_show[2], 1, 0, 1, 2)
    else:
        graph_layout.addWidget(graphs_to_show[0], 0, 0)
        graph_layout.addWidget(graphs_to_show[1], 0, 1)
        graph_layout.addWidget(graphs_to_show[2], 1, 0)
        graph_layout.addWidget(graphs_to_show[3], 1, 1)

# Conectar as ações ao sistema de atualização de gráficos
show_waveform_action.toggled.connect(update_graphics_layout)
show_fft_action.toggled.connect(update_graphics_layout)
show_envelope_action.toggled.connect(update_graphics_layout)

# Layout de gráficos
plot_layout = QtWidgets.QGridLayout()
layout.addLayout(plot_layout)

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

# Configurações para detecção de bips
short_bip_threshold = (400, 500)  # Faixa para bip curto
long_bip_threshold = (1000, 1200)  # Faixa para bip longo
recent_patterns = deque(maxlen=10)  # Armazena as detecções recentes para análise contínua


# Gráficos
plot_layout = QtWidgets.QGridLayout()
layout.addLayout(plot_layout)

waveform_plot = pg.PlotWidget(title="Waveform")
fft_plot = pg.PlotWidget(title="Frequência Dominante")
envelope_plot = pg.PlotWidget(title="Envelope")
spectrogram_plot = pg.PlotWidget(title="Espectrograma")

# Espectrograma como padrão
plot_layout.addWidget(spectrogram_plot, 0, 0, 2, 2)



waveform_curve = waveform_plot.plot()
fft_curve = fft_plot.plot()
envelope_curve = envelope_plot.plot()
spectrogram_image = pg.ImageItem()
spectrogram_plot.addItem(spectrogram_image)

spectrogram_data = np.zeros((chunk // 2, n_windows))



# Função para análise dos bips e detecção dos padrões
def detectar_padroes_bips(frequencia_dominante=None):
    # Configurações de duração para bips longos e curtos
    long_bip_min_duration = 0.4  # Duração mínima de um bip longo (em segundos)
    short_bip_max_duration = 0.2  # Duração máxima de um bip curto (em segundos)

    audio_data = capturar_audio()
    
    # Análise de envelope para identificar picos
    envelope = np.abs(hilbert(audio_data))
    peaks, properties = find_peaks(envelope, height=np.max(envelope) * 0.5, distance=fs * 0.1)
    
    # Determinar a duração entre picos para classificar bips longos e curtos
    intervals = np.diff(peaks) / fs  # Intervalo em segundos
    bip_types = []
    
    for interval in intervals:
        if interval >= long_bip_min_duration:
            bip_types.append("Bip longo")
        elif interval <= short_bip_max_duration:
            bip_types.append("Bip curto")
        else:
            bip_types.append("Ruído/Desconhecido")

    recent_patterns.extend(bip_types)

    # Imprimir o tipo de bip detectado
    print("Tipos de bip detectados na janela atual:", bip_types)

    # Verificar padrões
    if recent_patterns.count("Bip longo") >= 1 and recent_patterns.count("Bip curto") >= 2:
        if list(recent_patterns)[-3:] == ["Bip curto", "Bip curto", "Bip curto"]:
            status_label.setText("Padrão Detectado: Problema de vídeo (1 longo, 3 curtos)")
        elif list(recent_patterns)[-2:] == ["Bip curto", "Bip curto"]:
            status_label.setText("Padrão Detectado: Problema de RAM (1 longo, 2 curtos)")
    else:
        status_label.setText("Analisando...")

# Função para processar o áudio e detectar padrões
def processar_audio():
    audio_data = capturar_audio()
    fft_spectrum = np.abs(np.fft.fft(audio_data))
    freqs = np.fft.fftfreq(len(audio_data), 1 / fs)
    dominant_freq = freqs[np.argmax(fft_spectrum[:len(freqs) // 2])]
    detectar_padroes_bips(dominant_freq)



# Timers para atualizar cada gráfico individualmente
timer_waveform = QtCore.QTimer()
timer_waveform.timeout.connect(lambda: update_waveform())

timer_fft = QtCore.QTimer()
timer_fft.timeout.connect(lambda: update_fft())

timer_envelope = QtCore.QTimer()
timer_envelope.timeout.connect(lambda: update_envelope())

timer_spectrogram = QtCore.QTimer()
timer_spectrogram.timeout.connect(lambda: update_spectrograma())

# Configurações de intervalos para cada gráfico (em milissegundos)
timer_waveform.setInterval(150)     # Ajuste conforme desejado
timer_fft.setInterval(200)          # Ajuste conforme desejado
timer_envelope.setInterval(200)     # Ajuste conforme desejado
timer_spectrogram.setInterval(100)  # Ajuste conforme desejado

# Funções de atualização individuais
def update_waveform():
    audio_data = capturar_audio()
    waveform_curve.setData(audio_data)

def update_fft():
    audio_data = capturar_audio()
    fft_spectrum = np.abs(np.fft.fft(audio_data))
    freqs = np.fft.fftfreq(len(audio_data), 1 / fs)
    fft_curve.setData(freqs[:len(freqs) // 2], fft_spectrum[:len(fft_spectrum) // 2])

def update_envelope():
    audio_data = capturar_audio()
    envelope_data = np.abs(hilbert(audio_data))
    envelope_curve.setData(envelope_data)

def update_spectrograma():
    audio_data = capturar_audio()
    fft_spectrum = np.abs(np.fft.fft(audio_data))
    global spectrogram_data
    spectrogram_data[:, 1:] = spectrogram_data[:, :-1]
    spectrogram_data[:, 0] = fft_spectrum[:chunk // 2]
    spectrogram_image.setImage(np.flipud(spectrogram_data.T), autoRange=False)


# Inicializando o layout
update_graphics_layout()    

# Botões para controle de captura
start_button = QtWidgets.QPushButton("Iniciar Captura")
stop_button = QtWidgets.QPushButton("Parar Captura")
layout.addWidget(start_button)
layout.addWidget(stop_button)

start_button.clicked.connect(lambda: [timer_waveform.start(), timer_fft.start(), timer_envelope.start(), timer_spectrogram.start()])
stop_button.clicked.connect(lambda: [timer_waveform.stop(), timer_fft.stop(), timer_envelope.stop(), timer_spectrogram.stop()])


# Botões Bluetooth e Vibração
buttons_layout = QtWidgets.QHBoxLayout()
layout.addLayout(buttons_layout)

botao_conectar = QtWidgets.QPushButton("Conectar Bluetooth")
botao_conectar.setFixedHeight(40)  # Aumenta a altura do botão
botao_conectar.setStyleSheet("font-size: 16px;")
botao_conectar.clicked.connect(lambda: listar_dispositivos(lambda x: print(x)))  # Placeholder para conexão
buttons_layout.addWidget(botao_conectar)

botao_vibrar = QtWidgets.QPushButton("Enviar Vibração")
botao_vibrar.setFixedHeight(40)  # Aumenta a altura do botão
botao_vibrar.setStyleSheet("font-size: 16px;")
botao_vibrar.clicked.connect(lambda: enviar_vibracao("long,short", lambda x: print(x)))
buttons_layout.addWidget(botao_vibrar)

# Finalizando
win.resize(1600, 800)  # Redimensionando a janela
win.setWindowTitle('ConvertBip - Com Vibrações em Tempo Real')
win.show()

# Fechar corretamente ao sair
def close_app():
    encerrar_stream()
    app.quit()

win.closeEvent = lambda event: close_app()

# Agora chamar a função para não mostrar linhas e escalas
iniciar_sem_linhas_escala()

app.exec_()
