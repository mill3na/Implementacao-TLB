# Este script roda o simulador.py e seta os parâmetros para paridade msb2 e falha tripla
import simulador
import random
from simulador import executaSimulador


# Declaração dos parâmetros fixos
total_cache = 8
arquivo_acesso = "traces.txt"
debug = 0

# Variável de controle do for que imprime a iteração atual
i = 0

def quantidade_linhas_arquivo():
    a = open(arquivo_acesso, 'r')
    contador = 0
    for linha in a:
        contador += 1

    return contador


# salva o resultado na variável senão acaba chamando a função a cada ciclo do for
linhas = quantidade_linhas_arquivo()

# Salva o resultado final de falsos positivos
fp_final = 0

# Seta os parâmetros
# Quando for testar, copia e cola alterando o tipo de código para cada tipo de falha
# Seta no range do for a quantidade de vezes que vai rodar para cada teste


for i in range(0, 1000):


    codigo = "PARIDADE_2MSB"
    endereco_falha = random.randint(0, linhas)
    linha_tlb_falha = random.randint(1, 7)
    bit_falho = random.randint(1, 31)
    tipo_falhas_inseridas = "FALHA_TRIPLA"

    # chama o simulador.py, executa e contabiliza o retorno
    simulador.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho,
                               tipo_falhas_inseridas)
    fp = executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho,
                          tipo_falhas_inseridas)
    if fp == 1:
        fp_final += 1

    print("— "*20)
    print(f'\nIteração: {i+1}. Número de falsos positivos: {fp_final}.\n')
print(f'\033[31m\nNúmero de iterações {i + 1}. \nFalsos positivos ao longo da simulação: {fp_final}.\033[m')
