from bitstring import BitArray

def ler_cache(memoria_cache, posicao, codigo):	
	palavra = memoria_cache[posicao]
	p, e = decodifica_palavra(palavra,codigo)
	return p, int(palavra[0])

def escreve_cache(memoria_cache, posicao, palavra, codigo):
	p = codifica_palavra(palavra,codigo)
	memoria_cache[posicao] = p

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
	#print("Palavra em bits", word)
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
    if (checa_paridade(palavra)==1):
    	return 0,1
    else:
    	b = BitArray(bin=palavra[2:])
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

b = -1


memoria_cache = {}

escreve_cache(memoria_cache,0,-1,0)
print(memoria_cache)
p,erro = ler_cache(memoria_cache,0,0)

print("Valor armazenado na cache", p)
