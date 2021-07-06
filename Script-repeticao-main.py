# Este script roda o main.py e deveria setar novos parâmetros (a ser consertado).

import main
import random

# retorna a quantidade de linhas do arquivo
def quantidade_linhas_arquivo( ):
    a = open("enderecosInteiros.txt", 'r')
    contador  = 0
    for linha in a:
        contador += 1
    return contador

# seta "novos" parâmetros
main.total_cache = 0
main.endereco_falha = 0 # random.randint(0, quantidade_linhas_arquivo())
main.linha_tlb_falha = 0 # random.randint(0, 3)
main.bit_falho = 0 #random.randint(2, 33)

# chama o main.py e executa
exec(open("main.py").readline())
if (main.erro == 1):
    print("Houve falso positivo nesse teste")
