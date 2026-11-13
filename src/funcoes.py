import pygame
from sys import exit
import random
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

    # Config logo Grupo 3
    logo_grupo = pygame.image.load("assets/imagens/logo-grupo-3.png").convert_alpha()
    logo_grupo = pygame.transform.smoothscale(logo_grupo,(largura_alvo,altura_alvo))
    rect_logo_grupo = logo_grupo.get_rect(center=tela.get_rect().center)

    # Iniciar musica
    executar_musica_menu()

    # Sequência de animações
    mostrar_com_fade(tela,clock,logo_puc,rect_logo_puc)

    mostrar_com_fade(tela,clock,logo_ES,rect_logo_ES)

    mostrar_com_fade(tela,clock,logo_grupo,rect_logo_grupo)

    return "menu"

def gerar_flocos():
    """Gera 100 flocos em posições aleatórias com velocidades suaves (float)."""
    flocos_neve = []
    for _ in range(100):
        x = float(random.randint(0, LARGURA_TELA))
        y = float(random.randint(-ALTURA_TELA, ALTURA_TELA))
        velocidade_y = random.uniform(0.4, 1.0)   # Queda bem suave
        velocidade_x = random.uniform(-0.2, 0.2)  # Vento sutil
        tamanho = random.randint(1, 3)
        flocos_neve.append([x, y, velocidade_y, velocidade_x, tamanho])

    return flocos_neve

def variar_alfa(alfa, aumentando):
    """Varia o alpha do sprite conforme a direção informada."""
    return alfa + 1 if aumentando else alfa - 1

def executar_menu(tela, clock):
    """Executa o loop do menu principal"""
    # Config das imagens do menu
    imagem_fundo = pygame.image.load("assets/imagens/imagem-fundo-menu.jpg").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
    # Config do sprite do título
    titulo = pygame.image.load("assets/imagens/outpost-alpha.png").convert_alpha()
    largura_titulo = 600
    altura_titulo = int(largura_titulo * titulo.get_height() / titulo.get_width())
    titulo = pygame.transform.smoothscale(titulo,(largura_titulo, altura_titulo))
    titulo_ret = titulo.get_rect(center=(LARGURA_TELA // 2, 160))

    # Gerar Flocos
    flocos_neve = gerar_flocos()
    alfa = 0
    aumentando = True
    while True:
        conferir_inputs()

        tela.blit(imagem_fundo, (0, 0))

        # 3. Atualiza e desenha CADA floco de neve
        for floco in flocos_neve:
            floco[1] += floco[2]  # Cai no eixo Y
            floco[0] += floco[3]  # Move no eixo X (vento)
        
            # Reset ao sair da tela 
            if floco[1] > ALTURA_TELA:
                floco[1] = float(random.randint(-20, -5))
                floco[0] = float(random.randint(0, LARGURA_TELA))
                floco[2] = random.uniform(0.4, 1.0)    

            # Desenha o floco 
            cor_neve = (180, 195, 210) if floco[4] == 1 else (230, 240, 255)
            pygame.draw.circle(tela, cor_neve, (int(floco[0]), int(floco[1])), floco[4])
            
        # Verifica a transparência do título
        if alfa >= 180:
            alfa = 180
            aumentando = False
        elif alfa <= 60:
            alfa = 60
            aumentando = True

        alfa = variar_alfa(alfa, aumentando)
        titulo.set_alpha(alfa)
        tela.blit(titulo, titulo_ret)
        pygame.display.flip()
        clock.tick(FPS)