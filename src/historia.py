import random

import pygame

from src.config import LARGURA_TELA, ALTURA_TELA, FPS, VOLUME_MUSICA
from src.funcoes import fechar_jogo

MUSICA_HISTORIA = "assets/sons/HistoryReading.mp3"

# Tempos das animações (em milissegundos)
T_ENTRADA = 900        # imagem desliza e aparece
T_TRANSICAO = 180      # rápido "tremor" de quadro ao trocar de cena
T_DIGITACAO = 45       # tempo por letra da legenda
T_PARADO = 4500        # tempo com a cena parada
T_SAIDA = 900          # fade-out ao final da cena


# Cenas na ordem da história: (imagem, legenda do roteiro)
CENAS = [
    ("assets/imagens/abertura.jpg",
     "Após A Dissonância, as metrópoles viraram cinzas. Hoje, a humanidade se esconde atrás das muralhas de Outpost Alpha."),
    ("assets/imagens/lado-de-fora.jpg",
     "Lá fora, sob a neve de fuligem, humanos e Réplicas batem aos portões, implorando por abrigo."),
    ("assets/imagens/dentro-cabine.jpg",
     "Trancado numa sala sem janelas, o Inspetor julga vidas diante de um monitor, sem nunca ver o rosto de quem julga."),
    ("assets/imagens/mao-botao.jpg",
     "A decisão é solitária e irreversível: o botão Verde libera a entrada; o Vermelho aciona o incinerador."),
    ("assets/imagens/vendo-documento.jpg",
     "Os documentos chegam à mesa. Vidas inteiras são reduzidas a ondas, temperaturas e linhas de texto."),
    ("assets/imagens/incinerador.jpg",
     "O som abafado da fornalha atravessa a parede. O erro só aparece depois, na auditoria."),
    ("assets/imagens/reflexo.jpg",
     "Ao fim do turno, o reflexo na tela parece mais frio do que deveria."),
]


def _preparar_imagem(caminho, tela):
    """Carrega a imagem e a redimensiona para caber na tela, mantendo a proporção."""
    img = pygame.image.load(caminho).convert()
    escala = min(tela.get_width() / img.get_width(), tela.get_height() / img.get_height())
    novo_tamanho = (int(img.get_width() * escala), int(img.get_height() * escala))
    img = pygame.transform.smoothscale(img, novo_tamanho)
    rect = img.get_rect(center=tela.get_rect().center)
    return img, rect


def _quebrar_texto(texto, fonte, largura_max):
    """Divide o texto em linhas que caibam na largura máxima."""
    linhas = []
    atual = ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def _processar_eventos():
    """
    Lê os eventos do teclado e do mouse durante a história.

    Saída:
        bool: True se a barra de espaço foi apertada (pula a cena atual).
    """
    pular = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fechar_jogo()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_ESCAPE:
                fechar_jogo()
            if event.key == pygame.K_SPACE:
                pular = True
    return pular


