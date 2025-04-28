import random

def gera_numero_aleatorio(minimo, maximo):
    """Gera um número aleatório entre mínimo e máximo."""
    return random.randint(minimo, maximo)

def saudacao(nome):
    """Função simples para retornar uma saudação personalizada."""
    return f"Olá, {nome}! Como vai?"
