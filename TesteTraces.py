#Esse código foi feito pra tratar os traces que a gente conseguiu no http://traces.cs.umass.edu/index.php/CpuMem/CpuMem
#Os traces vem no formato: A B C D, em que A, B e D são números em hexadecimal e C é R para leitura ou W para escrita. Além disso, apenas D indica o endereço que queremos
#Portano, a função abaixo é pra capturar apenas o D e converter em número inteiro

def ler_arquivo(traces_hexadecimal, traces_inteiros):
    try:
        a = open(traces_hexadecimal, 'r')
    except:
        print("Arquivo não encontrado!")
    else:
        contador = 0
        posicoes_valores = {"posição": 0, "valor": 0}
        for linha in a:
            dado_inteiro = []
            dado = linha.split() 
            espaco = [" "] #O trace usa o espaço (" ") para separar as partes A, B, C e D
            for i in linha:
                if i in espaco:
                    contador += 1 #Conta os espaços em cada linha
                    if contador == 3: #No terceito espaço contado, chegou em D
                        aux = int(dado[3], 16) 
                        dado_inteiro.append(aux)
                        contador = 0 #Reinicia a contagem, antes de ir para a linha de baixo
                        with open(traces_inteiros, 'at') as b:
                            b.write(f'{aux}\n') 


def criar_arquivo(nome):
    try:
        a = open(nome, 'a')
        a.close()
    except:
        print("Houve um erro na criação do arquivo.")


arq = "traces.txt" 
arq_inteiros = "tracesInteiros.txt"
ler_arquivo(arq, arq_inteiros)
criar_arquivo("tracesInteiros.txt")
