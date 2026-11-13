import pygame
import src

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    FONTE_TITULO,
)
from src.funcoes import (
    fechar_jogo,
    executar_abertura,
    executar_menu
)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""

    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))

    clock = pygame.time.Clock()

    pygame.display.set_caption(TITULO_JOGO)

    estado_atual = "iniciando"

    while True:

        # Verificação de estado (mudança de telas)

        if estado_atual == "iniciando":
            estado_atual = executar_abertura(tela,clock)
        if estado_atual == "menu":
            estado_atual = executar_menu(tela,clock)
        print(estado_atual)