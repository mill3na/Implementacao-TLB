import argparse, random, re
from bitstring import BitArray

contador_falsos_positivos = 0
arq_binarios = "enderecosBinarios.txt"

#
#
#

def gerar_falhas_cache(memoria_cache, index):
    """essa é uma versão café com leite que gera falha no index=4
    posição 0, bit 3 (posicao 29)
    """
    if ( index != 4 ):
        return -1
    print(memoria_cache)        
    
    p = memoria_cache[0] #pega o valor binario codificado direto na list memoria_cache
    if ( p[33]=='0'):
        p=muda_bit(p,33,1)
        p=muda_bit(p,32,1)
    else:
        p=muda_bit(p,33,0)
        p=muda_bit(p,32,0)

    p=muda_bit(p,0,1) #sinaliza que tem um erro nessa palavra

    
    memoria_cache[0] = p #substitui o valor binario codificado direto na list memoria_cache
    print(memoria_cache)

    if qtd_conjuntos == 1:
        print_cache_associativo(memoria_cache)
    else:
        nome_mapeamento = 'Associativo Por Conjunto'
        print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)    
    
    return 1


def ler_cache(memoria_cache, posicao, codigo):  
    palavra = memoria_cache[posicao]
    #print("valor da cache",palavra)
    p, e = decodifica_palavra(palavra,codigo)
    return p, int(palavra[0])

def escreve_cache(memoria_cache, posicao, palavra, codigo):
    p = codifica_palavra(palavra,codigo)
    memoria_cache[posicao] = p
    #print("valor escrito na cache",p)

def codifica_palavra(palavra, codigo):
    """ pega um valor inteiro e põe em um código corretor de erro (binario no formato de string)
    Bit0 Bit1 Bit2-33
    E    P     DADOS
    E - indica que o um erro foi inserido na cache
    P - bit de paridade
    DADOS - dados armazenados
    Arguments:
      palavra {int} -- 
      codigo {int} -- seleciona um dos codigos disponíveis, no momento apenas paridade simples
    Returns:
      [string] -- retorna um binário representado em string
    """
    word = '{:034b}'.format(palavra& 0x3ffffffff) #põe a palavra como 34 bits em binario {string}
    p = calcula_paridade(word)
    return muda_bit(word,1,p)

def decodifica_palavra(palavra,codigo):
    """ pega uma palavra em um código corretor de erro (binario no formato de string) e transforma em inteiro
    Arguments:
      palavra {string} --  binario codificado
      codigo {int} -- seleciona um dos codigos disponíveis, no momento apenas paridade simples
      erro {int} -- indica se houve erro na decodificação
    Returns:
      [int] -- retorna o valor inteiro decodificado
      [int] -- 1 erro, 0 sem erro
    """
    if (checa_paridade(palavra)==1):#detectamos um erro
        b = BitArray(bin=palavra[2:]) #houve erro, corrige invalidando a linha de cache
        return -1, 1
    else:
        b = BitArray(bin=palavra[2:]) #não houve erro
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
    if ( valor == 1 ):
        string_list[posicao] = '1'
    else:
        string_list[posicao] = '0'
    return "".join(string_list)  

def calcula_paridade(palavra):
    """calcula a paridade par de um binario representado como string, assume que o bit 1 [MSB+1] é a paridade. então,
    calcula do bit 1 ao último
    Bit0 Bit1 Bit2-33
    E    P     DADOS
    E - indica que o um erro foi inserido na cache
    P - bit de paridade
    DADOS - dados armazenados
    Arguments:
      palavra -- binário representado em uma string
    Returns:
      [int] -- retorna a paridade par
    """ 
    sum = 0
    for i in range(2,len(palavra)):
        sum = sum + int(palavra[i])
    return sum%2

def checa_paridade(palavra):
    """checa a paridade par de um binario representado como string. A paridade fica no bit 1 (MSB+1, bit mais a esquerda da string)
    Arguments:
      palavra -- binário representado em uma string
    Returns:
      [int] -- 1 erro, 0 sem erro
    """     
    p = calcula_paridade(palavra)   
    #print("paridade calculada",p)
    if ( p == int(palavra[1])):
        #print("sem erro")
        return 0 #sem erro
    #print("com erro")
    return 1 #com erro  

