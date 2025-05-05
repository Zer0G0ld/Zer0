import random
import datetime

def gera_numero_aleatorio(minimo, maximo):
    """Gera um número aleatório entre mínimo e máximo com verificação de validade."""
    if minimo > maximo:
        raise ValueError("O valor mínimo não pode ser maior que o valor máximo.")
    return random.randint(minimo, maximo)

def saudacao(nome=None):
    """Retorna uma saudação personalizada baseada no horário do dia."""
    hora_atual = datetime.datetime.now().hour
    if nome is None:
        nome = "amigo"  # Usa um nome genérico se nenhum nome for passado
    
    if 5 <= hora_atual < 12:
        saudacao = "Bom dia"
    elif 12 <= hora_atual < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"
    
    return f"{saudacao}, {nome}! Como vai?"

# Testando as funções
print(gera_numero_aleatorio(1, 10))
print(saudacao("Carlos"))
