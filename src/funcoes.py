import pygame
from sys import exit
import random
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    VOLUME_MUSICA,
)

class Botao:
    def __init__(self, img_normal_base, img_hover_base, texto, fonte, pos_centro):
        # 1. Prepara a imagem do estado NORMAL (com texto)
        self.img_normal = img_normal_base.copy()
        self._escrever_texto(self.img_normal, texto, fonte, (220, 220, 220))

        # 2. Prepara a imagem do estado HOVER (com texto destacado)
        self.img_hover = img_hover_base.copy()
        self._escrever_texto(self.img_hover, texto, fonte, (255, 255, 255))

        # Começa com a imagem normal
        self.image = self.img_normal
        self.rect = self.image.get_rect(center=pos_centro)

    def _escrever_texto(self, superficie, texto, fonte, cor):
        """Centraliza o texto dentro da superfície do botão."""
        txt_surf = fonte.render(texto, True, cor)
        txt_rect = txt_surf.get_rect(center=(superficie.get_width() // 2, superficie.get_height() // 2))
        superficie.blit(txt_surf, txt_rect)

    def desenhar(self, tela):
        # Verifica a posição atual do mouse a cada frame
        pos_mouse = pygame.mouse.get_pos()

        # Troca o sprite se o mouse estiver dentro do retângulo do botão
        if self.rect.collidepoint(pos_mouse):
            self.image = self.img_hover
        else:
            self.image = self.img_normal

        tela.blit(self.image, self.rect)

    def foi_clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False


def fechar_jogo():
    """ Finalizar a execução do jogo. """
    pygame.quit()
    exit()



def executar_musica_menu():
    """Executa a música do menu"""
    # Config música

    pygame.mixer.init()
    pygame.mixer.music.load("assets/sons/MainTheme.mp3")
    pygame.mixer.music.set_volume(VOLUME_MUSICA)

    # Executar música

    pygame.mixer.music.play(-1)

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
            if event.key == pygame.K_SPACE:
                return "menu"

def mostrar_com_fade(tela, clock, imagem, rect, t_fadein=2000, t_parado=2000, t_fadeout=2000):
    """Exibe qualquer Surface (imagem ou texto) com fade-in, pausa e fade-out."""
    tempo_inicio = pygame.time.get_ticks()
    
    fim_fadein = t_fadein
    fim_parado = fim_fadein + t_parado
    fim_fadeout = fim_parado + t_fadeout

    while True:
        tela.fill((0, 0, 0))
        estado = conferir_inputs()
        if estado == "menu":
            return estado

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
    if mostrar_com_fade(tela, clock, logo_puc, rect_logo_puc) == "menu":
        return "menu"
    if mostrar_com_fade(tela, clock, logo_ES, rect_logo_ES) == "menu":
        return "menu"
    if mostrar_com_fade(tela, clock, logo_grupo, rect_logo_grupo) == "menu":
        return "menu"

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

def variar_alfa(alfa, aumentando, minimo=60, maximo=180):
    """Atualiza o alpha e troca a direção ao atingir os limites."""
    if alfa >= maximo:
        alfa = maximo
        aumentando = False
    elif alfa <= minimo:
        alfa = minimo
        aumentando = True

    alfa += 1 if aumentando else -1
    return alfa, aumentando

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

    # Config do sprite dos botões
    btn_normal = pygame.image.load("assets/imagens/botao-sem-selecao.png").convert_alpha()
    btn_hover = pygame.image.load("assets/imagens/botao-com-selecao.png").convert_alpha()
    tamanho_botao = (200, 60)
    btn_normal = pygame.transform.smoothscale(btn_normal, tamanho_botao)
    btn_hover = pygame.transform.smoothscale(btn_hover, tamanho_botao)
    fonte_menu = pygame.font.Font("assets/fontes/Asimovian/commando.ttf", 30)

    centro_x = LARGURA_TELA // 2
    botao_jogar = Botao(btn_normal, btn_hover, "JOGAR", fonte_menu, (centro_x, 335))
    botao_config = Botao(btn_normal, btn_hover, "CONFIG", fonte_menu, (centro_x, 440))
    botao_sair = Botao(btn_normal, btn_hover, "SAIR", fonte_menu, (centro_x, 545))

    # Gerar Flocos
    flocos_neve = gerar_flocos()
    alfa = 0
    aumentando = True
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif evento.key == pygame.K_ESCAPE:
                    fechar_jogo()
            elif botao_jogar.foi_clicado(evento):
                return "jogo"
            elif botao_sair.foi_clicado(evento):
                fechar_jogo()

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
        alfa, aumentando = variar_alfa(alfa, aumentando)
        titulo.set_alpha(alfa)
        tela.blit(titulo, titulo_ret)

        #Cria os botões
        botao_jogar.desenhar(tela)
        botao_config.desenhar(tela)
        botao_sair.desenhar(tela)
        pygame.display.flip()
        clock.tick(FPS)