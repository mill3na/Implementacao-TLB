# Este script roda o main.py e seta os parâmetros.

import main
import random
from main import executaSimulador

#Declaração dos parâmetros fixos
total_cache = 8
arquivo_acesso = "traces.txt"
debug = 0

def quantidade_linhas_arquivo():
    a = open(arquivo_acesso, 'r')
    contador  = 0
    for linha in a:
        contador += 1
    #print(contador)
    return contador

#salva o resultado na variável senão acaba chamando a função a cada ciclo do for
linhas = quantidade_linhas_arquivo()


# Seta os parâmetros
# Quando for testar, copia e cola alterando o tipo de código para cada tipo de falha
# Seta no range do for a quantidade de vezes que vai rodar para cada teste

for i in range(0,1000):

    codigo = "NENHUM"
    endereco_falha = random.randint(0, linhas)
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(0, 31)
    tipo_falhas_inseridas = "FALHA_SIMPLES"

    # chama o main.py, executa e contabiliza o retorno
    
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)
    print("iteração:",i+1)
    #print("codigo: nenhum")
    #print("falha simples")
    print('-' * 5)
