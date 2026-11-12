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

def mostrar_com_fade(tela, clock, imagem, rect, t_fadein=2000, t_parado=2000, t_fadeout=2000):
    """Exibe qualquer Surface (imagem ou texto) com fade-in, pausa e fade-out."""
    tempo_inicio = pygame.time.get_ticks()
    
    fim_fadein = t_fadein
    fim_parado = fim_fadein + t_parado
    fim_fadeout = fim_parado + t_fadeout

    while True:
        tela.fill((0, 0, 0))
        conferir_inputs()

        decorrido = pygame.time.get_ticks() - tempo_inicio

        if decorrido <= fim_fadein:
            progresso = decorrido / t_fadein
            alpha = int(255 * progresso)

        elif decorrido <= fim_parado:
            alpha = 255

        elif decorrido <= fim_fadeout:
            tempo_etapa = decorrido - fim_parado
            progresso = tempo_etapa / t_fadeout
            alpha = int(255 * (1.0 - progresso))

        else:
            break  # Terminou essa imagem, sai do loop para ir para a próxima

        alpha = max(0, min(255, alpha))

        # Aplica a transparência na cópia
        img_atual = imagem.copy()
        img_atual.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        tela.blit(img_atual, rect)

        pygame.display.update()
        clock.tick(FPS)

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
    rect_logo_puc = logo_puc.get_rect(center=tela.get_rect().center) # Liga a logo ao retângulo ligado ao centro da tela

    # Config logo eng.software
    logo_ES = pygame.image.load("assets/imagens/Logo_ES_negativo@4x-1.png").convert_alpha()
    largura_alvo = int(tela.get_width() * 0.50) # Define a largura como 50% da largura da tela
    altura_alvo = int(largura_alvo * (logo_ES.get_height() / logo_ES.get_width())) # Calcula a altura exata mantendo a proporção
    logo_ES = pygame.transform.smoothscale(logo_ES, (largura_alvo, altura_alvo)) # Redimensiona com suavização (ideal para imagens grandes reduzidas)
    rect_logo_ES = logo_ES.get_rect(center=tela.get_rect().center)
    

    # Iniciar musica
    executar_musica_menu()

    # Sequência de animações
    mostrar_com_fade(tela,clock,logo_puc,rect_logo_puc)

    mostrar_com_fade(tela,clock,logo_ES,rect_logo_ES)

    return True

def executar_menu():
    modo = "iniciando"
    return modo