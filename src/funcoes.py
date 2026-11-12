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

def executar_musica_menu():
    """Executa a música do menu"""
    # Config música

    pygame.mixer.init()
    pygame.mixer.music.load("assets/sons/MainTheme.mp3")
    pygame.mixer.music.set_volume(VOLUME_MUSICA)

    # Executar música

    pygame.mixer.music.play(-1)

def executar_abertura(tela,clock):
    """
    Executa a animação de abertura do jogo
    
    Parâmetros: 
        Tela (Object): Superficie principal criada na execução inicial do código.

    Saída: 
        str: String referente ao estado do jogo após o fim da execução.
    """
    # Config fonte texto
    fonte_texto = pygame.font.Font(None, 50)
    texto = fonte_texto.render("Bem vindo a Outpost Alpha!", False, "White")
    texto_ret = texto.get_rect(midtop = (400, 100))

    # Config logo puc
    logo_puc = pygame.image.load("assets/imagens/brasao-pucminas.png").convert_alpha()
    rect_logo = logo_puc.get_rect(center=tela.get_rect().center) # Liga a logo ao retângulo ligado ao centro da tela
    

    # Config do tempo de execução

    
    logo_tempo_fadein = 2000
    logo_tempo_parado = logo_tempo_fadein  + 2000 # 4000 ms
    logo_tempo_fadeout = logo_tempo_parado + 2000 # 6000 ms

    tempo_inicio = pygame.time.get_ticks()
    executar_musica_menu()

    while True:
        tela.fill((0, 0, 0))
        conferir_inputs()

        decorrido = pygame.time.get_ticks() - tempo_inicio

        if decorrido <= logo_tempo_fadein:
            progresso = min(1.0, max(0.0, decorrido / logo_tempo_fadein))
            alpha = int(255 * progresso)

        elif decorrido <= logo_tempo_parado:
            alpha = 255

        elif decorrido <= logo_tempo_fadeout:

            tempo_etapa = decorrido - logo_tempo_parado
            duracao_etapa = logo_tempo_fadeout - logo_tempo_parado
            progresso = min(1.0, max(0.0, tempo_etapa / duracao_etapa))
            alpha = int(255 * (1.0 - progresso))
            
        logo_atual = logo_puc.copy()
        logo_atual.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        tela.blit(logo_atual, rect_logo)        
        
        pygame.display.update()
        clock.tick(FPS)

