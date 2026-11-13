import pygame


from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    FONTE_TITULO,
    DADOS
)
from src.funcoes import (
    fechar_jogo,
    executar_abertura,
    executar_menu
)
from src.historia import (
    executar_historia
)
from src.dados import(
    iniciar_dados,
    ler_dados,
    registrar_dados,
)

def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""

    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))

    clock = pygame.time.Clock()

    pygame.display.set_caption(TITULO_JOGO)

    estado_atual = "iniciando"

    iniciar_dados(DADOS)

    while True:

        # Verificação de estado (mudança de telas)
        estado_memoria = ler_dados(DADOS)
        print(estado_memoria)

        if estado_memoria["tela"] == "abertura":
            executar_abertura(tela,clock,estado_memoria)
        elif estado_memoria["tela"] == "menu":
            executar_menu(tela,clock,estado_memoria)
        elif estado_memoria["tela"] == "historia":
            executar_historia(tela,clock,estado_memoria, True)