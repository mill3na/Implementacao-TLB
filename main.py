import argparse, random, re
from bitstring import BitArray

contador_falsos_positivos = 0
num_falso_positivo = 0
erro = 0
fp = 0
r = 0
arq_binarios = "enderecosBinarios.txt"


# Exemplo de comando pra teste passando os argumentos :)
# main.py --total_cache=8 --tipo_mapeamento=AS --arquivo_acesso=enderecosInteiros.txt --politica_substituicao=LRU --debug=1 --codigo=PARIDADE_MSB --endereco_falha=12 --linha_tlb_falha=3 --bit_falho=5 --tipo_falhas_inseridas=FALHA_SIMPLES
#


def gerar_falhas_cache(memoria_cache, index, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas, codigo):
    
    if (index != endereco_falha):
        # print("endereço falha", endereco_falha)
        return -1
    # print(memoria_cache)

    p = memoria_cache[linha_tlb_falha]  # pega o valor binario codificado direto na list memoria_cache
    if (tipo_falhas_inseridas == "FALHA_SIMPLES"):
        if (p[bit_falho] == '0'):
            p = muda_bit(p, bit_falho, 1)
        else:
            p = muda_bit(p, bit_falho, 0)

    if (tipo_falhas_inseridas == 'FALHA_DUPLA'):
        # verifica se a inserção de erro não está na última posição, para evitar erros do tipo index out of range

        if bit_falho != len(p):
            if (p[bit_falho] == '0'):
                p = muda_bit(p, bit_falho, 1)
            else:
                p = muda_bit(p, bit_falho, 0)

            if (p[bit_falho + 1] == '0'):
                p = muda_bit(p, bit_falho + 1, 1)
            else:
                p = muda_bit(p, bit_falho + 1, 0)

        if bit_falho == len(p):
            if (p[bit_falho] == '0'):
                p = muda_bit(p, bit_falho, 1)
            else:
                p = muda_bit(p, bit_falho, 0)

            if (p[bit_falho - 1] == '0'):
                p = muda_bit(p, bit_falho - 1, 1)
            else:
                p = muda_bit(p, bit_falho - 1, 0)

    if (tipo_falhas_inseridas == 'FALHA_TRIPLA'):
        # verifica se a inserção de erro não está na última posição, para evitar erros do tipo index out of range

        if bit_falho != len(p) and bit_falho != 2:
            if (p[bit_falho] == '0'):
                p = muda_bit(p, bit_falho, 1)
            else:
                p = muda_bit(p, bit_falho, 0)

            if (p[bit_falho + 1] == '0'):
                p = muda_bit(p, bit_falho + 1, 1)
            else:
                p = muda_bit(p, bit_falho + 1, 0)

            if (p[bit_falho - 1] == '0'):
                p = muda_bit(p, bit_falho - 1, 1)
            else:
                p = muda_bit(p, bit_falho - 1, 0)

        if bit_falho == len(p):

            if (p[bit_falho] == '0'):
                p = muda_bit(p, bit_falho, 1)
            else:
                p = muda_bit(p, bit_falho, 0)

            if (p[bit_falho + 1] == '0'):
                p = muda_bit(p, bit_falho - 1, 1)
            else:
                p = muda_bit(p, bit_falho - 1, 0)

            if (p[bit_falho - 1] == '0'):
                p = muda_bit(p, bit_falho - 2, 1)
            else:
                p = muda_bit(p, bit_falho - 2, 0)

        if bit_falho == 2 and codigo == 'PARIDADE_SIMPLES':
            # no codigo de paridade simples, temos 34 bits. Essa vericação impede que o bit na posição 1 seja alterado.
            if (p[bit_falho] == '0'):
                p = muda_bit(p, bit_falho, 1)
            else:
                p = muda_bit(p, bit_falho, 0)

            if (p[bit_falho + 1] == '0'):
                p = muda_bit(p, bit_falho + 1, 1)
            else:
                p = muda_bit(p, bit_falho + 1, 0)

            if (p[bit_falho + 2] == '0'):
                p = muda_bit(p, bit_falho + 2, 1)
            else:
                p = muda_bit(p, bit_falho + 2, 0)

        if bit_falho == 1 and codigo != 'PARIDADE_SIMPLES':
            # nos demais códigos de paridade, temos 33 bits. Essa vericação impede que o bit na posição 0 seja alterado.

            if (p[bit_falho] == '0'):
                p = muda_bit(p, bit_falho, 1)
            else:
                p = muda_bit(p, bit_falho, 0)

            if (p[bit_falho + 1] == '0'):
                p = muda_bit(p, bit_falho + 1, 1)
            else:
                p = muda_bit(p, bit_falho + 1, 0)

            if (p[bit_falho + 2] == '0'):
                p = muda_bit(p, bit_falho + 2, 1)
            else:
                p = muda_bit(p, bit_falho + 2, 0)




    if (tipo_falhas_inseridas != 'FALHA_SIMPLES' and tipo_falhas_inseridas != 'FALHA_DUPLA' and tipo_falhas_inseridas != 'FALHA_TRIPLA'):
        print("Opção inválida.\n")

    p = muda_bit(p, 0, 1)
    '''
    if codigo == 'PARIDADE_SIMPLES' or 'NENHUM':
       p = muda_bit(p, 0, 1)  # sinaliza que tem um erro nessa palavra
        
    if codigo == 'PARIDADE_MSB' or 'PARIDADE_2MSB':
       p = muda_bit(p, 0, 0)  # mantém a flag de erro igual a 0'''






    memoria_cache[linha_tlb_falha] = p  # substitui o valor binario codificado direto na list memoria_cache
    #print(memoria_cache)
    if debug:
        print("\nTipo de falha inserida:",tipo_falhas_inseridas)
        print("Falha inserida em ", endereco_falha, linha_tlb_falha, bit_falho, ".\n")
        print(memoria_cache)

    return 1


