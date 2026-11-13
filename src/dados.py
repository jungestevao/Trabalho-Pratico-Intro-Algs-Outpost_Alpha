def ler_dados(arquivo):
    """
    Lê os dados em data/dados_jogador.txt e transforma em dicionário.

    Parâmentros:
        arquivo (str): caminho do arquivo.

    Saída:
        (Dict): dicionário com o nome dos dados em chaves e seu valor atribuído.
    """
    dic = {}
    formato_dados = ["fase", 1,"erros", 0,"acertos",0,"historia",True]
    try:
        with open(arquivo,"r",encoding="utf-8")as arquivo:
            for linha in arquivo:
                chave,dado = linha.strip().split(",")
                dic[chave] = dado
                

    except FileNotFoundError:
        with open(arquivo,"w",encoding="utf-8")as arquivo:
            for i in range(0, len(formato_dados),2):
                  dic[formato_dados[i]] = formato_dados[i+1]

    return dic

def registrar_dados(dicionario,arquivo):
    """
    Lê os dados do dicionário local e registra em arquivo

    Parâmetros:
        dicionário(dict): dicionário com os dados organizados.
    
    Saídas: 
        Nada

    OBS: Após o fim da execução, o arquivo é atualizado.
    """
