import socket

# Configurações do servidor
host = '0.0.0.0'  # Escuta em todas as interfaces de rede
port = 12345     # Porta de comunicação

# Criar o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Servidor escutando em {host}:{port}")

# Aceitar conexões
while True:
    conn, addr = server_socket.accept()
    print(f"Conexão estabelecida com {addr}")

    # Receber dados do cliente
    data = conn.recv(1024).decode()
    if data:
        print(f"Dados recebidos: {data}")
        # Responder ao cliente
        conn.send("Dados recebidos com sucesso!".encode())

    conn.close()