def ler_cache(memoria_cache, posicao, codigo):
    palavra = memoria_cache[posicao]
    # print("valor da cache",palavra)
    p, e = decodifica_palavra(palavra, codigo)
    return p, int(palavra[0])


def escreve_cache(memoria_cache, posicao, palavra, codigo):
    p = codifica_palavra(palavra, codigo)
    memoria_cache[posicao] = p
    # print("valor escrito na cache",p)


def codifica_palavra(palavra, codigo):
    """ pega um valor inteiro e põe em um código corretor de erro (binario no formato de string)
    Bit0 Bit1 Bit2-33
    E    P     DADOS
    E - indica que o um erro foi inserido na cache
    P - bit de paridade
    DADOS - dados armazenados
    Arguments:
      palavra {int} --
      codigo {int} -- seleciona um dos codigos disponíveis: PARIDADE_SIMPLES, PARIDADE_MSB, PARIDADE_2MSB
    Returns:
      [string] -- retorna um binário representado em string
    """
    if (codigo == 'NENHUM'):
        return codifica_nenhum(palavra)
    elif (codigo == 'PARIDADE_SIMPLES'):
        return codifica_paridade_simples(palavra)
    elif (codigo == 'PARIDADE_MSB'):
        return codifica_paridade_msb(palavra)
    elif (codigo == 'PARIDADE_2MSB'):
        return codifica_paridade_2msb(palavra)
    elif (codigo == 'PARIDADE_MSB4'):
        return codifica_paridade_msb4(palavra)
    elif (codigo == 'PARIDADE_MSB8'):
        return codifica_paridade_msb8(palavra)
    elif (codigo == 'PARIDADE_MSB12'):
        return codifica_paridade_msb12(palavra)
    elif (codigo == 'PARIDADE_MSB16'):
        return codifica_paridade_msb16(palavra)
    elif (codigo == 'PARIDADE_2MSB4'):
        return codifica_paridade_2msb4(palavra)
    elif (codigo == 'PARIDADE_2MSB8'):
        return codifica_paridade_2msb8(palavra)
    elif (codigo == 'PARIDADE_2MSB12'):
        return codifica_paridade_2msb12(palavra)
    else:
        return codifica_paridade_2msb16(palavra)  


def decodifica_palavra(palavra, codigo):
    """ pega uma palavra em um código corretor de erro (binario no formato de string) e transforma em inteiro
    Arguments:
      palavra {string} --  binario codificado
      codigo {int} -- seleciona um dos codigos disponíveis: PARIDADE_SIMPLES, PARIDADE_MSB, PARIDADE_2MSB
      erro {int} -- indica se houve erro na decodificação
    Returns:
      [int] -- retorna o valor inteiro decodificado
      [int] -- 1 erro, 0 sem erro
    """
    if (codigo == 'NENHUM'):
        return decodifica_nenhum(palavra)
    elif (codigo == 'PARIDADE_SIMPLES'):
        return decodifica_paridade_simples(palavra)
    elif (codigo == 'PARIDADE_MSB'):
        return decodifica_paridade_msb(palavra)
    elif (codigo == 'PARIDADE_2MSB'):
        return decodifica_paridade_2msb(palavra)
    elif (codigo == 'PARIDADE_MSB4'):
        return decodifica_paridade_msb4(palavra)
    elif (codigo == 'PARIDADE_MSB8'):
        return decodifica_paridade_msb8(palavra)
    elif (codigo == 'PARIDADE_MSB12'):
        return decodifica_paridade_msb12(palavra)
    elif (codigo == 'PARIDADE_MSB16'):
        return decodifica_paridade_msb16(palavra)
    elif (codigo == 'PARIDADE_2MSB4'):
        return decodifica_paridade_2msb4(palavra)
    elif (codigo == 'PARIDADE_2MSB8'):
        return decodifica_paridade_2msb8(palavra)
    elif (codigo == 'PARIDADE_2MSB12'):
        return decodifica_paridade_2msb12(palavra)
    else:
        return decodifica_paridade_2msb16(palavra)
    

def codifica_nenhum(palavra):
    return '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)


def decodifica_nenhum(palavra):
    b = BitArray(bin=palavra[1:])
    return b.int, 0


def codifica_paridade_msb(palavra):
    """Formato | E | PARIDADE (MSB) | RESTO DOS DADOS |
        PARIDADE é calculada com todos os bits de dados inclusive o MSB
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    p = calcula_paridade(word, 1)
    return muda_bit(word, 1, p)


def decodifica_paridade_msb(palavra):
    p = calcula_paridade(palavra, 1)
    p = muda_bit(palavra, 1, p)
    b = BitArray(bin=p[1:])
    return b.int, 0


def codifica_paridade_msb4(palavra):
    """Formato | E | PARIDADE (MSB com os 4 LSB) | RESTO DOS DADOS |
        PARIDADE é calculada com os 4 bits menos significativos de dados
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    p = calcula_paridade(word, 29)
    return muda_bit(word, 1, p)

def decodifica_paridade_msb4(palavra):
    p = calcula_paridade(palavra, 29)
    p = muda_bit(palavra, 1, p)
    b = BitArray(bin=p[1:])
    return b.int, 0

def codifica_paridade_msb8(palavra):
    """Formato | E | PARIDADE (MSB com os 8 LSB) | RESTO DOS DADOS |
        PARIDADE é calculada com os 8 bits menos significativos de dados
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    p = calcula_paridade(word, 25)
    return muda_bit(word, 1, p)

def decodifica_paridade_msb8(palavra):
    p = calcula_paridade(palavra, 25)
    p = muda_bit(palavra, 1, p)
    b = BitArray(bin=p[1:])
    return b.int, 0

def codifica_paridade_msb12(palavra):
    """Formato | E | PARIDADE (MSB com os 12 LSB) | RESTO DOS DADOS |
        PARIDADE é calculada com os 12 bits menos significativos de dados
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    p = calcula_paridade(word, 21)
    return muda_bit(word, 1, p)

