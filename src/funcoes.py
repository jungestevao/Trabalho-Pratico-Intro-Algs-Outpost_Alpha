import pygame
from sys import exit
import random
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    FONTE_MENU,
    SPRITE_BTN_ATIVO,
    SPRITE_BTN_DESATIVO,
    SPRITE_FUNDO_MENU,
    SPRITE_LOGO_ES,
    SPRITE_LOGO_G3,
    SPRITE_LOGO_JOGO,
    SPRITE_LOGO_PUC,
    MUSICA_FIM_FASE,
    MUSICA_HISTORIA,
    MUSICA_MENU
)
from src.dados import(
    registrar_dados
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


def fechar_jogo(dados):
    """ Finalizar a execução do jogo. """
    dados["tela"] = "abertura"
    registrar_dados(dados)
    pygame.quit()
    exit()

def configurar_sprite_botao():

    btn_normal = pygame.image.load(SPRITE_BTN_DESATIVO).convert_alpha()
    btn_hover = pygame.image.load(SPRITE_BTN_ATIVO).convert_alpha()
    tamanho_botao = (200, 60)
    btn_normal = pygame.transform.smoothscale(btn_normal, tamanho_botao)
    btn_hover = pygame.transform.smoothscale(btn_hover, tamanho_botao)
    fonte_menu = pygame.font.Font(FONTE_MENU[0],FONTE_MENU[1])

    return btn_normal,btn_hover,fonte_menu

def executar_musica(dados,musica):
    """Executa a música do menu"""
    # Config música

    pygame.mixer.init()
    pygame.mixer.music.load(musica)
    pygame.mixer.music.set_volume(dados["volume"])

    # Executar música

    pygame.mixer.music.play(-1)

def conferir_inputs(dados):
    """Processa inputs globais e devolve eventos para a tela atual."""
    eventos_da_tela = []
    estado = None

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fechar_jogo(dados)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            elif evento.key == pygame.K_ESCAPE:
                fechar_jogo(dados)
            elif evento.key == pygame.K_SPACE:
                estado = "menu"
        else:
            eventos_da_tela.append(evento)

    return estado, eventos_da_tela

def mostrar_com_fade(tela, clock, imagem, rect, dados, t_fadein=2000, t_parado=2000, t_fadeout=2000,):
    """Exibe qualquer Surface (imagem ou texto) com fade-in, pausa e fade-out."""
    tempo_inicio = pygame.time.get_ticks()
    
    fim_fadein = t_fadein
    fim_parado = fim_fadein + t_parado
    fim_fadeout = fim_parado + t_fadeout

    while True:
        tela.fill((0, 0, 0))
        estado, _ = conferir_inputs(dados)
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
    
def executar_abertura(tela,clock,dados):
    """
    Executa a animação de abertura do jogo
    
    Parâmetros: 
        Tela (Object): Superficie principal criada na execução inicial do código.
        Clock (Class): Classe referente a frequencia de execução.
        Dados (Dict): Dicionário do estado do jogo.
 
    Saída: 
        None
    """
    # Config fonte texto
    fonte_texto = pygame.font.Font(None, 50)
    texto = fonte_texto.render("Bem vindo a Outpost Alpha!", False, "White")
    texto_ret = texto.get_rect(midtop = (400, 100))

    # Config logo puc
    logo_puc = pygame.image.load(SPRITE_LOGO_PUC).convert_alpha()
    rect_logo_puc = logo_puc.get_rect(center=tela.get_rect().center) # Liga a logo ao retângulo ligado ao centro da tela

    # Config logo eng.software
    logo_ES = pygame.image.load(SPRITE_LOGO_ES).convert_alpha()
    largura_alvo = int(tela.get_width() * 0.50) # Define a largura como 50% da largura da tela
    altura_alvo = int(largura_alvo * (logo_ES.get_height() / logo_ES.get_width())) # Calcula a altura exata mantendo a proporção
    logo_ES = pygame.transform.smoothscale(logo_ES, (largura_alvo, altura_alvo)) # Redimensiona com suavização (ideal para imagens grandes reduzidas)
    rect_logo_ES = logo_ES.get_rect(center=tela.get_rect().center)

    # Config logo Grupo 3
    logo_grupo = pygame.image.load(SPRITE_LOGO_G3).convert_alpha()
    logo_grupo = pygame.transform.smoothscale(logo_grupo,(largura_alvo,altura_alvo))
    rect_logo_grupo = logo_grupo.get_rect(center=tela.get_rect().center)

    # Iniciar musica
    executar_musica(dados, MUSICA_MENU)

    # Sequência de animações
    if mostrar_com_fade(tela, clock, logo_puc, rect_logo_puc, dados) == "menu":
        dados["tela"] = "menu"
        return registrar_dados(dados)
    if mostrar_com_fade(tela, clock, logo_ES, rect_logo_ES, dados) == "menu":
        dados["tela"] = "menu"
        return registrar_dados(dados)
    if mostrar_com_fade(tela, clock, logo_grupo, rect_logo_grupo, dados) == "menu":
        dados["tela"] = "menu"
        return registrar_dados(dados)

    dados["tela"] = "menu"
    return registrar_dados(dados)


def gerar_flocos():
    """
    Gera 100 flocos em posições aleatórias com velocidades suaves (float).
    
    Parâmetros:
        None.
    
    Saídas:
        flocos_neve (list):
    """
    flocos_neve = []
    for _ in range(100):
        x = float(random.randint(0, LARGURA_TELA))
        y = float(random.randint(-ALTURA_TELA, ALTURA_TELA))
        velocidade_y = random.uniform(0.4, 1.0)   # Queda bem suave
        velocidade_x = random.uniform(-0.2, 0.2)  # Vento sutil
        tamanho = random.randint(1, 3)
        flocos_neve.append([x, y, velocidade_y, velocidade_x, tamanho])

    return flocos_neve

def atualizar_flocos(tela, flocos_neve):
    """Atualiza as posições e desenha os flocos de neve na tela."""
    for floco in flocos_neve:
        floco[1] += floco[2]
        floco[0] += floco[3]

        if floco[1] > ALTURA_TELA:
            floco[1] = float(random.randint(-20, -5))
            floco[0] = float(random.randint(0, LARGURA_TELA))
            floco[2] = random.uniform(0.4, 1.0)

        cor_neve = (180, 195, 210) if floco[4] == 1 else (230, 240, 255)
        pygame.draw.circle(
            tela,
            cor_neve,
            (int(floco[0]), int(floco[1])),
            floco[4]
        )

def variar_alfa(alfa, aumentando, minimo=60, maximo=180):
    """
    Atualiza o alpha e troca a direção ao atingir os limites.

    Parâmetros:
        alfa (int): coeficiente de transparência,
        aumentando (bool): Flag que representa a direção de alfa,
        minimo (int): valor minimo de variação do alfa,
        maximo (int): valor máximo de variação do alfa.

    Saídas:
        alfa (int): valor atualizado para alfa,
        aumentando (bool): Flag atualizada de acordo com o estado. 
    """
    if alfa >= maximo:
        alfa = maximo
        aumentando = False
    elif alfa <= minimo:
        alfa = minimo
        aumentando = True

    alfa += 1 if aumentando else -1
    return alfa, aumentando

def executar_menu_config(tela,clock,dados):
    """
    Executa a tela de configurações em loop

    Parâmetros: 
    Tela (Object): Superficie principal criada na execução inicial do código.
    Clock (Class): Classe referente a frequencia de execução.
    Dados (Dict): Dicionário do estado do jogo.
 
    Saída: 
        None
    """
    # Config imagem fundo config
    imagem_fundo = pygame.image.load(SPRITE_FUNDO_MENU).convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))

    centro = LARGURA_TELA/2
    flocos = gerar_flocos()

    # Configs botões
    btn_normal,btn_hover,fonte = configurar_sprite_botao()

    btn_historia = Botao(btn_normal, btn_hover, "HISTORIA", fonte, (centro,300))
    btn_sair = Botao(btn_normal, btn_hover, "MENU", fonte, (centro,400))
    while True:
        btn_volume = Botao(
            btn_normal,
            btn_hover,
            f"{int(dados['volume'] * 100)}",
            fonte,
            (centro, 200)
        )
        _, evento = conferir_inputs(dados)
        tela.blit(imagem_fundo,(0,0))

        # Config Inputs
        for eventos in evento:
            if btn_volume.foi_clicado(eventos):
                if dados["volume"] >= 1.0:
                    dados["volume"] = 0.0
                else:
                    dados["volume"] = round(dados["volume"] + 0.1, 1)
                    
                pygame.mixer.music.set_volume(dados["volume"])
                registrar_dados(dados)
            elif btn_sair.foi_clicado(eventos):
                dados["tela"] = "menu"
                registrar_dados(dados)
                return
            elif btn_historia.foi_clicado(eventos):
                dados["tela"] = "historia-btn"
                registrar_dados(dados)
                return

        btn_volume.desenhar(tela)
        btn_historia.desenhar(tela)
        btn_sair.desenhar(tela)

        atualizar_flocos(tela,flocos)
        pygame.display.flip()
        clock.tick(FPS)