def _ease_out(t):
    """Curva de desaceleração: começa rápido e termina suave (0 a 1)."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def _letras_visiveis_por_linha(linhas, total_letras):
    """Distribui as letras já digitadas entre as linhas da legenda."""
    restantes = total_letras
    partes = []
    for linha in linhas:
        n = min(len(linha), max(0, restantes))
        partes.append(linha[:n])
        restantes -= len(linha)
    return partes


def mostrar_cena(tela, clock, caminho, legenda, indice, t_saida=T_SAIDA, t_parado=T_PARADO):
    """
    Mostra uma cena com:
      - entrada: a imagem desliza (alternando esquerda e direita) e aparece;
      - transição: um tremor curto de quadro no começo da cena;
      - legenda: digitada letra por letra, com cursor piscando;
      - saída: fade-out ao final.
    """
    img, rect_final = _preparar_imagem(caminho, tela)
    direcao = -1 if indice % 2 == 0 else 1
    distancia = LARGURA_TELA * 0.25

    fonte = pygame.font.Font(None, 28)
    altura_linha = fonte.get_linesize()
    linhas = _quebrar_texto(legenda, fonte, LARGURA_TELA - 120)
    total_letras = sum(len(linha) for linha in linhas)
    altura_caixa = altura_linha * len(linhas) + 20
    caixa = pygame.Surface((LARGURA_TELA, altura_caixa))
    caixa.fill((0, 0, 0))

    inicio_digitacao = T_ENTRADA // 2
    duracao_digitacao = total_letras * T_DIGITACAO
    total = T_ENTRADA + t_parado + t_saida
    inicio = pygame.time.get_ticks()
    rnd = random.Random(indice)

    fala_completa = False      # a legenda já foi escrita por inteiro
    completar_fala = False     # espaço pediu para completar a fala agora

    while True:
        if _processar_eventos():
            if fala_completa:
                break          # espaço com a fala completa: pula para a próxima cena
            completar_fala = True  # espaço durante a digitação: completa a fala

        decorrido = pygame.time.get_ticks() - inicio
        if decorrido >= total:
            break

        # Entrada: deslize e fade-in
        if decorrido < T_ENTRADA:
            progresso = _ease_out(decorrido / T_ENTRADA)
            alpha_img = int(255 * progresso)
            deslocamento = int(direcao * distancia * (1 - progresso))
        # Parado
        elif decorrido < T_ENTRADA + t_parado:
            alpha_img = 255
            deslocamento = 0
        # Saída: fade-out
        else:
            alpha_img = int(255 * (total - decorrido) / t_saida)
            deslocamento = 0
        alpha_img = max(0, min(255, alpha_img))

        tela.fill((0, 0, 0))

        rect = rect_final.move(deslocamento, 0)
        img_atual = img.copy()
        img_atual.set_alpha(alpha_img)
        tela.blit(img_atual, rect)

        # Transição: tremor de quadro no começo da cena
        if decorrido < T_TRANSICAO:
            for _ in range(6):
                y = rnd.randrange(0, ALTURA_TELA)
                altura = rnd.randrange(4, 18)
                faixa = tela.subsurface((0, y, LARGURA_TELA, min(altura, ALTURA_TELA - y))).copy()
                tela.blit(faixa, (rnd.randrange(-25, 25), y))

        # Legenda: digitada letra por letra
        alpha_texto = max(0, min(255, alpha_img))
        caixa.set_alpha(int(alpha_texto * 0.6))
        tela.blit(caixa, (0, ALTURA_TELA - altura_caixa))

        letras = int((decorrido - inicio_digitacao) / T_DIGITACAO) if decorrido > inicio_digitacao else 0
        if completar_fala:
            letras = total_letras
        letras = min(letras, total_letras)
        fala_completa = letras >= total_letras
        partes = _letras_visiveis_por_linha(linhas, letras)
        digitando = not fala_completa
        cursor_visivel = digitando and (decorrido // 250) % 2 == 0

        for i, parte in enumerate(partes):
            texto = parte + ("_" if cursor_visivel and i == len([p for p in partes if p]) - 1 else "")
            if not texto:
                continue
            superficie = fonte.render(texto, False, "White")
            superficie.set_alpha(alpha_texto)
            pos = superficie.get_rect(topleft=(60, ALTURA_TELA - altura_caixa + 10 + i * altura_linha))
            tela.blit(superficie, pos)

        pygame.display.update()
        clock.tick(FPS)


def executar_historia(tela, clock):
    """
    Executa a história inteira: passa as cenas na ordem, cada uma com a sua legenda,
    animações de entrada e a música da história.

    Parâmetros:
        tela (Surface): superfície principal do jogo.
        clock (Clock): relógio usado para controlar o FPS.

    Saída:
        bool: True quando todas as cenas terminarem.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(MUSICA_HISTORIA)
    pygame.mixer.music.set_volume(VOLUME_MUSICA)
    pygame.mixer.music.play()  # toca uma vez, sem repetir

    for indice, (caminho, legenda) in enumerate(CENAS):
        mostrar_cena(tela, clock, caminho, legenda, indice)

    pygame.mixer.music.stop()
    return "menu"
