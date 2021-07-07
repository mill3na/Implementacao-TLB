# protótipo 1.0 da função de leitura do arquivo linha por linha. No código, a extensão está .txt, mas também rodou com .out

def ler_arquivo_linha_por_linha(origem):
    try:
        a = open(origem, 'r')
    except:
        print("Arquivo não encontrado!")
    else:
        tempoinicial = time()
        contador = 0
        dados = []
        for linha in a:
            contador += 1
            j = (int(a.readline(6)))
            print(j)
            dados.append(j)
            if (contador == 1000):
                break
        print(dados)
        tempofinal = time()
        print(f"Tempo de execução: {tempofinal - tempoinicial}")