def decodifica_paridade_msb12(palavra):
    p = calcula_paridade(palavra, 21)
    p = muda_bit(palavra, 1, p)
    b = BitArray(bin=p[1:])
    return b.int, 0


def codifica_paridade_msb16(palavra):
    """Formato | E | PARIDADE (MSB com os 16 LSB) | RESTO DOS DADOS |
        PARIDADE é calculada com os 16 bits menos significativos de dados
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    p = calcula_paridade(word, 17)
    return muda_bit(word, 1, p)

def decodifica_paridade_msb16(palavra):
    p = calcula_paridade(palavra, 17)
    p = muda_bit(palavra, 1, p)
    b = BitArray(bin=p[1:])
    return b.int, 0



def codifica_paridade_2msb(palavra):
    """Formato | E | PARIDADE EVEN (MSB) | PARIDADE ODD (MSB-1) | RESTO DOS DADOS |
        PARIDADE EVEN é calculada com bits 1,3,5,...
        PARIDADE ODD é calculada com bits 2,4,6,...
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    # calcula paridade dos bits 1,3,5,7,...,31
    sum = 0
    for i in range(1, len(word)):
        if (i % 2 != 0):
            sum = sum + int(word[i])
    p_even = sum % 2
    # calcula paridade dos bits 2,4,6,...,32
    sum = 0
    for i in range(1, len(word)):
        if (i % 2 == 0):
            sum = sum + int(word[i])
    p_odd = sum % 2
    word = muda_bit(word, 1, p_even)

    return muda_bit(word, 2, p_odd)

# odd é impar, even é par

def decodifica_paridade_2msb(palavra):
    # calcula paridade dos bits 1,3,5,7,...,31
    sum = 0
    for i in range(1, len(palavra)):
        if (i % 2 != 0):
            sum = sum + int(palavra[i])
    p_even = sum % 2
    # calcula paridade dos bits 2,4,6,...,32
    sum = 0
    for i in range(1, len(palavra)):
        if (i % 2 == 0):
            sum = sum + int(palavra[i])
    p_odd = sum % 2
    word = muda_bit(palavra, 1, p_even)
    word = muda_bit(word, 2, p_odd)

    b = BitArray(bin=word[1:])
    return b.int, 0

def codifica_paridade_2msb4(palavra):
    """Formato | E | PARIDADE EVEN (MSB) | PARIDADE ODD (MSB-1) | RESTO DOS DADOS |
        PARIDADE EVEN é calculada com bits 1 e 3
        PARIDADE ODD é calculada com bits 2 e 4
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    # calcula paridade dos bits 1 e 3
    sum = 0
    for i in range(29, len(word)):
        if (i % 2 != 0):
            sum = sum + int(word[i])
    p_even = sum % 2
    # calcula paridade dos bits 2 e 4
    sum = 0
    for i in range(29, len(word)):
        if (i % 2 == 0):
            sum = sum + int(word[i])
    p_odd = sum % 2
    word = muda_bit(word, 1, p_even)

    return muda_bit(word, 2, p_odd)


def decodifica_paridade_2msb4(palavra):
    # calcula paridade dos bits 1 e 3
    sum = 0
    for i in range(29, len(palavra)):
        if (i % 2 != 0):
            sum = sum + int(palavra[i])
    p_even = sum % 2
    # calcula paridade dos bits 2 e 4
    sum = 0
    for i in range(29, len(palavra)):
        if (i % 2 == 0):
            sum = sum + int(palavra[i])
    p_odd = sum % 2
    word = muda_bit(palavra, 1, p_even)
    word = muda_bit(word, 2, p_odd)

    b = BitArray(bin=word[1:])
    return b.int, 0

def codifica_paridade_2msb8(palavra):
    """Formato | E | PARIDADE EVEN (MSB) | PARIDADE ODD (MSB-1) | RESTO DOS DADOS |
        PARIDADE EVEN é calculada com bits 1, 3, 5 e 7
        PARIDADE ODD é calculada com bits 2, 4, 6 e 8
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    # calcula paridade dos bits 1, 3, 5 e 7
    sum = 0
    for i in range(25, len(word)):
        if (i % 2 != 0):
            sum = sum + int(word[i])
    p_even = sum % 2
    # calcula paridade dos bits 2, 4, 6 e 8
    sum = 0
    for i in range(25, len(word)):
        if (i % 2 == 0):
            sum = sum + int(word[i])
    p_odd = sum % 2
    word = muda_bit(word, 1, p_even)

    return muda_bit(word, 2, p_odd)


def decodifica_paridade_2msb8(palavra):
    # calcula paridade dos bits 1, 3, 5 e 7
    sum = 0
    for i in range(25, len(palavra)):
        if (i % 2 != 0):
            sum = sum + int(palavra[i])
    p_even = sum % 2
    # calcula paridade dos bits 2, 4, 6 e 8
    sum = 0
    for i in range(25, len(palavra)):
        if (i % 2 == 0):
            sum = sum + int(palavra[i])
    p_odd = sum % 2
    word = muda_bit(palavra, 1, p_even)
    word = muda_bit(word, 2, p_odd)

    b = BitArray(bin=word[1:])
    return b.int, 0

