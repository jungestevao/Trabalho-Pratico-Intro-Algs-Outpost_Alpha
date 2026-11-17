import ast
from src.config import DADOS

def iniciar_dados(arquivo = DADOS):
    """
    Confere se existe um dicionário pra iniciar um ou não:

    Parâmetros:
        arquivo (str): Caminho do arquivo de dados
    
    Saída:
        None
    """
    dic = {}
    formato_dados = ["tela","abertura","fase", 1,"erros", 0,"acertos",0,"historia",True,"volume",0.8]

    try:
        with open(arquivo,"r",encoding="utf-8"):
            print("Arquivo aberto")

    except FileNotFoundError:
        with open(arquivo,"w",encoding="utf-8")as arquivo:
            for i in range(0, len(formato_dados),2):
                  arquivo.write(f"{formato_dados[i]},{formato_dados[i+1]}\n")

def ler_dados(arquivo):
    """
    Lê os dados em data/dados_jogador.txt e transforma em dicionário.

    Parâmentros:
        arquivo (str): caminho do arquivo.

    Saída:
        (Dict): dicionário com o nome dos dados em chaves e seu valor atribuído.
    """
    dic = {}

    with open(arquivo,"r",encoding="utf-8")as dados:
        for linha in dados:
            chave,dado = linha.strip().split(",")

            try:
                dic[chave] = ast.literal_eval(dado)
            except (ValueError, SyntaxError):
                dic[chave] = dado
                

    return dic

def registrar_dados(dicionario,arquivo):
    """
    Lê os dados do dicionário local e registra em arquivo

    Parâmetros:
        dicionário(dict): dicionário com os dados organizados.
    
    Saídas: 
        None

    OBS: Após o fim da execução, o arquivo é atualizado.
    """
    with open(arquivo,"w",encoding="utf-8")as dados:
        for chave in dicionario.keys():
            dados.write(f"{chave},{dicionario[chave]}\n")

def iniciar_personagens(dados_personagens = "data/dados_personagens.txt"):

    dic = {}

    with open(dados_personagens, "r", encoding="utf-8") as dados:
        q_personagens = int(dados.readline().strip())
        q_dados = int(dados.readline().strip())
        for i in range(q_personagens):
            chave_nome, nome = dados.readline().strip().split(":")
            nome = nome.lstrip()
            dic[nome] = {}
            for j in range(q_dados):
                linha = dados.readline()
                chave, resto = linha.strip().split(":")
                dado = resto.split(",")
                if len(dado) == 1:
                    try:
                        dado = ast.literal_eval(dado[0])
                    except (ValueError, SyntaxError):
                        dado = dado[0]
                try:
                    dic[nome][chave] = ast.literal_eval(dado)
                except (ValueError,SyntaxError):
                    dic[nome][chave] = dado
            dados.readline()
    return dic

print(iniciar_personagens())