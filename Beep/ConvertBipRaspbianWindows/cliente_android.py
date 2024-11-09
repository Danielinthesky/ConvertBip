import socket

def enviar_comando_para_android(comando, ip_android, porta=12345):
    """
    Conecta ao servidor Android e envia o comando de vibração.
    :param comando: O comando de vibração ("vibrate_short" ou "vibrate_long").
    :param ip_android: O endereço IP do dispositivo Android.
    :param porta: A porta na qual o servidor Android está escutando (12345 por padrão).
    """
    try:
        # Cria um socket TCP e conecta ao servidor Android
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip_android, porta))
            client_socket.sendall(comando.encode())
            print(f"Comando '{comando}' enviado para o Android.")
    except Exception as e:
        print(f"Erro ao conectar ao Android: {e}")

# Exemplo de uso
if __name__ == "__main__":
    ip_android = "IP_DO_ANDROID"  # Substitua pelo IP do dispositivo Android
    enviar_comando_para_android("vibrate_short", ip_android)
    enviar_comando_para_android("vibrate_long", ip_android)