"""comando de teste: python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=enderecosInteiros.txt --debug 1 --politica_substituicao LRU"""
def existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria):
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
        palavra, erro = ler_cache(memoria_cache,x,0)
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


def print_cache_associativo(cache):
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
        palavra,erro = ler_cache(cache, posicao, 0)
        print("|{:>14}|{:>16}|".format(hex(posicao), hex(palavra)))
    print("+-------------+-----------------+")


def print_cache_associativo_conjunto(cache, qtd_conjuntos):
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
        palavra,erro = ler_cache(cache, posicao, 0)
        print("|{} \t|{:4}\t|\t   {:>4}|".format(posicao, num_conjunto, palavra))
    print("+-------+-------+--------------+")


def inicializar_cache(total_cache):
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
        #memoria_cache[x] = -1
        escreve_cache(memoria_cache,x,-1,0)

    return memoria_cache


def verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria, ):
    """Verifica se uma determinada posição de memória está na cache no modo associativo / associativo por conjunto
    Arguments:
      memoria_cache {list} -- memória cache
      qtd_conjuntos {int} -- número de conjuntos do cache
      posicao_memoria {int} -- posição que se deseja acessar
    """
    num_conjunto = int(posicao_memoria) % int(qtd_conjuntos)
    print("numero de conjunto", num_conjunto)

    while num_conjunto < len(memoria_cache):
        palavra, erro = ler_cache(memoria_cache, num_conjunto,0)
        if palavra == posicao_memoria:
            return num_conjunto, erro

        num_conjunto += qtd_conjuntos

    # não achou a posição de memória na cache
    return -1, erro


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

def politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria):
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
            #nesse caso, não precisa passar por escreve_cache e ler_cache, estamos copiando de uma posicao para outra
            memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]
            
    # coloca a posição que acabou de ser lida na topo da lista, assim, ela nesse momento é a última que será removida


    #memoria_cache[lista_posicoes[-1]] = posicao_memoria
    #aqui a gente usa a função escreve_cache para que ele salve e deixe o bit ERRO zerado
    #estamos sobreescrevendo uma posição da cache
    escreve_cache(memoria_cache,lista_posicoes[-1],posicao_memoria,0)

    if debug:
        print('Posição Memória: {}'.format(posicao_memoria))
        print('Conjunto: {}'.format(num_conjunto))
        print('Lista posições: {}'.format(lista_posicoes))


def politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria, posicao_cache_hit):
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
    #salva o valor da posicao que foi acessada na cache em p
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
                #não preciso usar ler_cache, nem escreve_cache, copiando de uma posição para outra
                memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]


    # coloca no topo da pilha a posição de memória que acabou de ser lida
    memoria_cache[lista_posicoes[-1]] = p
    print("Posicao memoria", hex(posicao_memoria))

    if debug:
        print('Posição Memória: {}'.format(posicao_memoria))
        print('Conjunto: {}'.format(num_conjunto))
        print('Lista posições: {}'.format(lista_posicoes))


def executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar,
                                             politica_substituicao='RANDOM'):
    """Executa a operação de mapeamento associativo, ou seja, não existe uma posição específica
    para o mapemento de uma posição de memória.
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
      qtd_conjuntos {int} -- quantidade de conjuntos na cache
      posicoes_memoria_para_acessar {list} -- quais são as posições de memória que devem ser acessadas
      politica_substituicao {str} -- Qual é a política para substituição caso a posição de memória desejada não esteja na cache E não exista espaço vazio
    """

    memoria_cache = inicializar_cache(total_cache)

    # se o número de conjuntos for igual a zero, então estamos simulando
    # com a cache associativo!
    nome_mapeamento = 'Associativo'
    if qtd_conjuntos == 1:
        print_cache_associativo(memoria_cache)
    else:
        nome_mapeamento = 'Associativo Por Conjunto'
        print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)
    

    num_hit = 0
    num_miss = 0
    num_falso_positivo = 0
    posicao_cache_falhas = {}


    # percorre cada uma das posições de memória que estavam no arquivo
    for index, posicao_memoria in enumerate(posicoes_memoria_para_acessar):
        #
        #TODO
        #Lógica de inserção de falhas tem que ser inserida aqui
        #O ideal é inserir falhas aleatoriamente com uma dada taxa
        #1 falha em 10.000 acessos, etc
        #
        #Nessa versão estou inserindo uma falha na 4° interação
        #bit 3, posição 0 da cache
        #
        gerar_falhas_cache(memoria_cache, index)

        print('\n\n\nInteração número: {}'.format(index + 1))
        # verificar se existe ou não a posição de memória desejada na cache, bem se o codigo detector de erro
        #identificou algum erro na leitura
        inserir_memoria_na_posicao_cache, erro = verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria)

        # a posição desejada já está na memória
        if inserir_memoria_na_posicao_cache >= 0:
            num_hit += 1
            #
            #verifica se a posição está na lista de posições falhas, se estiver incrementa o contador de falsos positivos
            #
            if ( erro == 1 ):
                num_falso_positivo+=1

            print('Cache HIT: posiçao de memória {}, posição cache {}'.format(hex(posicao_memoria),
                                                                              hex(inserir_memoria_na_posicao_cache)))

          # se for LFU então toda vez que der um HIT será incrementado o contador daquela posição
            """if politica_substituicao == 'LFU':
                contador_lfu[inserir_memoria_na_posicao_cache] += 1
                imprimir_contador_lfu()"""

            # se for LRU então toda vez que der um HIT será incrementado o contador daquela posição
            if politica_substituicao == 'LRU':
                politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria,
                                              inserir_memoria_na_posicao_cache)

        else:
            num_miss += 1
            print('Cache MISS: posiçao de memória {}'.format(hex(posicao_memoria)))

            # verifica se existe uma posição vazia na cache, se sim aloca nela a posição de memória
            posicao_vazia = existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria)

            if debug:
                print('Posição da cache ainda não utilizada: {}'.format(posicao_vazia))
                print('\nLeitura linha {}, posição de memória {}.'.format(index, hex(posicao_memoria)))

            ########
            # se posicao_vazia for < 0 então devemos executar as políticas de substituição
            ########
            if posicao_vazia >= 0:
                #memoria_cache[posicao_vazia] = posicao_memoria
                escreve_cache(memoria_cache, posicao_vazia, posicao_memoria, 0)
                '''
            elif politica_substituicao == 'RANDOM':
                politica_substituicao_RANDOM(memoria_cache, qtd_conjuntos, posicao_memoria)
            elif politica_substituicao == 'FIFO':
                politica_substituicao_FIFO(memoria_cache, qtd_conjuntos, posicao_memoria)
            elif politica_substituicao == 'LFU':
                politica_substituicao_LFU(memoria_cache, qtd_conjuntos, posicao_memoria)'''
            elif politica_substituicao == 'LRU':
                politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria)

        if qtd_conjuntos == 1:
            print_cache_associativo(memoria_cache)
        else:
            print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)

        if step:
            print('Tecle ENTER para processar o próximo passo:')
            input()

    print('\n\n-----------------')
    print('Resumo Mapeamento {}'.format(nome_mapeamento))
    print('-----------------')
    print('Política de Substituição: {}'.format(politica_substituicao))
    print('-----------------')
    print('Total de memórias acessadas: {}'.format(len(posicoes_memoria_para_acessar)))
    print('Total HIT {}'.format(num_hit))
    print('Total MISS {}'.format(num_miss))
    print('Total Falsos Positivos {}'.format(num_falso_positivo))
    taxa_cache_hit = (num_hit / len(posicoes_memoria_para_acessar)) * 100
    print('Taxa de Cache HIT {number:.{digits}f}%'.format(number=taxa_cache_hit, digits=2))


def executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao):
    """O mapeamento associativo é um tipo de mapeamento associativo por conjunto
    ou o número de conjunto é igual a 1
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
      posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
      politica_substituicao {str} -- qual será a política de subistituição
    """
    # o número 1 indica que haverá apenas um único conjunto no modo associativo por conjunto
    # que é igual ao modo associativo padrão! :) SHAZAM
    executar_mapeamento_associativo_conjunto(total_cache, 1, posicoes_memoria_para_acessar, politica_substituicao)


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
                b.write(f'{hexadecimal}\n')



def criar_arquivo (nome):
    try:
        a = open(nome, 'a')
        a.close()
    except:
        print("Houve um erro na criação do arquivo.")



