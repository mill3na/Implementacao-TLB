def ler_arquivo(traces_hexadecimal, traces_inteiros):
    try:
        a = open(traces_hexadecimal, 'r')
    except:
        print("Não sei cadê o arquivo.")
    else:
        contador = 0
        posicoes_valores = {"posição": 0, "valor": 0}
        for linha in a:
            dado_inteiro = []
            dado = linha.split()
            espaco = [" "]
            for i in linha:
                if i in espaco:
                    contador += 1
                    if contador == 3:
                        aux = int(dado[3], 16)
                        dado_inteiro.append(aux)
                        contador = 0
                        #print(aux)
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
