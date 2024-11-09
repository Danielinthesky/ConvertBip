import socket

# Configuração do servidor
host = '0.0.0.0'  # Escuta em todas as interfaces de rede
port = 12345      # Porta de comunicação

# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Servidor escutando em {host}:{port}")

def processar_comando(data):
    if data == "vibrate_short":
        print("Comando recebido: Vibração curta")
        # Ação para vibração curta
    elif data == "vibrate_long":
        print("Comando recebido: Vibração longa")
        # Ação para vibração longa
    else:
        print("Comando desconhecido")

# Aceitar conexões
while True:
    conn, addr = server_socket.accept()
    print(f"Conexão estabelecida com {addr}")

    # Recebe dados do cliente
    data = conn.recv(1024).decode()
    if data:
        print(f"Dados recebidos: {data}")
        processar_comando(data)
        # Responde ao cliente
        conn.send("Comando processado com sucesso!".encode())

    conn.close()
