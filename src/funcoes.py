import pygame
from sys import exit
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    VOLUME_MUSICA,
)

def fechar_jogo():
    """ Finalizar a execução do jogo. """
    pygame.quit()
    exit()

def conferir_inputs():     

    for event in pygame.event.get():
        #Fecha o jogo ao clicar no (X) em tela janela
        if event.type == pygame.QUIT:
            fechar_jogo()
        if event.type == pygame.KEYDOWN:
            # Alterna tela cheia ao apertar F11
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            # Sai do jogo ao apertar ESC
            if event.key == pygame.K_ESCAPE:
                fechar_jogo()

def executar_abertura(tela,clock,fonte):

    # Config música

    pygame.mixer.init()
    pygame.mixer.music.load("assets/sons/MainTheme.mp3")
    pygame.mixer.music.set_volume(VOLUME_MUSICA)
    pygame.mixer.music.play(-1)

    # Config Texto tela

    titulo = fonte.render(TITULO_JOGO, False, 'White')
    titulo_ret = titulo.get_rect(center = (400,100))

    while True:

        conferir_inputs()
        tela.blit(titulo,titulo_ret)