def codifica_paridade_2msb12(palavra):
    """Formato | E | PARIDADE EVEN (MSB) | PARIDADE ODD (MSB-1) | RESTO DOS DADOS |
        PARIDADE EVEN é calculada com bits 1, 3,..., 11
        PARIDADE ODD é calculada com bits 2, 4,..., 12
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    # calcula paridade dos bits 1, 3,..., 11.
    sum = 0
    for i in range(21, len(word)):
        if (i % 2 != 0):
            sum = sum + int(word[i])
    p_even = sum % 2
    # calcula paridade dos bits 2, 4,..., 12.
    sum = 0
    for i in range(21, len(word)):
        if (i % 2 == 0):
            sum = sum + int(word[i])
    p_odd = sum % 2
    word = muda_bit(word, 1, p_even)

    return muda_bit(word, 2, p_odd)


def decodifica_paridade_2msb12(palavra):
    # calcula paridade dos bits 1, 3,..., 11.
    sum = 0
    for i in range(21, len(palavra)):
        if (i % 2 != 0):
            sum = sum + int(palavra[i])
    p_even = sum % 2
    # calcula paridade dos bits 2, 4,..., 12.
    sum = 0
    for i in range(21, len(palavra)):
        if (i % 2 == 0):
            sum = sum + int(palavra[i])
    p_odd = sum % 2
    word = muda_bit(palavra, 1, p_even)
    word = muda_bit(word, 2, p_odd)

    b = BitArray(bin=word[1:])
    return b.int, 0

def codifica_paridade_2msb16(palavra):
    """Formato | E | PARIDADE EVEN (MSB) | PARIDADE ODD (MSB-1) | RESTO DOS DADOS |
        PARIDADE EVEN é calculada com bits 1, 3,..., 13 e 15
        PARIDADE ODD é calculada com bits 2, 4,..., 14 e 16
        E é o flag que indica se uma falha foi inserida nessa palavra
    """
    word = '{:033b}'.format(
        palavra & 0x0ffffffff)  # põe a palavra como 33 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    # calcula paridade dos bits 1, 3,..., 13 e 15.
    sum = 0
    for i in range(17, len(word)):
        if (i % 2 != 0):
            sum = sum + int(word[i])
    p_even = sum % 2
    # calcula paridade dos bits 2, 4,..., 14 e 16.
    sum = 0
    for i in range(17, len(word)):
        if (i % 2 == 0):
            sum = sum + int(word[i])
    p_odd = sum % 2
    word = muda_bit(word, 1, p_even)

    return muda_bit(word, 2, p_odd)


def decodifica_paridade_2msb16(palavra):
    # calcula paridade dos bits 1, 3,..., 13 e 15.
    sum = 0
    for i in range(17, len(palavra)):
        if (i % 2 != 0):
            sum = sum + int(palavra[i])
    p_even = sum % 2
    # calcula paridade dos bits 2, 4,..., 14 e 16.
    sum = 0
    for i in range(17, len(palavra)):
        if (i % 2 == 0):
            sum = sum + int(palavra[i])
    p_odd = sum % 2
    word = muda_bit(palavra, 1, p_even)
    word = muda_bit(word, 2, p_odd)

    b = BitArray(bin=word[1:])
    return b.int, 0


def codifica_paridade_simples(palavra):
    word = '{:034b}'.format(
        palavra & 0x1ffffffff)  # põe a palavra como 34 bits em binario {string}, deixo o bit 0 em 0 (flag de erro)
    p = calcula_paridade(word, 2)
    return muda_bit(word, 1, p)


def decodifica_paridade_simples(palavra):
    if (checa_paridade(palavra, 2, 1) == 1):  # detectamos um erro
        b = BitArray(bin=palavra[2:])  # houve erro, corrige invalidando a linha de cache
        return -1, 1
    else:
        b = BitArray(bin=palavra[2:])  # não houve erro
        return b.int, 0


def muda_bit(palavra, posicao, valor):
    """modifica o valor de um bit na posição de uma palavra. A palavra é um número binário representado por uma string
    Arguments:
      palavra -- binário representado em uma string
      posicao {int} -- posicao do bit que vai ser mudado, lembrando que o bit 0 é o MSB
      valor {int} -- valor 1 ou valor 0
    Returns:
      [string] -- retorna um binário representado em string
    """
    string_list = list(palavra)
    if (valor == 1):
        string_list[posicao] = '1'
    else:
        string_list[posicao] = '0'
    return "".join(string_list)


def calcula_paridade(palavra, posicao_inicial):
    """calcula a paridade par de um binario representado como string, assume que o bit posicao_inicial-1 é a paridade. então,
    calcula do bit posicao_inicial ao último
      DADOS - dados armazenados
    Arguments:
      palavra -- binário representado em uma string
      posicao_inicial -- posicao do primeiro bit de dados
    Returns:
      [int] -- retorna a paridade par
    """
    sum = 0
    for i in range(posicao_inicial, len(palavra)):
        sum = sum + int(palavra[i])
    return sum % 2


def checa_paridade(palavra, posicao_inicial, posicao_paridade):
    """checa a paridade par de um binario representado como string. A paridade fica no bit posicao_paridade, o primeiro
    bit de dados fica em posical_inicial
    Arguments:
      palavra -- binário representado em uma string
    Returns:
      [int] -- 1 erro, 0 sem erro
    """
    p = calcula_paridade(palavra, posicao_inicial)
    # print("paridade calculada",p)
    if (p == int(palavra[posicao_paridade])):
        # print("sem erro")
        return 0  # sem erro
    # print("com erro")
    return 1  # com erro



def existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria, codigo):
    """Verifica se existe na cache uma posição de memória que ainda não foi utilizada,
    se existir, essa posição é retornada.
    Arguments:
      memoria_cache {list} -- memória cache
      qtd_conjuntos {int} -- número de conjuntos da cache
      posicao_memoria {int} -- posição de memória que se quer armazenar na cache
    Returns:
      [int] -- com a primeira posição de memória vazia do conjunto
    """
    num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
    lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)

    # verifica se alguma das posições daquele conjunto está vazia
    for x in lista_posicoes:
        palavra, erro = ler_cache(memoria_cache, x, codigo)
        if palavra == -1:
            return x
    return -1


def get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos):
    """Retorna o número do conjunto onde essa posição de memória é sempre mapeada
    Arguments:
      posicao_memoria {int} -- posição de memória que se quer acessar
      qtd_conjuntos {int} -- número de conjuntos que a cache possui
    """
    return int(posicao_memoria) % int(qtd_conjuntos)


def print_cache_associativo(cache, codigo):
    """Imprime o estado da memória cache no modelo de mapeamento associativo.
    """
    print("+-------------------------------+")
    print("|Tamanho Cache: {:>16}| ".format(len(cache)))
    print("+-------------+-----------------+")
    print("|        Cache Associativo      |")
    print("+-------------+-----------------+")
    print("|Posição Cache | Posição Memória|")
    print("+-------------+-----------------+")
    for posicao, valor in cache.items():
        palavra, erro = ler_cache(cache, posicao, codigo)
        print("|{:>14}|{:>16}|".format(hex(posicao), hex(palavra)))
    print("+-------------+-----------------+")
    print(cache)


def print_cache_associativo_conjunto(cache, qtd_conjuntos, codigo):
    """Imprime o estado da memória cache no modelo de mapeamento associativo por conjunto.
    """
    print("+------------------------------+")
    print("|Tamanho: {:>21}|\n|Conjuntos: {:>19}|".format(len(cache), qtd_conjuntos))
    print("+------------------------------+")
    print("+  Cache Associativo Conjunto  +")
    print("+-------+-------+--------------+")
    print("|#\t| Cnj\t|   Pos Memória|")
    print("+-------+-------+--------------+")
    for posicao, valor in cache.items():
        num_conjunto = get_num_conjuno_posicao_memoria(posicao, qtd_conjuntos)
        palavra, erro = ler_cache(cache, posicao, codigo)
        print("|{} \t|{:4}\t|\t   {:>4}|".format(posicao, num_conjunto, palavra))
    print("+-------+-------+--------------+")
    print(cache)


def inicializar_cache(total_cache, codigo):
    """Cria uma memória cache zerada utilizando dicionários (chave, valor) e com
    valor padrão igual a '-1'
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
    Returns:
      [list] -- [dicionário]
    """
    # zera total a memória cache
    memoria_cache = {}

    # popula a memória cache com o valor -1, isso indica que a posição não foi usada
    for x in range(0, total_cache):
        # memoria_cache[x] = -1
        escreve_cache(memoria_cache, x, -1, codigo)

    return memoria_cache


def verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria, codigo):
    """Verifica se uma determinada posição de memória está na cache no modo associativo / associativo por conjunto
    Arguments:
      memoria_cache {list} -- memória cache
      qtd_conjuntos {int} -- número de conjuntos do cache
      posicao_memoria {int} -- posição que se deseja acessar
    """
    num_conjunto = int(posicao_memoria) % int(qtd_conjuntos)

    p = codifica_palavra(posicao_memoria, codigo)
    # CODIFICA A POSICAO MEMORIA PARA COMPARAR COM O CONTEUDO DA CAM DA TLB
    while num_conjunto < len(memoria_cache):
        d = memoria_cache[num_conjunto]
        if d[1:] == p[1:]:
            return num_conjunto, d[0]

        num_conjunto += qtd_conjuntos

    # não achou a posição de memória na cache
    return -1, p[0]


def get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos):
    """Retorna uma lista com todas as posições da memória cache que fazem parte de um determinado conjunto.
    Arguments:
      memoria_cache {list} -- memória cache
      num_conjunto {int} -- número do conjunto que se quer saber quais são os endereçamentos associados com aquele conjunto
      qtd_conjuntos {int} -- quantidade total de conjuntos possíveis na memória
    Returns:
      [list] -- lista de posições de memória associada com um conjunto em particular
    """
    lista_posicoes = []
    posicao_inicial = num_conjunto
    while posicao_inicial < len(memoria_cache):
        lista_posicoes.append(posicao_inicial)
        posicao_inicial += qtd_conjuntos
    return lista_posicoes


def politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria, codigo):
    """Nessa politica de substituição quando ocorre um HIT a posição vai para o topo da fila,
    se ocorrer um MISS remove o elemento 0 e a posição da cache onde a memória foi alocada é
    colocada no topo da fila
    Arguments:
      memoria_cache {list} -- memóiria cache
      qtd_conjuntos {int} -- quantidade de conjuntos
      posicao_memoria {int} -- posição de memória que será acessada
    """
    num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
    lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)

    # copiar os valores de cada posição da cache do conjunto em questão uma posição para traz
    for posicao_cache in lista_posicoes:
        proxima_posicao = posicao_cache + qtd_conjuntos
        if proxima_posicao < len(memoria_cache):
            # nesse caso, não precisa passar por escreve_cache e ler_cache, estamos copiando de uma posicao para outra
            memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]

    # coloca a posição que acabou de ser lida na topo da lista, assim, ela nesse momento é a última que será removida

    # memoria_cache[lista_posicoes[-1]] = posicao_memoria
    # a linha que vai ser substituída sempre está em lista_posicoes[0], o conteudo dessa linha vai ser apagado
    # por isso, a gente salva antes, para ver se a linha substituida tinha algum erro inserido
    # aqui a gente usa a função escreve_cache para que ele salve e deixe o bit ERRO zerado
    # estamos sobreescrevendo uma posição da cache, verifica se a posição salva estava com erro inserido
    # se tiver erro inserido retorna 1
    x = memoria_cache[lista_posicoes[0]]
    p, erro = ler_cache(memoria_cache, lista_posicoes[0], codigo)
    escreve_cache(memoria_cache, lista_posicoes[-1], posicao_memoria, codigo)

    if debug:
        print('Posição Memória: {}'.format(posicao_memoria))
        print('Posição da Cache: {}'.format(lista_posicoes[-1]))
        print('Erro ', erro)
        print('Valor da linha substituída', x)
        print('Conjunto: {}'.format(num_conjunto))
        print('Lista posições: {}'.format(lista_posicoes))
    return erro


def politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria, posicao_cache_hit, codigo):
    """Nessa politica de substituição quando ocorre um HIT a posição vai para o topo da fila,
    se ocorrer um MISS remove o elemento 0 e a posição da cache onde a memória foi alocada é
    colocada no topo da fila
    Arguments:
      memoria_cache {list} -- memóiria cache
      qtd_conjuntos {int} -- quantidade de conjuntos
      posicao_memoria {int} -- posição de memória que será acessada
      posicao_cache_hit {int} -- posição de memória cache onde o dados da memória principal está
    """
    num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
    lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)
    # salva o valor da posicao que foi acessada na cache em p
    p = memoria_cache[posicao_cache_hit]
    # copiar os valores de cada posição da cache do conjunto em questão uma posição para traz
    for posicao_cache in lista_posicoes:
        if posicao_cache_hit <= posicao_cache:
            # em uma cache com 4 conjuntos e 20 posições, as posições do 'conjunto 0' são:
            # [0, 4, 8, 12, 16], se o hit for na posição 4, então, então, será necessário copiar os dados da posição
            # 0 não faz nada
            # 4 <- 8
            # 8 <- 12
            # 12 <- 16
            # 16 <- 4
            proxima_posicao = posicao_cache + qtd_conjuntos
            if proxima_posicao < len(memoria_cache):
                # não preciso usar ler_cache, nem escreve_cache, copiando de uma posição para outra
                memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]

    # coloca no topo da pilha a posição de memória que acabou de ser lida
    memoria_cache[lista_posicoes[-1]] = p

    if debug:
        print("Posicao memoria", hex(posicao_memoria))
        print('Posição Memória: {}'.format(posicao_memoria))
        print('Conjunto: {}'.format(num_conjunto))
        print('Lista posições: {}'.format(lista_posicoes))


def executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar,
                                             politica_substituicao, codigo):
    """Executa a operação de mapeamento associativo, ou seja, não existe uma posição específica
    para o mapemento de uma posição de memória.
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
      qtd_conjuntos {int} -- quantidade de conjuntos na cache
      posicoes_memoria_para_acessar {list} -- quais são as posições de memória que devem ser acessadas
      politica_substituicao {str} -- Qual é a política para substituição caso a posição de memória desejada não esteja na cache E não exista espaço vazio
    """
    global erro

    memoria_cache = inicializar_cache(total_cache, codigo)

    # se o número de conjuntos for igual a zero, então estamos simulando
    # com a cache associativo!
    nome_mapeamento = 'Associativo'

    if (qtd_conjuntos == 1 and debug):
        print_cache_associativo(memoria_cache, codigo)
    else:
        if (debug):
            nome_mapeamento = 'Associativo Por Conjunto'
            print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, codigo)

    num_hit = 0
    num_miss = 0
    num_falso_positivo = 0
    posicao_cache_falhas = {}
    index = 0

    try:
        f = open(arquivo_acesso, "r")
        
        
    except IOError as identifier:
        print('\n\n------------------------------')
        print('ERRO: Arquivo \'{}\'não encontrado.'.format(arquivo_acesso))
        print('------------------------------')
        exit(-1)
        
    # percorre cada uma das posições de memória que estavam no arquivo
    #for index, posicao_memoria in enumerate(posicoes_memoria_para_acessar):
    #with open(filename, 'rb') as f:
    while True:
        line = f.readline()
        index = index + 1
        if not line:
            break
        posicao_memoria = int(line)
        
        gerar_falhas_cache(memoria_cache, index, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas,
                           codigo)

        if debug:
            print('\n\n\nInteração número: {}'.format(index + 1))
        # verificar se existe ou não a posição de memória desejada na cache, bem se o codigo detector de erro
        # identificou algum erro na leitura
        inserir_memoria_na_posicao_cache, erro = verifica_posicao_em_cache_associativo_conjunto(memoria_cache,
                                                                                                qtd_conjuntos,
                                                                                                posicao_memoria, codigo)

        # a posição desejada já está na memória
        if inserir_memoria_na_posicao_cache >= 0:
            num_hit += 1

            #num_falsos_positivos = verificar_falsos_positivos(posicoes_memoria_para_acessar, contador_falsos_positivos, total_cache)
            # verifica se a posição está na lista de posições falhas, se estiver incrementa o contador de falsos positivos
            # finaliza a simulação no primeiro falso positivo
            #print("Erro: ", erro)
            
            
            if debug:
                print('Cache HIT: posiçao de memória {}, posição cache {}'.format(hex(posicao_memoria),
                                                                                  hex(
                                                                                      inserir_memoria_na_posicao_cache)))
            
            if erro == 1:
                num_falso_positivo += 1
                print(r)
                #if debug:
            #print("Falso Positivo, posição", index)
                print_cache_associativo(memoria_cache, codigo)
                f.close()
                return 1 #ESSE RETURN AQUI FAZ PARAR A SIMULAÇÃO
            
           #print("Falso Positivo, posição", index)

                                                                        

            # se for LRU então toda vez que der um HIT será incrementado o contador daquela posição
            if politica_substituicao == 'LRU':
                politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria,
                                              inserir_memoria_na_posicao_cache, codigo)

        else:
            num_miss += 1
            #print("Erro: ", erro)
        

            if debug:
                print('Cache MISS: posiçao de memória {}'.format(hex(posicao_memoria)))

            # verifica se existe uma posição vazia na cache, se sim aloca nela a posição de memória
            posicao_vazia = existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria, codigo)

            if debug:
                print('Posição da cache ainda não utilizada: {}'.format(posicao_vazia))
                print('\nLeitura linha {}, posição de memória {}.'.format(index, hex(posicao_memoria)))

            ########
            # se posicao_vazia for < 0 então devemos executar as políticas de substituição
            ########
            if posicao_vazia >= 0:
                # memoria_cache[posicao_vazia] = posicao_memoria
                escreve_cache(memoria_cache, posicao_vazia, posicao_memoria, codigo)
                '''
            elif politica_substituicao == 'RANDOM':
                politica_substituicao_RANDOM(memoria_cache, qtd_conjuntos, posicao_memoria)
            elif politica_substituicao == 'FIFO':
                politica_substituicao_FIFO(memoria_cache, qtd_conjuntos, posicao_memoria)
            elif politica_substituicao == 'LFU':
                politica_substituicao_LFU(memoria_cache, qtd_conjuntos, posicao_memoria)'''
            elif politica_substituicao == 'LRU':
                erro = politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria, codigo)

        if erro == 1:  # se a linha com falha tiver sido lida, encerra a simulação
            #print("Posição com falha foi substituída: ", index)
           # return 0

            if debug:
                print("Posição com falha foi substituída: ", index)
            f.close()
            return 0 #ESSE RETURN AQUI FAZ PARAR A SIMULAÇÃO
        
        if qtd_conjuntos == 1:
            if debug:
                print_cache_associativo(memoria_cache, codigo)
        else:
            if debug:
                print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, codigo)

        if step:
            print('Tecle ENTER para processar o próximo passo:')
            input()

    if debug:
        print('\n\n-----------------')
        print('Resumo Mapeamento {}'.format(nome_mapeamento))
        print('-----------------')
        print('Política de Substituição: {}'.format(politica_substituicao))
        print('-----------------')
        #print('Total de memórias acessadas: {}'.format(len(posicoes_memoria_para_acessar)))
        print('Total HIT {}'.format(num_hit))
        print('Total MISS {}'.format(num_miss))
        #print('Total Falsos Positivos {}'.format(num_falso_positivo))
        #taxa_cache_hit = (num_hit / len(posicoes_memoria_para_acessar)) * 100
        #print('Taxa de Cache HIT {number:.{digits}f}%'.format(number=taxa_cache_hit, digits=2))

    f.close()
    return 0


def executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao, codigo):
    """O mapeamento associativo é um tipo de mapeamento associativo por conjunto
    ou o número de conjunto é igual a 1
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
      posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
      politica_substituicao {str} -- qual será a política de subistituição
    """
    # o número 1 indica que haverá apenas um único conjunto no modo associativo por conjunto
    # que é igual ao modo associativo padrão! :) SHAZAM
    return executar_mapeamento_associativo_conjunto(total_cache, 1, posicoes_memoria_para_acessar,
                                                    politica_substituicao, codigo)


def conversao_hexa_inteiro(origem, destino):
    try:
        a = open(origem, 'rt')
    except:
        print("Erro ao abrir o arquivo de endereços!")
    else:
        with open(destino, 'w') as b:
            for linha in a:
                aux = linha
                aux = linha.replace("\n", '')
                aux = int(aux)
                hexadecimal = (hex(aux))
                b.write(" \n", hexadecimal)


def criar_arquivo(nome):
    try:
        a = open(nome, 'a')
        a.close()
    except:
        print("Houve um erro na criação do arquivo.")


def verificar_falsos_positivos(memoria_cache, contador_falsos_positivos, index):
    for posicao in memoria_cache:
        for i in range(0, index-1):
            if memoria_cache[i] == posicao:
                contador_falsos_positivos += 1
                #print("Houve um falso positivo")
    return contador_falsos_positivos



def injetar_falsos_positivos(arq_binarios, tamanho_da_cache):
    try:
        a = open(arq_binarios, 'rt')
    except:
        print("Erro ao ler o arquivo.")
    else:
        nova = []
        for linha in a:
            dado = linha.split(';')
            dado[0] = dado[0].replace('\n', '')
            retirar = [" ", ",", "[", "]"]
            for i in dado[0]:
                if i not in retirar:
                    nova.append(i)
        tamanho_da_palavra = 31
        linha_injecao_de_erro = random.randint(0, tamanho_da_cache - 1)
        bit_injecao_de_erro = random.randint(2, tamanho_da_palavra)
        '''if nova[bit_injecao_de_erro] == "0":
            nova[bit_injecao_de_erro] = "1"
        else:
            nova[bit_injecao_de_erro] = "0"'''
        erro_aleatorio = str(random.randint(0, 1))
        if nova[bit_injecao_de_erro] != erro_aleatorio:
            print("Houve um erro aqui")
            print("Erro na linha", linha_injecao_de_erro," bit alterado: ",bit_injecao_de_erro)
        nova[bit_injecao_de_erro] = erro_aleatorio
        return nova


def conversao_inteiro_binario(origem, destino):
    try:
        a = open(origem, 'rt')
    except:
        print("Erro ao abrir o arquivo de endereços!")
    else:
        with open(destino, 'w') as b:
            for linha in a:
                aux = linha
                aux = linha.replace("\n", '')
                aux = int(aux)
                binario = (bin(aux))
                b.write(" \n", binario)


# at


##########################
# O programa começa aqui!
##########################
'''
# parse dos parâmetros passados no comando
parser = argparse.ArgumentParser(prog='Simulador de Cache')
parser.add_argument('--total_cache', required=True, type=int, help='Número total de posições da memória cache.')
parser.add_argument('--tipo_mapeamento', required=True,
                    help='Tipo do mapeamento desejado. Os valores aceitos para esse parâmetro são: DI / AS / AC.')
parser.add_argument('--politica_substituicao', default='ALL',
                    help='Qual será a política de substituição da cache que será utilizada. Os valores aceitos para esse parâmetro são: RANDOM / FIFO / LRU / LFU.')
parser.add_argument('--qtd_conjuntos', type=int, default=2,
                    help='Quando for escolhido o tipo de mapeamento AC deve-se informar quantos conjuntos devem ser criados dentro da memória cache.')
parser.add_argument('--arquivo_acesso', required=True, default='',
                    help='Nome do arquivo que possui as posições da memória principal que serão acessadas. Para cada linha do arquivo deve-se informar um número inteiro.')
parser.add_argument('--debug', default=0,
                    help='Por padrão vem setado como 0, caso queira exibir as mensagens de debugs basta passar --debug 1.')
parser.add_argument('--step', default=0,
                    help='Solicita a interação do usuário após cada linha processada do arquivo --step 1.')
parser.add_argument('--codigo', default='PARIDADE_SIMPLES',
                    help='Qual código será utilizado na TLB: NENHUM, PARIDADE, MSB_1, MSB_2')
parser.add_argument('--endereco_falha', default=0,
                    help='Número de falhas a serem inseridas na simulação')
parser.add_argument('--linha_tlb_falha', default=0,
                    help='Número de falhas a serem inseridas na simulação')
parser.add_argument('--bit_falho', default=0,
                    help='Frequência na qual as falhas são inseridas')
parser.add_argument('--tipo_falhas_inseridas', default=0,
                    help='Tipo de falhas inseridas. Os parâmetros são: FALHA_SIMPLES, FALHA_DUPLA, FALHA_TRIPLA')
args = parser.parse_args()
# recuperar todos os parâmetros passados
total_cache = args.total_cache
tipo_mapeamento = args.tipo_mapeamento
arquivo_acesso = args.arquivo_acesso
qtd_conjuntos = args.qtd_conjuntos
politica_substituicao = args.politica_substituicao.upper()
debug = args.debug
step = args.step
codigo = args.codigo
endereco_falha = int(args.endereco_falha)
linha_tlb_falha = int(args.linha_tlb_falha)
bit_falho = int(args.bit_falho)
tipo_falhas_inseridas = (args.tipo_falhas_inseridas)
'''

total_cache = 0
tipo_mapeamento = 'AC'
arquivo_acesso = " "
qtd_conjuntos = 1
politica_substituicao = 'LRU'
debug = 1
step = 0
codigo = " "
endereco_falha = 0
linha_tlb_falha = 0
bit_falho = 0 
tipo_falhas_inseridas = 0

# Ambiente controlado para teste com o script de repetição
def executaSimulador(xtotal_cache, xarquivo_acesso, xdebug, xcodigo, xendereco_falha, xlinha_tlb_falha, xbit_falho, xtipo_falhas_inseridas):
    global total_cache, arquivo_acesso, debug, codigo, endereco_falha, linha_tlb_falha, bit_falho, tipo_falhas_inseridas, r
    total_cache = xtotal_cache
    tipo_mapeamento = 'AC'
    arquivo_acesso = xarquivo_acesso
    qtd_conjuntos = 1
    politica_substituicao = 'LRU'
    debug = xdebug
    step = 0
    codigo = xcodigo
    endereco_falha = xendereco_falha
    linha_tlb_falha = xlinha_tlb_falha
    bit_falho = xbit_falho 
    tipo_falhas_inseridas = xtipo_falhas_inseridas



    if qtd_conjuntos <= 0:
        print('\n\n------------------------------')
        print('ERRO: O número de conjuntos não pode ser 0.')
        print('------------------------------')
        exit()

    if arquivo_acesso == '':
        print('\n\n------------------------------')
        print(
            'ERRO: É necesário informar o nome do arquivo que será processado, o parâmetro esperado é --arquivo_acesso seguido do nome do arquivo.')
        print('------------------------------')
        exit()

    # lê o arquivo e armazena cada uma das posições de memória que será lida em uma lista
    posicoes_memoria_para_acessar = []

    '''if len(posicoes_memoria_para_acessar) == 0:
        print('\n\n------------------------------')
        print('ERRO: o arquivo {} não possui nenhuma linha com números inteiros.'.format(arquivo_acesso))
        print('------------------------------')
        exit(-1)'''

    if debug:
        print('+====================+')
        print('| SIMULADOR DE TLB |')
        print('+====================+')
        print('+ Setando parâmetros iniciais da TLB+')

    if tipo_mapeamento == 'AS':
        r = executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao, codigo)

        
    elif tipo_mapeamento == 'AC':
        # o número de conjuntos deve ser um divisor do total da memória
        if total_cache % qtd_conjuntos != 0:
            print('\n\n------------------------------')
            print(
                'ERRO: O número de conjuntos {} deve ser obrigatoriamente um divisor do total de memória cache disponível {}.'.format(
                    qtd_conjuntos, total_cache))
            print('------------------------------')
            exit(-1)
        r = executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar,
                                                     politica_substituicao, codigo)
    else:
        print('\n\n------------------------------')
        print(
            'ERRO: O tipo de mapeamento \'{}\'não foi encontrado. \nOs valores possíveis para o parâmetro --tipo_mapeamento são: DI / AS / AC'.format(
                tipo_mapeamento))
        print('------------------------------')
        exit(-1)
    
    if debug:
        print('\n')
        print('-' * 80)
        print('Parâmetros da Simulação')
        print('-' * 80)
        print("Arquivo com as posições de memória: {}".format(arquivo_acesso))
        print('Número de posições de memória: {}'.format(len(posicoes_memoria_para_acessar)))
        print('Tamanho total da cache: {}'.format(total_cache))
        print("Tipo Mapeamento: {}".format(tipo_mapeamento))
        if tipo_mapeamento != 'AS':
            print("Quantidade de Conjuntos: {}".format(qtd_conjuntos))
        print("Política de Substituição: {}".format(politica_substituicao))
        print("Debug: {}".format(debug))
        print("Step: {}".format(step))
        print("Tipo de falha inserida: ", tipo_falhas_inseridas)
        print("Falha inserida em ", endereco_falha, linha_tlb_falha, bit_falho)
        #print("Número falsos positivos: ", r)
        print('-' * 80)

    return r
