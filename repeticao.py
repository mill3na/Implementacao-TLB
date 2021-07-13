# Este script roda o main.py e deveria setar os parâmetros.

import main
import random
from main import executaSimulador

# seta os parâmetros
for i in range(0,3):
    total_cache = 8
    arquivo_acesso = "controle.txt"
    debug = 1
    codigo = "NENHUM"
    endereco_falha = random.randint(0,9)
    linha_tlb_falha = random.randint(0, 7)
    bit_falho = random.randint(17, 32)
    tipo_falhas_inseridas = "FALHA_DUPLA"

    # chama o simulador.py e executa
    main.executaSimulador(total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas)
