
# Script para comparar a frequência dominante obtida com padrões de bips conhecidos

def comparar_frequencias(frequencia):
    if 410 < frequencia < 490:
        return "Bip curto"
    elif 1010 < frequencia < 1190:
        return "Bip longo"
    elif 2050 < frequencia < 2450:
        return "Problema de vídeo (1 bip longo, 3 curtos)"
    elif 1520 < frequencia < 1780:
        return "Problema de RAM (1 bip longo, 2 curtos)"
    else:
        return "Frequência desconhecida"