def executar_menu(tela, clock, dados):
    """Executa o loop do menu principal"""
    # Config das imagens do menu
    imagem_fundo = pygame.image.load(SPRITE_FUNDO_MENU).convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
    # Config do sprite do título
    titulo = pygame.image.load(SPRITE_LOGO_JOGO).convert_alpha()
    largura_titulo = 600
    altura_titulo = int(largura_titulo * titulo.get_height() / titulo.get_width())
    titulo = pygame.transform.smoothscale(titulo,(largura_titulo, altura_titulo))
    titulo_ret = titulo.get_rect(center=(LARGURA_TELA // 2, 160))

    # Config do sprite dos botões
    btn_normal, btn_hover, fonte_menu = configurar_sprite_botao()

    # Config das variáveis do botão
    centro_x = LARGURA_TELA // 2
    botao_jogar = Botao(btn_normal, btn_hover, "JOGAR", fonte_menu, (centro_x, 335))
    botao_config = Botao(btn_normal, btn_hover, "CONFIG", fonte_menu, (centro_x, 440))
    botao_sair = Botao(btn_normal, btn_hover, "SAIR", fonte_menu, (centro_x, 545))

    # Conferir se a música está ativa
    if not(pygame.mixer.music.get_busy()):
        executar_musica(dados, MUSICA_MENU)

    # Gerar Flocos
    flocos_neve = gerar_flocos()

    # Variárveis iniciais título
    alfa = 0
    aumentando = True

    while True:
        # Config Inputs
        _, eventos = conferir_inputs(dados)
        for evento in eventos:
            if botao_jogar.foi_clicado(evento):
                if dados["historia"]:
                    dados["tela"] = "historia"
                    registrar_dados(dados)
                    pygame.mixer.music.fadeout(1)
                    return
                else: 
                    dados["tela"] = "jogo"
                    registrar_dados(dados)
                    return
            elif botao_config.foi_clicado(evento):
                dados["tela"] = "config"
                registrar_dados(dados)
                return
            elif botao_sair.foi_clicado(evento):
                fechar_jogo(dados)

        tela.blit(imagem_fundo, (0, 0))

        atualizar_flocos(tela, flocos_neve)
            
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

def executar_fases(tela,clock,dados):

    fonte = pygame.font.Font(FONTE_MENU[0],20)
    texto = fonte.render("EM DESENVOLVIMENTO - AGRADECEMOS SUA PACIENCIA!", True, "White")
    rect_texto = texto.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))

    executar_musica(dados,MUSICA_FIM_FASE)

    while True:
        conferir_inputs(dados)

        tela.fill((0,0,0))
        tela.blit(texto,rect_texto)

        pygame.display.flip()
        clock.tick(FPS)
