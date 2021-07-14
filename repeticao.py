# Este script roda o main.py e seta os parâmetros.
import csv
import simulador
import random
from main import executaSimulador

def quantidade_linhas_arquivo():
    a = open("controle.txt", 'r')
    contador  = 0
    for linha in a:
        contador += 1
    return contador

#Declaração dos parâmetros mais fixos
total_cache = 8
arquivo_acesso = "controle.txt"
debug = 1 


# seta os parâmetros
for i in range(0,10):

    codigo = "NENHUM"
    endereco_falha = random.randint(0, quantidade_linhas_arquivo())
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(0, 31)
    tipo_falhas_inseridas = "FALHA_SIMPLES"

    # chama o main.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)

for i in range(0,10):

    codigo = "NENHUM"
    endereco_falha = random.randint(0,quantidade_linhas_arquivo())
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(0, 31)
    tipo_falhas_inseridas = "FALHA_DUPLA"

    # chama o main.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)

for i in range(0,10):

    codigo = "NENHUM"
    endereco_falha = random.randint(0,quantidade_linhas_arquivo())
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(1, 31)
    tipo_falhas_inseridas = "FALHA_TRIPLA"

    # chama o main.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)

for i in range(0,10):

    codigo = "PARIDADE_MSB"
    endereco_falha = random.randint(0, quantidade_linhas_arquivo())
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(0, 31)
    tipo_falhas_inseridas = "FALHA_SIMPLES"

    # chama o main.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)

for i in range(0,10):

    codigo = "PARIDADE_MSB"
    endereco_falha = random.randint(0,quantidade_linhas_arquivo())
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(0, 31)
    tipo_falhas_inseridas = "FALHA_DUPLA"

    # chama o main.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)

for i in range(0,10):

    codigo = "PARIDADE_MSB"
    endereco_falha = random.randint(0,quantidade_linhas_arquivo())
    linha_tlb_falha = random.randint(1,7)
    bit_falho = random.randint(1, 31)
    tipo_falhas_inseridas = "FALHA_TRIPLA"

    # chama o main.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)

#Criação do csv pra preencher o output, mas ainda tá bem simples

fp = str(simulador.erro)
o = open('output.csv', 'w', newline='', encoding='utf-8')
w = csv.writer(o)
w.writerow(fp)
o.close() 

