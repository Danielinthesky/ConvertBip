import bluetooth
import threading

def listar_dispositivos_pareados(atualizar_painel):
    """
    Lista todos os dispositivos Bluetooth pareados e exibe na interface.
    """
    def buscar_dispositivos():
        dispositivos_pareados = bluetooth.discover_devices(lookup_names=True, lookup_class=True)

        if not dispositivos_pareados:
            atualizar_painel("Nenhum dispositivo pareado encontrado.")
            return []

        mensagem = "Dispositivos pareados encontrados:\n"
        for idx, (endereco, nome, _) in enumerate(dispositivos_pareados):
            mensagem += f"{idx}: {nome} - {endereco}\n"

        atualizar_painel(mensagem)
        return [(endereco, nome) for endereco, nome, _ in dispositivos_pareados]

    # Executa a descoberta de dispositivos em uma thread separada
    thread = threading.Thread(target=buscar_dispositivos)
    thread.start()

def selecionar_dispositivo_pareado(dispositivos, atualizar_painel):
    """
    Permite que o usuário selecione um dispositivo pareado da lista exibida via interface.
    """
    if not dispositivos:
        atualizar_painel("Nenhum dispositivo disponível para seleção.")
        return None

    # A interface pode ter um campo onde o usuário insere o índice do dispositivo
    escolha = int(input("Digite o número do dispositivo desejado: "))  # Isso deve ser substituído por um input na interface
    
    if 0 <= escolha < len(dispositivos):
        endereco, nome = dispositivos[escolha]
        atualizar_painel(f"Dispositivo selecionado: {nome} ({endereco})")
        return endereco, nome
    else:
        atualizar_painel("Escolha inválida. Tente novamente.")
        return None

def conectar_dispositivo(endereco_bluetooth, atualizar_painel):
    """
    Conecta ao dispositivo Bluetooth selecionado e atualiza a interface.
    """
    def conectar():
        try:
            socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            socket.connect((endereco_bluetooth, 1))
            atualizar_painel(f"Conectado ao dispositivo: {endereco_bluetooth}")
            return socket
        except bluetooth.BluetoothError as e:
            atualizar_painel(f"Erro ao conectar ao dispositivo: {e}")
            return None

    # Executa a conexão em uma thread separada
    thread = threading.Thread(target=conectar)
    thread.start()

def enviar_comando(socket, comando, atualizar_painel):
    """
    Envia um comando via Bluetooth e exibe o status na interface.
    """
    try:
        socket.send(comando)
        atualizar_painel(f"Comando '{comando}' enviado com sucesso.")
    except bluetooth.BluetoothError as e:
        atualizar_painel(f"Erro ao enviar comando: {e}")

# Função principal para integrar com a interface gráfica
def main(atualizar_painel):
    """
    Função principal para integrar com a interface, listar dispositivos, selecionar e conectar.
    """
    def executar():
        dispositivos_pareados = listar_dispositivos_pareados(atualizar_painel)

        if dispositivos_pareados:
            resultado_selecao = selecionar_dispositivo_pareado(dispositivos_pareados, atualizar_painel)
            if resultado_selecao:
                endereco_selecionado, nome_selecionado = resultado_selecao
                socket = conectar_dispositivo(endereco_selecionado, atualizar_painel)
                if socket:
                    # Exemplo de envio de comando após a conexão
                    enviar_comando(socket, "vibrate_short", atualizar_painel)
                else:
                    atualizar_painel("Falha na conexão com o dispositivo.")
        else:
            atualizar_painel("Nenhum dispositivo disponível para conectar.")

    # Executa o fluxo principal em uma thread separada
    thread = threading.Thread(target=executar)
    thread.start()

def enviar_bips_para_celular(padrao_bips, atualizar_painel):
    """
    Função para enviar padrões de bips (vibração) para o celular via Bluetooth.
    """
    try:
        # Verifica se o dispositivo está conectado (substitua pelo código correto de verificação de conexão)
        # socket deve ser o BluetoothSocket que você criou ao conectar ao dispositivo.
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  # Suponha que você tenha o socket conectado.

        # Enviar o padrão de vibração (bip) para o celular
        socket.send(padrao_bips)
        atualizar_painel(f"Padrão de bips '{padrao_bips}' enviado para o dispositivo.")

    except bluetooth.BluetoothError as e:
        atualizar_painel(f"Erro ao enviar bips para o dispositivo: {e}")
