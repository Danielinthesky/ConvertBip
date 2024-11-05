# Script para comparar a frequência dominante obtida com padrões de bips conhecidos
# Utilizado para identificar o tipo de bip (bip curto, bip longo, etc.)

# Função para comparar a frequência dominante com padrões predefinidos
def comparar_frequencias(frequencia):
    # Verifica se a frequência dominante está dentro dos limites de um bip curto
    if 400 < frequencia < 500:
        return "Bip curto"

    # Verifica se a frequência dominante está dentro dos limites de um bip longo
    elif 1000 < frequencia < 1200:
        return "Bip longo"

    # Verifica se a frequência corresponde a um problema de vídeo (1 bip longo, 3 curtos)
    elif 2000 < frequencia < 2500:
        return "Problema de vídeo (1 bip longo, 3 curtos)"

    # Verifica se a frequência corresponde a um problema de RAM (1 bip longo, 2 curtos)
    elif 1500 < frequencia < 1800:
        return "Problema de RAM (1 bip longo, 2 curtos)"

    # Caso nenhuma correspondência seja encontrada, retorna como desconhecida
    else:
        return "Frequência desconhecida"