def verificar_falsos_positivos(memoria_cache, contador_falsos_positivos):
    for posicao, valor in memoria_cache.items():
        for posicao2, valor2 in memoria_cache.items():
            # print(f'Valor for externo: {valor}.\nValor for interno: {valor2}.')
            if (valor == valor2) and (posicao != posicao2):
                contador_falsos_positivos += 1
                # print("Houve um falso positivo!\n")
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
            print(f'\033[31mHouve um erro aqui.\033[m')
            print(f'Erro na linha {linha_injecao_de_erro}, bit alterado: {bit_injecao_de_erro}.')
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
                b.write(f'{binario}\n')
#at


##########################
# O programa começa aqui!
##########################

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

args = parser.parse_args()

# recuperar toos os parâmetros passados
total_cache = args.total_cache
tipo_mapeamento = args.tipo_mapeamento
arquivo_acesso = args.arquivo_acesso
qtd_conjuntos = args.qtd_conjuntos
politica_substituicao = args.politica_substituicao.upper()
debug = args.debug
step = args.step

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
try:
    f = open(arquivo_acesso, "r")
    posicoes_memoria_para_acessar = []
    for posicao_memoria in f:
        posicoes_memoria_para_acessar.append(int(re.sub(r"\r?\n?$", "", posicao_memoria, 1)))
    f.close()
except IOError as identifier:
    print('\n\n------------------------------')
    print('ERRO: Arquivo \'{}\'não encontrado.'.format(arquivo_acesso))
    print('------------------------------')
    exit()

if len(posicoes_memoria_para_acessar) == 0:
    print('\n\n------------------------------')
    print('ERRO: o arquivo {} não possui nenhuma linha com números inteiros.'.format(arquivo_acesso))
    print('------------------------------')
    exit()

print('+====================+')
print('| SIMULADOR DE CACHE |')
print('+====================+')
print('+ Setando parâmetros iniciais da cache+')

if tipo_mapeamento != 'DI':
    if politica_substituicao != 'RANDOM' and politica_substituicao != 'FIFO' and politica_substituicao != 'LRU' and politica_substituicao != 'LFU' and politica_substituicao != 'ALL':
        print('\n\n------------------------------')
        print('ERRO: A política de substituição {} não existe.'.format(politica_substituicao))
        print('------------------------------')
        exit()


if tipo_mapeamento == 'AS':
    if (politica_substituicao == 'ALL'):
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'RANDOM')
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'FIFO')
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'LRU')
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'LFU')
    else:
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao)

elif tipo_mapeamento == 'AC':
    # o número de conjuntos deve ser um divisor do total da memória
    if total_cache % qtd_conjuntos != 0:
        print('\n\n------------------------------')
        print(
            'ERRO: O número de conjuntos {} deve ser obrigatoriamente um divisor do total de memória cache disponível {}.'.format(
                qtd_conjuntos, total_cache))
        print('------------------------------')
        exit()

    if (politica_substituicao == 'ALL'):
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'RANDOM')
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'FIFO')
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'LRU')
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'LFU')
    else:
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar,
                                                 politica_substituicao)
else:
    print('\n\n------------------------------')
    print(
        'ERRO: O tipo de mapeamento \'{}\'não foi encontrado. \nOs valores possíveis para o parâmetro --tipo_mapeamento são: DI / AS / AC'.format(
            tipo_mapeamento))
    print('------------------------------')
    exit()

if debug:
    print('\n')
    print('-' * 80)
    print('Parâmetros da Simulação')
    print('-' * 80)
    print("Arquivo com as posições de memória: {}".format(arquivo_acesso))
    print('Número de posições de memória: {}'.format(len(posicoes_memoria_para_acessar)))
    print('As posições são: {}'.format(posicoes_memoria_para_acessar))
    print('Tamanho total da cache: {}'.format(total_cache))
    print("Tipo Mapeamento: {}".format(tipo_mapeamento))
    if tipo_mapeamento != 'AS':
        print("Quantidade de Conjuntos: {}".format(qtd_conjuntos))
    print("Política de Substituição: {}".format(politica_substituicao))
    print("Debug: {}".format(debug))
    print("Step: {}".format(step))
    print('-' * 80)

