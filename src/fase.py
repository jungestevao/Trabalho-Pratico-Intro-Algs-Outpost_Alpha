import math
import pygame
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    BRANCO,
    PRETO,
    CINZA,
    FONTE_TITULO,
    FONTE_CARTAO,
    DADOS,
    MUSICA_FIM_FASE,
    SOM_FUNDO,
    SOM_MONITOR,
    SPRITE_FUNDO_JOGO,
    SPRITE_CAIXA_CORREIO_DESATIVADA,
    SPRITE_CAIXA_CORREIO_ATIVA,
    SPRITE_BOTAO,
    SPRITE_BOTAO_SELECIONADO,
    SPRITE_COMPUTADOR,
    SPRITE_COMPUTADOR_SELECIONADO,
    SPRITE_MICROFONE,
    SPRITE_MICROFONE_SELECIONADO,
    SPRITE_TELA_CHEIA_BOTAO,
    SPRITE_TELA_CHEIA_VERDE_APERTADO,
    SPRITE_TELA_CHEIA_VERMELHO_APERTADO,
    SPRITE_MONITOR_CRT_BASE,
    SPRITE_ICONE_BPM_NORMAL,
    SPRITE_ICONE_BPM_HOVER,
    SPRITE_ICONE_TEMP_NORMAL,
    SPRITE_ICONE_TEMP_HOVER,
    SPRITE_ICONE_PESO_NORMAL,
    SPRITE_ICONE_PESO_HOVER,
    SPRITE_MONITOR_APP_BPM,
    SPRITE_MONITOR_APP_TEMP,
    SPRITE_MONITOR_APP_PESO,
    SPRITE_AVATAR_ID_PERSONAGENS,
    AVATARES_PERSONAGENS,
)
from src.dados import iniciar_personagens, registrar_dados
from src.funcoes import fechar_jogo, executar_musica


# Config de cores do terminal CRT
VERDE_CRT = (60, 235, 110)
VERDE_CRT_BRILHO = (180, 250, 172)
VERDE_CRT_SUAVE = (120, 195, 130)
VERDE_CRT_ESCURO = (20, 75, 35)
VERDE_PAINEL = (12, 34, 18)

# Config de perguntas, métodos e filas por fase
PERGUNTAS_MICROFONE = [
    "1. Qual sua situacao e motivo para pedir abrigo?",
    "2. Confirme sua identidade, origem e registro.",
    "3. Como estao suas condicoes fisicas e bagagem/peso?",
]

METODOS_VERIFICACAO = ("bpm", "temperatura", "peso")

METODOS_POR_FASE = {
    1: ("bpm", "temperatura", "peso"),
    2: ("bpm", "temperatura", "peso"),
    3: ("bpm", "temperatura", "peso"),
}

FILAS_POR_FASE = {
    1: [
        "Marcos Silva",
        "Elena Vance",
        "Jonas Ribeiro",
        "Clara Mendes",
        "Artur Kovic",
        "Laerte Xavier",
    ],
}

TITULOS_METODOS_MONITOR = {
    "bpm": "BATIMENTOS",
    "temperatura": "TEMPERATURA",
    "peso": "PESO",
}

# Config de áreas dos objetos na guarita e no monitor
RECT_MONITOR_CRT = pygame.Rect(100, 36, 600, 472)

RECTS_ICONES_MONITOR = {
    "bpm": pygame.Rect(172, 185, 128, 128),
    "temperatura": pygame.Rect(336, 185, 128, 128),
    "peso": pygame.Rect(500, 185, 128, 128),
}

POSICOES_GUARITA = {
    "caixa_correio": (85, 140, 160, 229),
    "computador": (230, 204, 371, 348),
    "microfone": (85, 314, 157, 237),
    "botao": (562, 441, 160, 104),
}

RECT_BOTAO_VERDE_CHEIA = pygame.Rect(245, 177, 101, 84)
RECT_BOTAO_VERMELHO_CHEIA = pygame.Rect(451, 177, 101, 87)


def _quebrar_linhas(texto, fonte, largura_max):
    """
    Divide um texto em linhas que caibam dentro da largura máxima em pixels.

    Parâmetros:
        texto (str): texto a ser quebrado.
        fonte (pygame.font.Font): fonte utilizada para medir o texto.
        largura_max (int): largura máxima em pixels.

    Saída:
        linhas (list): lista de strings linha a linha.
    """
    linhas = []
    atual = ""
    for palavra in str(texto).split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def _desenhar_botao_terminal(
    tela, rect, texto, fonte, hover=False, cor_borda=VERDE_CRT, alinhar_esquerda=False
):
    """
    Desenha um botão retangular no estilo CRT do terminal.

    Parâmetros:
        tela (pygame.Surface): superfície principal do jogo.
        rect (pygame.Rect): área do botão.
        texto (str): texto do botão.
        fonte (pygame.font.Font): fonte usada no texto.
        hover (bool): indica se o mouse está sobre o botão.
        cor_borda (tuple): cor RGB da borda e do texto.
        alinhar_esquerda (bool): alinha o texto à esquerda quando True.

    Saída:
        None
    """
    cor_fundo = (30, 70, 42) if hover else (12, 28, 18)
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=4)
    pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=4)
    surf = fonte.render(texto, True, BRANCO if hover else cor_borda)
    pos = (
        surf.get_rect(midleft=(rect.x + 20, rect.centery))
        if alinhar_esquerda
        else surf.get_rect(center=rect.center)
    )
    tela.blit(surf, pos)


# =====================================================================
# CLASSES ORIENTADAS A OBJETO DA GUARITA
# =====================================================================

class ObjetoInterativo:
    """
    Representa qualquer objeto clicável da guarita ou ícone do monitor com estado normal e hover.
    """

    def __init__(self, nome, img_normal, img_hover, rect):
        """
        Inicializa o objeto com suas imagens normal/hover e retângulo de colisão.

        Parâmetros:
            nome (str): identificador do objeto.
            img_normal (pygame.Surface): sprite padrão.
            img_hover (pygame.Surface): sprite ao passar o mouse.
            rect (tuple | pygame.Rect): posição e dimensões do objeto.

        Saída:
            None
        """
        self.nome = nome
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.image = self.img_normal
        self.rect = pygame.Rect(rect)

    @classmethod
    def de_arquivos(cls, nome, caminho_normal, caminho_hover, rect):
        """
        Carrega e escala os sprites normal e hover diretamente dos caminhos de arquivo.

        Parâmetros:
            nome (str): identificador do objeto.
            caminho_normal (str): caminho da imagem normal.
            caminho_hover (str): caminho da imagem hover.
            rect (tuple | pygame.Rect): posição e dimensões alvo.

        Saída:
            (ObjetoInterativo): instância pronta para uso.
        """
        r = pygame.Rect(rect)
        img_n = pygame.transform.smoothscale(
            pygame.image.load(caminho_normal).convert_alpha(), r.size
        )
        img_h = pygame.transform.smoothscale(
            pygame.image.load(caminho_hover).convert_alpha(), r.size
        )
        return cls(nome, img_n, img_h, r)

    def em_hover(self, pos_mouse):
        """
        Verifica se o cursor do mouse está sobre o objeto.

        Parâmetros:
            pos_mouse (tuple): coordenadas (x, y) do mouse.

        Saída:
            (bool): True se o mouse colidir com o retângulo do objeto.
        """
        return self.rect.collidepoint(pos_mouse)

    def desenhar(self, tela, ativo_hover=False):
        """
        Desenha o objeto na tela alternando o sprite conforme o hover.

        Parâmetros:
            tela (pygame.Surface): superfície principal do jogo.
            ativo_hover (bool): True para exibir o sprite selecionado.

        Saída:
            None
        """
        self.image = self.img_hover if ativo_hover else self.img_normal
        tela.blit(self.image, self.rect.topleft)

    def foi_clicado(self, evento):
        """
        Verifica se houve clique esquerdo do mouse sobre o objeto.

        Parâmetros:
            evento (pygame.event.Event): evento atual do Pygame.

        Saída:
            (bool): True se o objeto foi clicado.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False


class CaixaCorreio(ObjetoInterativo):
    """
    Objeto da Caixa de Correio e seu pop-up de Cartão de Identidade.
    """

    def __init__(self, fila):
        """
        Carrega os sprites da Caixa de Correio, o cartão de identidade e os avatares da fila.

        Parâmetros:
            fila (list): lista de visitantes do turno.

        Saída:
            None
        """
        base = ObjetoInterativo.de_arquivos(
            "caixa_correio",
            SPRITE_CAIXA_CORREIO_DESATIVADA,
            SPRITE_CAIXA_CORREIO_ATIVA,
            POSICOES_GUARITA["caixa_correio"],
        )
        super().__init__("caixa_correio", base.img_normal, base.img_hover, base.rect)

        cartao_orig = pygame.image.load(SPRITE_AVATAR_ID_PERSONAGENS).convert_alpha()
        altura_c = int(720 * cartao_orig.get_height() / cartao_orig.get_width())
        self.cartao_id = pygame.transform.smoothscale(cartao_orig, (720, altura_c))
        self.avatares = {
            v["nome"]: pygame.image.load(v["avatar"]).convert_alpha() for v in fila
        }

    def desenhar_popup(self, tela, visitante, fontes, pos_mouse):
        """
        Desenha o pop-up do cartão de identidade preenchido com os dados do visitante.

        Parâmetros:
            tela (pygame.Surface): superfície principal do jogo.
            visitante (dict | None): visitante atual da fila.
            fontes (dict): dicionário de fontes carregadas.
            pos_mouse (tuple): posição atual do mouse.

        Saída:
            rect_voltar (pygame.Rect): retângulo do botão de voltar à guarita.
        """
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 195))
        tela.blit(overlay, (0, 0))

        fonte_menu = fontes["pequena_menu"]
        fonte_crt = fontes["crt"]
        fonte_menor = fontes["cartao_pequena"]

        faixa_topo = pygame.Rect(110, 42, LARGURA_TELA - 220, 38)
        pygame.draw.rect(tela, (8, 22, 12), faixa_topo, border_radius=6)
        pygame.draw.rect(tela, VERDE_CRT_ESCURO, faixa_topo, 1, border_radius=6)
        titulo = fonte_menu.render(
            "DOCUMENTO DE IDENTIFICACAO - CAIXA DE CORREIO", True, VERDE_CRT
        )
        tela.blit(titulo, titulo.get_rect(center=faixa_topo.center))

        cartao_rect = self.cartao_id.get_rect(center=(LARGURA_TELA // 2, 232))
        tela.blit(self.cartao_id, cartao_rect)

        if visitante is not None:
            dados_cartao = extrair_dados_cartao(visitante)
            avatar_orig = self.avatares.get(visitante["nome"])
            if avatar_orig is not None:
                ex, ey = cartao_rect.width / 962.0, cartao_rect.height / 352.0
                quadro = pygame.Rect(
                    cartao_rect.x + int(57 * ex),
                    cartao_rect.y + int(43 * ey),
                    int(240 * ex),
                    int(252 * ey),
                )
                prop = min(
                    (quadro.width - 8) / avatar_orig.get_width(),
                    (quadro.height - 8) / avatar_orig.get_height(),
                )
                tam = (
                    max(1, int(avatar_orig.get_width() * prop)),
                    max(1, int(avatar_orig.get_height() * prop)),
                )
                av_esc = pygame.transform.smoothscale(avatar_orig, tam)
                tela.blit(av_esc, av_esc.get_rect(center=quadro.center))

            cache = fontes.get("cartao_tamanhos")
            for campo in obter_especificacoes_campos_cartao(dados_cartao, cartao_rect):
                f_campo, linhas = ajustar_render_campo_cartao(
                    campo["valor"], campo["largura_disponivel"], fontes_cache=cache
                )
                altura_l = f_campo.get_height() if len(linhas) == 1 else f_campo.get_linesize()
                pos_y = campo["linha_base_y"] - altura_l * len(linhas)
                for i, linha in enumerate(linhas):
                    surf = f_campo.render(linha, True, (25, 25, 25))
                    tela.blit(surf, (campo["pos_x"], pos_y + i * altura_l))

            caixa_obs = pygame.Rect(70, cartao_rect.bottom + 18, LARGURA_TELA - 140, 92)
            pygame.draw.rect(tela, (8, 22, 12), caixa_obs, border_radius=6)
            pygame.draw.rect(tela, VERDE_CRT_ESCURO, caixa_obs, 1, border_radius=6)
            tela.blit(
                fonte_crt.render("OBSERVACAO VISUAL:", True, VERDE_CRT),
                (caixa_obs.x + 18, caixa_obs.y + 12),
            )
            texto_obs = dados_cartao["descricao"] or "Sem observacoes registradas."
            y_obs = caixa_obs.y + 38
            for linha in _quebrar_linhas(texto_obs, fonte_menor, caixa_obs.width - 36)[:2]:
                tela.blit(fonte_menor.render(linha, True, BRANCO), (caixa_obs.x + 18, y_obs))
                y_obs += fonte_menor.get_linesize() + 4

        rect_voltar = pygame.Rect(LARGURA_TELA // 2 - 130, 514, 260, 44)
        _desenhar_botao_terminal(
            tela, rect_voltar, "VOLTAR A GUARITA (ESC)", fonte_crt, rect_voltar.collidepoint(pos_mouse)
        )
        return rect_voltar


class Microfone(ObjetoInterativo):
    """
    Objeto do Microfone na mesa e tela de interrogatório com perguntas padronizadas.
    """

    def __init__(self):
        """
        Carrega os sprites do Microfone e define as perguntas padronizadas.

        Parâmetros:
            None.

        Saída:
            None
        """
        base = ObjetoInterativo.de_arquivos(
            "microfone",
            SPRITE_MICROFONE,
            SPRITE_MICROFONE_SELECIONADO,
            POSICOES_GUARITA["microfone"],
        )
        super().__init__("microfone", base.img_normal, base.img_hover, base.rect)
        self.perguntas = list(PERGUNTAS_MICROFONE)

    def desenhar_overlay(self, tela, estado_fase, fontes, pos_mouse, tempo_atual_ms):
        """
        Desenha a janela de interrogatório e a resposta com efeito máquina de escrever.

        Parâmetros:
            tela (pygame.Surface): superfície principal do jogo.
            estado_fase (dict): estado atual da fase.
            fontes (dict): dicionário de fontes carregadas.
            pos_mouse (tuple): posição atual do cursor.
            tempo_atual_ms (int): tempo atual em ms.

        Saídas:
            rects_perguntas (list): lista de pygame.Rect das 3 perguntas.
            rect_voltar (pygame.Rect): retângulo do botão voltar.
        """
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 205))
        tela.blit(overlay, (0, 0))

        visitante = obter_visitante_atual(estado_fase)
        nome_vis = visitante["nome"] if visitante else "---"
        monitor_rect = pygame.Rect(60, 34, LARGURA_TELA - 120, 236)
        pygame.draw.rect(tela, VERDE_PAINEL, monitor_rect, border_radius=8)
        pygame.draw.rect(tela, VERDE_CRT, monitor_rect, 2, border_radius=8)

        fonte_menu = fontes["pequena_menu"]
        fonte_crt = fontes["crt"]
        fonte_peq = fontes["crt_pequena"]

        tela.blit(
            fonte_menu.render(f"INTERROGATORIO MICROFONE - {nome_vis.upper()}", True, VERDE_CRT),
            (monitor_rect.x + 20, monitor_rect.y + 14),
        )
        pygame.draw.line(
            tela, VERDE_CRT_ESCURO, (monitor_rect.x + 16, 78), (monitor_rect.right - 16, 78), 1
        )

        if estado_fase["texto_monitor"]:
            idx_p = estado_fase.get("pergunta_selecionada")
            y_txt = monitor_rect.y + 56
            if idx_p is not None and 0 <= idx_p < len(self.perguntas):
                tela.blit(
                    fonte_peq.render(f"PERGUNTA: {self.perguntas[idx_p]}", True, VERDE_CRT_SUAVE),
                    (monitor_rect.x + 20, y_txt),
                )
                y_txt += 26

            decorrido = tempo_atual_ms - estado_fase["inicio_digitacao_ms"]
            visivel, concluido = obter_texto_digitado(estado_fase["texto_monitor"], decorrido)
            sufixo = "_" if (not concluido and (tempo_atual_ms // 220) % 2 == 0) else ""
            for linha in _quebrar_linhas(visivel + sufixo, fonte_crt, monitor_rect.width - 40)[:5]:
                tela.blit(fonte_crt.render(linha, True, BRANCO), (monitor_rect.x + 20, y_txt))
                y_txt += fonte_crt.get_linesize() + 6

            if not concluido:
                dica = fonte_peq.render("[ESPACO] COMPLETAR TRANSCRICAO", True, VERDE_CRT_SUAVE)
                tela.blit(
                    dica, dica.get_rect(bottomright=(monitor_rect.right - 18, monitor_rect.bottom - 10))
                )
        else:
            inst = fonte_crt.render(
                "Selecione uma pergunta abaixo para iniciar o interrogatorio do visitante.",
                True,
                VERDE_CRT,
            )
            tela.blit(inst, inst.get_rect(center=(monitor_rect.centerx, monitor_rect.y + 140)))

        rects_perguntas = []
        y_btn = 290
        for idx, pergunta in enumerate(self.perguntas):
            rect_q = pygame.Rect(60, y_btn, LARGURA_TELA - 120, 52)
            sel = estado_fase["pergunta_selecionada"] == idx
            _desenhar_botao_terminal(
                tela,
                rect_q,
                pergunta,
                fonte_crt,
                hover=(rect_q.collidepoint(pos_mouse) or sel),
                cor_borda=(BRANCO if sel else VERDE_CRT),
                alinhar_esquerda=True,
            )
            rects_perguntas.append(rect_q)
            y_btn += 64

        rect_voltar = pygame.Rect(LARGURA_TELA // 2 - 130, 514, 260, 44)
        _desenhar_botao_terminal(
            tela, rect_voltar, "VOLTAR A GUARITA (ESC)", fonte_crt, rect_voltar.collidepoint(pos_mouse)
        )
        return rects_perguntas, rect_voltar


class ComputadorMonitor(ObjetoInterativo):
    """
    Objeto do Computador na mesa e interface do Monitor CRT com os 3 aplicativos biométricos.
    """

    def __init__(self):
        """
        Carrega os sprites do computador, a tela CRT base, os 3 ícones e as 3 telas de apps.

        Parâmetros:
            None.

        Saída:
            None
        """
        base_obj = ObjetoInterativo.de_arquivos(
            "computador",
            SPRITE_COMPUTADOR,
            SPRITE_COMPUTADOR_SELECIONADO,
            POSICOES_GUARITA["computador"],
        )
        super().__init__("computador", base_obj.img_normal, base_obj.img_hover, base_obj.rect)

        tam_crt = RECT_MONITOR_CRT.size
        self.base = pygame.transform.smoothscale(
            pygame.image.load(SPRITE_MONITOR_CRT_BASE).convert_alpha(), tam_crt
        )
        self.apps = {
            "bpm": pygame.transform.smoothscale(
                pygame.image.load(SPRITE_MONITOR_APP_BPM).convert_alpha(), tam_crt
            ),
            "temperatura": pygame.transform.smoothscale(
                pygame.image.load(SPRITE_MONITOR_APP_TEMP).convert_alpha(), tam_crt
            ),
            "peso": pygame.transform.smoothscale(
                pygame.image.load(SPRITE_MONITOR_APP_PESO).convert_alpha(), tam_crt
            ),
        }
        self.botoes_apps = {
            "bpm": ObjetoInterativo.de_arquivos(
                "bpm", SPRITE_ICONE_BPM_NORMAL, SPRITE_ICONE_BPM_HOVER, RECTS_ICONES_MONITOR["bpm"]
            ),
            "temperatura": ObjetoInterativo.de_arquivos(
                "temperatura",
                SPRITE_ICONE_TEMP_NORMAL,
                SPRITE_ICONE_TEMP_HOVER,
                RECTS_ICONES_MONITOR["temperatura"],
            ),
            "peso": ObjetoInterativo.de_arquivos(
                "peso",
                SPRITE_ICONE_PESO_NORMAL,
                SPRITE_ICONE_PESO_HOVER,
                RECTS_ICONES_MONITOR["peso"],
            ),
        }

    def desenhar_overlay(self, tela, estado_fase, fontes, pos_mouse, tempo_atual_ms=0):
        """
        Desenha a tela inicial do Monitor CRT com os 3 ícones ou a tela interna do app ativo.

        Parâmetros:
            tela (pygame.Surface): superfície principal do jogo.
            estado_fase (dict): estado atual da fase.
            fontes (dict): dicionário de fontes carregadas.
            pos_mouse (tuple): posição atual do mouse.
            tempo_atual_ms (int): instante atual em ms.

        Saídas:
            controles_monitor (dict): hitboxes de 'apps' e 'voltar_monitor'.
            rect_voltar (pygame.Rect): retângulo do botão voltar à guarita.
        """
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        tela.blit(overlay, (0, 0))

        fonte_crt = fontes["crt"]
        fonte_peq = fontes["crt_pequena"]
        fonte_sub = fontes["monitor_sub"]
        fonte_val = fontes["monitor_valor"]

        app_ativo = estado_fase.get("app_monitor")
        permitidos = estado_fase.get("metodos_permitidos", METODOS_VERIFICACAO)
        visitante = obter_visitante_atual(estado_fase)
        idx_v = min(estado_fase["indice_visitante"] + 1, max(1, len(estado_fase["fila"])))
        tot_v = len(estado_fase["fila"])

        if app_ativo is None:
            tela.blit(self.base, RECT_MONITOR_CRT.topleft)
            titulo = fonte_sub.render(
                f"TERMINAL BIOMETRICO // VISITANTE {idx_v}/{tot_v}", True, VERDE_CRT_BRILHO
            )
            tela.blit(titulo, titulo.get_rect(center=(RECT_MONITOR_CRT.centerx, 82)))
            sub = fonte_peq.render(
                "SELECIONE UM APLICATIVO DE VERIFICACAO", True, VERDE_CRT_SUAVE
            )
            tela.blit(sub, sub.get_rect(center=(RECT_MONITOR_CRT.centerx, 110)))

            rects_apps = {}
            for metodo, btn_app in self.botoes_apps.items():
                em_hover = (metodo in permitidos) and btn_app.em_hover(pos_mouse)
                if metodo in permitidos:
                    btn_app.desenhar(tela, ativo_hover=em_hover)
                    rects_apps[metodo] = btn_app.rect
                    cor_rotulo = BRANCO if em_hover else VERDE_CRT_BRILHO
                else:
                    bloq = btn_app.img_normal.copy()
                    bloq.set_alpha(75)
                    tela.blit(bloq, btn_app.rect.topleft)
                    av = fonte_peq.render("BLOQUEADO", True, CINZA)
                    tela.blit(av, av.get_rect(center=btn_app.rect.center))
                    cor_rotulo = CINZA

                rot = fonte_crt.render(TITULOS_METODOS_MONITOR[metodo], True, cor_rotulo)
                tela.blit(rot, rot.get_rect(center=(btn_app.rect.centerx, 334)))

            rod = fonte_peq.render(
                "COMPARE AS LEITURAS COM O CARTAO E O INTERROGATORIO", True, VERDE_CRT_SUAVE
            )
            tela.blit(rod, rod.get_rect(center=(RECT_MONITOR_CRT.centerx, 434)))

            rect_voltar = pygame.Rect(LARGURA_TELA // 2 - 130, 526, 260, 44)
            _desenhar_botao_terminal(
                tela, rect_voltar, "VOLTAR A GUARITA (ESC)", fonte_crt, rect_voltar.collidepoint(pos_mouse)
            )
            return {"apps": rects_apps, "voltar_monitor": None}, rect_voltar

        tela.blit(self.apps[app_ativo], RECT_MONITOR_CRT.topleft)
        leitura = obter_leitura_monitor(visitante, app_ativo, tempo_atual_ms)
        cab = fonte_peq.render(
            f"{TITULOS_METODOS_MONITOR[app_ativo]} // VISITANTE {idx_v}/{tot_v}",
            True,
            VERDE_CRT_SUAVE,
        )
        tela.blit(cab, cab.get_rect(center=(RECT_MONITOR_CRT.centerx, 78)))

        s_val = fonte_val.render(leitura["valor_texto"], True, VERDE_CRT_BRILHO)
        s_faixa = fonte_crt.render(leitura["faixa_texto"], True, VERDE_CRT_BRILHO)

        if app_ativo == "bpm":
            tela.blit(s_val, s_val.get_rect(midright=(522, 152)))
            tela.blit(s_faixa, s_faixa.get_rect(center=(475, 212)))
        elif app_ativo == "temperatura":
            tela.blit(s_val, s_val.get_rect(midright=(538, 202)))
            tela.blit(s_faixa, s_faixa.get_rect(center=(472, 326)))
        else:
            tela.blit(s_val, s_val.get_rect(midright=(518, 150)))
            barra_ext = pygame.Rect(274, 198, 256, 22)
            larg_p = int((barra_ext.width - 4) * max(0.0, min(1.0, leitura["valor"] / 140.0)))
            if larg_p > 0:
                pygame.draw.rect(
                    tela,
                    VERDE_CRT_BRILHO,
                    pygame.Rect(barra_ext.x + 2, barra_ext.y + 2, larg_p, barra_ext.height - 4),
                )

        rect_voltar_mon = pygame.Rect(140, 526, 240, 44)
        _desenhar_botao_terminal(
            tela, rect_voltar_mon, "VOLTAR AO MONITOR", fonte_crt, rect_voltar_mon.collidepoint(pos_mouse)
        )
        rect_voltar = pygame.Rect(420, 526, 240, 44)
        _desenhar_botao_terminal(
            tela, rect_voltar, "VOLTAR A GUARITA (ESC)", fonte_crt, rect_voltar.collidepoint(pos_mouse)
        )
        return {"apps": {}, "voltar_monitor": rect_voltar_mon}, rect_voltar


class PainelBotoes(ObjetoInterativo):
    """
    Objeto do Painel de Botões na mesa e tela cheia de decisão (Verde e Vermelho).
    """

    def __init__(self):
        """
        Carrega o sprite do painel na mesa e as 3 imagens em tela cheia dos botões.

        Parâmetros:
            None.

        Saída:
            None
        """
        base = ObjetoInterativo.de_arquivos(
            "botao", SPRITE_BOTAO, SPRITE_BOTAO_SELECIONADO, POSICOES_GUARITA["botao"]
        )
        super().__init__("botao", base.img_normal, base.img_hover, base.rect)
        tam = (LARGURA_TELA, ALTURA_TELA)
        self.sprites_tela_cheia = {
            "normal": pygame.transform.smoothscale(
                pygame.image.load(SPRITE_TELA_CHEIA_BOTAO).convert(), tam
            ),
            "verde": pygame.transform.smoothscale(
                pygame.image.load(SPRITE_TELA_CHEIA_VERDE_APERTADO).convert(), tam
            ),
            "vermelho": pygame.transform.smoothscale(
                pygame.image.load(SPRITE_TELA_CHEIA_VERMELHO_APERTADO).convert(), tam
            ),
        }

    def detectar_hover_cheia(self, pos_mouse):
        """
        Identifica se o mouse está sobre o botão Verde ou Vermelho na tela cheia.

        Parâmetros:
            pos_mouse (tuple): coordenadas (x, y) do mouse.

        Saída:
            (str | None): 'verde', 'vermelho' ou None.
        """
        if RECT_BOTAO_VERDE_CHEIA.collidepoint(pos_mouse):
            return "verde"
        if RECT_BOTAO_VERMELHO_CHEIA.collidepoint(pos_mouse):
            return "vermelho"
        return None

    def desenhar_tela_cheia(self, tela, fontes, pos_mouse):
        """
        Desenha a tela cheia dos botões trocando o sprite no hover Verde/Vermelho.

        Parâmetros:
            tela (pygame.Surface): superfície principal do jogo.
            fontes (dict): dicionário de fontes carregadas.
            pos_mouse (tuple): posição atual do mouse.

        Saídas:
            hover_botao (str | None): 'verde', 'vermelho' ou None.
            rect_voltar (pygame.Rect): retângulo do botão voltar à guarita.
        """
        hover_b = self.detectar_hover_cheia(pos_mouse)
        chave = hover_b if hover_b in ("verde", "vermelho") else "normal"
        tela.blit(self.sprites_tela_cheia[chave], (0, 0))

        fonte_crt = fontes["crt"]
        faixa = pygame.Rect(70, 16, LARGURA_TELA - 140, 38)
        pygame.draw.rect(tela, (10, 14, 12), faixa, border_radius=6)
        pygame.draw.rect(tela, VERDE_CRT, faixa, 1, border_radius=6)
        dica = fonte_crt.render(
            "VERDE: APROVAR ENTRADA   |   VERMELHO: ACIONAR INCINERADOR", True, BRANCO
        )
        tela.blit(dica, dica.get_rect(center=faixa.center))

        rect_voltar = pygame.Rect(LARGURA_TELA // 2 - 130, 534, 260, 44)
        _desenhar_botao_terminal(
            tela, rect_voltar, "VOLTAR A GUARITA (ESC)", fonte_crt, rect_voltar.collidepoint(pos_mouse)
        )
        return hover_b, rect_voltar


class SalaGuarita:
    """
    Reúne o fundo, as fontes e as instâncias dos 4 objetos interativos da guarita.
    """

    def __init__(self, fila):
        """
        Inicializa o fundo da guarita, as fontes e os 4 objetos interativos.

        Parâmetros:
            fila (list): lista de visitantes do turno.

        Saída:
            None
        """
        img_fundo = pygame.image.load(SPRITE_FUNDO_JOGO).convert()
        self.fundo = pygame.transform.scale(img_fundo, (LARGURA_TELA, ALTURA_TELA))
        self.fontes = {
            "titulo": pygame.font.Font(FONTE_TITULO[0], 38),
            "menu": pygame.font.Font(FONTE_TITULO[0], 22),
            "pequena_menu": pygame.font.Font(FONTE_TITULO[0], 17),
            "crt": pygame.font.Font(None, 22),
            "crt_pequena": pygame.font.Font(None, 17),
            "monitor_valor": pygame.font.Font(None, 76),
            "monitor_sub": pygame.font.Font(None, 24),
            "cartao": pygame.font.Font(FONTE_CARTAO[0], 18),
            "cartao_pequena": pygame.font.Font(FONTE_CARTAO[0], 15),
            "cartao_tamanhos": {
                tam: pygame.font.Font(FONTE_CARTAO[0], tam) for tam in range(11, 21)
            },
        }
        self.caixa_correio = CaixaCorreio(fila)
        self.computador = ComputadorMonitor()
        self.microfone = Microfone()
        self.painel_botoes = PainelBotoes()
        self.objetos_ordenados = (
            self.caixa_correio,
            self.computador,
            self.microfone,
            self.painel_botoes,
        )

    def detectar_hover(self, pos_mouse):
        """
        Retorna o identificador do objeto da mesa sob o cursor (em ordem de prioridade).

        Parâmetros:
            pos_mouse (tuple): coordenadas (x, y) do mouse.

        Saída:
            (str | None): nome do objeto em hover ou None.
        """
        for obj in (self.painel_botoes, self.microfone, self.computador, self.caixa_correio):
            if obj.em_hover(pos_mouse):
                return obj.nome
        return None

    def desenhar_mesa(self, tela, hover_objeto=None):
        """
        Desenha o fundo da guarita e os 4 objetos interativos.

        Parâmetros:
            tela (pygame.Surface): superfície principal do jogo.
            hover_objeto (str | None): nome do objeto atualmente sob o mouse.

        Saída:
            None
        """
        tela.blit(self.fundo, (0, 0))
        for obj in self.objetos_ordenados:
            obj.desenhar(tela, ativo_hover=(hover_objeto == obj.nome))


# =====================================================================
# FUNÇÕES DE LÓGICA, CARTÃO E FLUXO DA PARTIDA
# =====================================================================

def montar_fila_fase(fase=1, personagens=None):
    """
    Monta a fila de visitantes da fase informada a partir de dados_personagens.txt.

    Parâmetros:
        fase (int): número da fase (padrão 1).
        personagens (dict | None): dicionário opcional já carregado por iniciar_personagens().

    Saída:
        fila (list): lista de dicionários normalizados dos visitantes do turno.
    """
    if personagens is None:
        personagens = iniciar_personagens()

    nomes = FILAS_POR_FASE.get(fase, FILAS_POR_FASE[1])
    fila = []
    for nome in nomes:
        dados_b = personagens[nome]
        fila.append(
            {
                "nome": nome,
                "avatar": AVATARES_PERSONAGENS.get(nome, SPRITE_AVATAR_ID_PERSONAGENS),
                "passou": bool(dados_b.get("passou", False)),
                "humano": bool(dados_b.get("humano", False)),
                "falas": [str(f).strip() for f in dados_b.get("falas", [])],
                "temp_base": int(dados_b.get("temp_base", 0)),
                "temp_max": int(dados_b.get("temp_max", 0)),
                "freq_base": int(dados_b.get("freq_base", 0)),
                "freq_maxim": int(dados_b.get("freq_maxim", 0)),
                "identidade": [str(x).strip() for x in dados_b.get("identidade", [])],
                "registro": [str(x).strip() for x in dados_b.get("registro", [])],
                "Peso": int(dados_b.get("Peso", 0)),
            }
        )
    return fila


def extrair_dados_cartao(visitante):
    """
    Extrai os campos formatados do visitante para o cartão de identidade.

    Parâmetros:
        visitante (dict): dicionário do visitante.

    Saída:
        (dict): dicionário com nome, data_nascimento, id, origem, funcao, peso e descricao.
    """
    identidade = visitante.get("identidade", [])
    registro = visitante.get("registro", [])
    peso_doc = (
        identidade[3].strip()
        if len(identidade) > 3 and str(identidade[3]).strip()
        else str(visitante.get("Peso", 0))
    )
    return {
        "nome": identidade[1].strip() if len(identidade) > 1 else visitante.get("nome", "---"),
        "data_nascimento": identidade[5].strip() if len(identidade) > 5 else "---",
        "id": identidade[0].strip() if len(identidade) > 0 else "---",
        "origem": identidade[4].strip() if len(identidade) > 4 else "---",
        "funcao": registro[5].strip() if len(registro) > 5 else "---",
        "peso": f"{peso_doc} kg",
        "descricao": identidade[2].strip() if len(identidade) > 2 else "",
    }


def obter_especificacoes_campos_cartao(dados_cartao, cartao_rect):
    """
    Calcula as coordenadas e larguras disponíveis para cada linha do cartão.

    Parâmetros:
        dados_cartao (dict): dados extraídos por extrair_dados_cartao().
        cartao_rect (pygame.Rect): retângulo do cartão na tela.

    Saída:
        campos (list): lista de dicionários com pos_x, linha_base_y e limites.
    """
    ex, ey = cartao_rect.width / 962.0, cartao_rect.height / 352.0
    refs = [
        ("nome", dados_cartao["nome"], 436, 64, 900),
        ("data_nascimento", dados_cartao["data_nascimento"], 684, 111, 900),
        ("id", dados_cartao["id"], 390, 157, 900),
        ("origem", dados_cartao["origem"], 468, 203, 900),
        ("funcao", dados_cartao["funcao"], 468, 251, 900),
        ("peso", dados_cartao["peso"], 430, 297, 639),
    ]
    campos = []
    for chave, valor, x_ref, y_ref, x_fim in refs:
        pos_x = cartao_rect.x + int(x_ref * ex)
        limite_dir = cartao_rect.x + int(x_fim * ex)
        campos.append(
            {
                "chave": chave,
                "valor": valor,
                "x_ref": x_ref,
                "y_ref": y_ref,
                "pos_x": pos_x,
                "linha_base_y": cartao_rect.y + int(y_ref * ey),
                "limite_direito": limite_dir,
                "largura_disponivel": max(40, limite_dir - pos_x),
            }
        )
    return campos


def ajustar_render_campo_cartao(
    valor, largura_max, tamanho_inicial=18, tamanho_minimo=11, fontes_cache=None
):
    """
    Escolhe o tamanho da fonte VCR ou quebra linhas para caber no espaço do cartão.

    Parâmetros:
        valor (str): texto do campo.
        largura_max (int): largura máxima disponível em pixels.
        tamanho_inicial (int): maior tamanho de fonte testado.
        tamanho_minimo (int): menor tamanho de fonte antes de quebrar linha.
        fontes_cache (dict | None): dicionário opcional {tamanho: Font}.

    Saídas:
        fonte (pygame.font.Font): fonte selecionada.
        linhas (list): lista com 1 ou 2 linhas ajustadas.
    """
    texto = str(valor)
    for tam in range(tamanho_inicial, tamanho_minimo - 1, -1):
        fonte = (
            fontes_cache[tam]
            if fontes_cache and tam in fontes_cache
            else pygame.font.Font(FONTE_CARTAO[0], tam)
        )
        if fonte.size(texto)[0] <= largura_max:
            return fonte, [texto]

    f_min = (
        fontes_cache[tamanho_minimo]
        if fontes_cache and tamanho_minimo in fontes_cache
        else pygame.font.Font(FONTE_CARTAO[0], tamanho_minimo)
    )
    linhas = _quebrar_linhas(texto, f_min, largura_max) or [""]
    if len(linhas) > 2:
        linhas = [linhas[0], " ".join(linhas[1:])]
    ajustadas = []
    for linha in linhas[:2]:
        while linha and f_min.size(linha)[0] > largura_max:
            linha = linha[:-1]
        ajustadas.append(linha)
    return f_min, ajustadas


def iniciar_estado_fase_1(dados, fila=None, fase=1, metodos_por_fase=None):
    """
    Inicializa o dicionário de estado da partida no estado 'inicio_turno'.

    Parâmetros:
        dados (dict): dicionário global do jogador.
        fila (list | None): fila opcional de visitantes.
        fase (int): número da fase atual.
        metodos_por_fase (dict | None): mapa opcional de métodos liberados por fase.

    Saída:
        (dict): estado mutável da partida.
    """
    mapa = METODOS_POR_FASE if metodos_por_fase is None else metodos_por_fase
    metodos = tuple(m for m in METODOS_VERIFICACAO if m in mapa.get(fase, METODOS_VERIFICACAO))
    if fila is None:
        fila = montar_fila_fase(fase=fase)

    dados["fase"] = fase
    dados["acertos"] = 0
    dados["erros"] = 0

    return {
        "fase": fase,
        "estado_atual": "inicio_turno",
        "subtela": "guarita",
        "fila": fila,
        "indice_visitante": 0,
        "botoes_travados": False,
        "pergunta_selecionada": None,
        "texto_monitor": "",
        "inicio_digitacao_ms": 0,
        "metodos_permitidos": metodos,
        "app_monitor": None,
        "relatorio_auditoria": "",
        "resultado_auditoria": None,
        "inicio_auditoria_ms": 0,
        "duracao_auditoria_ms": 2200,
        "acertos_turno": 0,
        "erros_turno": 0,
    }


def avancar_inicio_turno(estado_fase, dados):
    """
    Avança do estado 'inicio_turno' para 'triagem' zerando contadores e índice.

    Parâmetros:
        estado_fase (dict): estado atual da fase.
        dados (dict): dicionário global do jogador.

    Saída:
        (dict): estado_fase atualizado.
    """
    if estado_fase["estado_atual"] == "inicio_turno":
        dados["acertos"] = 0
        dados["erros"] = 0
        estado_fase.update(
            {
                "acertos_turno": 0,
                "erros_turno": 0,
                "indice_visitante": 0,
                "estado_atual": "triagem",
                "subtela": "guarita",
                "app_monitor": None,
                "botoes_travados": False,
                "pergunta_selecionada": None,
                "texto_monitor": "",
                "relatorio_auditoria": "",
                "resultado_auditoria": None,
            }
        )
    return estado_fase


def obter_visitante_atual(estado_fase):
    """
    Retorna o visitante atual da fila conforme indice_visitante.

    Parâmetros:
        estado_fase (dict): estado atual da fase.

    Saída:
        (dict | None): visitante atual ou None.
    """
    idx = estado_fase.get("indice_visitante", 0)
    fila = estado_fase.get("fila", [])
    return fila[idx] if 0 <= idx < len(fila) else None


def selecionar_pergunta_microfone(estado_fase, indice_pergunta, tempo_atual_ms=0):
    """
    Seleciona uma pergunta padronizada e inicia a digitação da resposta no monitor.

    Parâmetros:
        estado_fase (dict): estado atual da fase.
        indice_pergunta (int): índice da pergunta (0 a 2).
        tempo_atual_ms (int): instante atual em ms.

    Saída:
        resposta (str): fala selecionada do visitante.
    """
    visitante = obter_visitante_atual(estado_fase)
    if visitante is None or not (0 <= indice_pergunta < len(PERGUNTAS_MICROFONE)):
        return ""

    falas = visitante.get("falas", [])
    resposta = (
        str(falas[indice_pergunta]).strip()
        if indice_pergunta < len(falas)
        else "Sem resposta registrada."
    )
    estado_fase["pergunta_selecionada"] = indice_pergunta
    estado_fase["texto_monitor"] = resposta
    estado_fase["inicio_digitacao_ms"] = tempo_atual_ms
    return resposta


def obter_texto_digitado(texto_completo, decorrido_ms, ms_por_letra=25):
    """
    Retorna o trecho de texto já revelado pelo efeito máquina de escrever.

    Parâmetros:
        texto_completo (str): texto integral.
        decorrido_ms (int): tempo decorrido em ms.
        ms_por_letra (int): tempo em ms por letra.

    Saídas:
        visivel (str): texto visível até o momento.
        concluido (bool): True quando todo o texto foi exibido.
    """
    if not texto_completo or ms_por_letra <= 0:
        return texto_completo or "", True
    qtd = max(0, int(decorrido_ms // ms_por_letra))
    return (texto_completo, True) if qtd >= len(texto_completo) else (texto_completo[:qtd], False)


def obter_leitura_monitor(visitante, app, tempo_atual_ms=0):
    """
    Calcula a leitura biométrica neutra do visitante para o aplicativo do monitor.

    Parâmetros:
        visitante (dict | None): visitante atual.
        app (str): 'bpm', 'temperatura' ou 'peso'.
        tempo_atual_ms (int): tempo atual em ms.

    Saída:
        (dict): dados numéricos e textos formatados para exibição no app.
    """
    if visitante is None:
        return {"app": app, "valor": 0, "valor_texto": "--", "unidade": "", "faixa_texto": ""}

    fator = (1.0 - math.cos(max(0, tempo_atual_ms) / 650.0)) * 0.5
    if app == "bpm":
        b, m = int(visitante.get("freq_base", 0)), int(visitante.get("freq_maxim", 0))
        val = int(round(min(b, m) + abs(m - b) * fator))
        return {
            "app": "bpm",
            "valor": val,
            "valor_texto": str(val),
            "unidade": "BPM",
            "faixa_texto": f"FAIXA: {b} - {m} BPM",
        }
    if app == "temperatura":
        b, m = int(visitante.get("temp_base", 0)), int(visitante.get("temp_max", 0))
        val = int(round(min(b, m) + abs(m - b) * fator))
        return {
            "app": "temperatura",
            "valor": val,
            "valor_texto": str(val),
            "unidade": "°C",
            "faixa_texto": f"FAIXA: {b} - {m} °C",
        }
    peso = int(visitante.get("Peso", 0))
    return {
        "app": "peso",
        "valor": peso,
        "valor_texto": str(peso),
        "unidade": "kg",
        "faixa_texto": f"MEDICAO BALANCA: {peso} kg",
    }


def avaliar_decisao_visitante(estado_fase, dados, decisao, tempo_atual_ms=0):
    """
    Registra a decisão ('aprovar' ou 'incinerar') internamente e inicia 'auditoria'.

    Parâmetros:
        estado_fase (dict): estado atual da fase.
        dados (dict): dicionário global do jogador.
        decisao (str): 'aprovar' ou 'incinerar'.
        tempo_atual_ms (int): instante da decisão em ms.

    Saída:
        (dict): estado_fase atualizado.
    """
    visitante = obter_visitante_atual(estado_fase)
    if (
        estado_fase["estado_atual"] != "triagem"
        or estado_fase["botoes_travados"]
        or decisao not in ("aprovar", "incinerar")
        or visitante is None
    ):
        return estado_fase

    eh_humano = bool(visitante["humano"])
    acertou = (decisao == "aprovar" and eh_humano) or (decisao == "incinerar" and not eh_humano)
    if acertou:
        dados["acertos"] += 1
        estado_fase["acertos_turno"] += 1
    else:
        dados["erros"] += 1
        estado_fase["erros_turno"] += 1

    acao = "ENTRADA LIBERADA" if decisao == "aprovar" else "ENCAMINHADO AO INCINERADOR"
    estado_fase.update(
        {
            "botoes_travados": True,
            "estado_atual": "auditoria",
            "subtela": "guarita",
            "app_monitor": None,
            "inicio_auditoria_ms": tempo_atual_ms,
            "resultado_auditoria": {"acertou": acertou, "decisao": decisao},
            "relatorio_auditoria": (
                f"REGISTRO CONCLUIDO: {visitante['nome']} | "
                f"{acao}. CHAMANDO PROXIMO VISITANTE..."
            ),
        }
    )
    return estado_fase


def avancar_pos_auditoria(estado_fase, tempo_atual_ms=None):
    """
    Avança para o próximo visitante ou para 'fim_turno' após o tempo de registro.

    Parâmetros:
        estado_fase (dict): estado atual da fase.
        tempo_atual_ms (int | None): instante atual em ms.

    Saída:
        (dict): estado_fase atualizado.
    """
    if estado_fase["estado_atual"] != "auditoria":
        return estado_fase
    if tempo_atual_ms is not None:
        if tempo_atual_ms - estado_fase["inicio_auditoria_ms"] < estado_fase["duracao_auditoria_ms"]:
            return estado_fase

    estado_fase["indice_visitante"] += 1
    estado_fase["botoes_travados"] = False
    estado_fase["pergunta_selecionada"] = None
    estado_fase["texto_monitor"] = ""
    estado_fase["relatorio_auditoria"] = ""
    estado_fase["resultado_auditoria"] = None
    estado_fase["subtela"] = "guarita"
    estado_fase["app_monitor"] = None
    estado_fase["estado_atual"] = (
        "fim_turno"
        if estado_fase["indice_visitante"] >= len(estado_fase["fila"])
        else "triagem"
    )
    return estado_fase


# =====================================================================
# RENDERIZAÇÃO DAS TELAS DO TURNO E LOOP PRINCIPAL DA FASE
# =====================================================================

def _desenhar_inicio_turno(tela, fontes, tempo_atual_ms, dia=1):
    """
    Desenha a tela inicial de CRT com o número do dia e o boletim de protocolo.

    Parâmetros:
        tela (pygame.Surface): superfície principal do jogo.
        fontes (dict): dicionário de fontes da SalaGuarita.
        tempo_atual_ms (int): tempo atual em ms.
        dia (int): número do dia/fase.

    Saída:
        None
    """
    tela.fill(PRETO)
    moldura = pygame.Rect(48, 42, LARGURA_TELA - 96, ALTURA_TELA - 84)
    pygame.draw.rect(tela, (6, 20, 10), moldura, border_radius=8)
    pygame.draw.rect(tela, VERDE_CRT, moldura, 2, border_radius=8)

    f_tit, f_crt, f_menu = fontes["titulo"], fontes["crt"], fontes["menu"]
    tela.blit(
        f_tit.render(f"DIA {dia}", True, VERDE_CRT),
        f_tit.render(f"DIA {dia}", True, VERDE_CRT).get_rect(center=(LARGURA_TELA // 2, 96)),
    )
    sub = f_menu.render("TERMINAL GUARITA ALPHA-04", True, VERDE_CRT)
    tela.blit(sub, sub.get_rect(center=(LARGURA_TELA // 2, 142)))

    caixa = pygame.Rect(78, 174, LARGURA_TELA - 156, 272)
    pygame.draw.rect(tela, (4, 14, 8), caixa, border_radius=6)
    pygame.draw.rect(tela, VERDE_CRT_ESCURO, caixa, 1, border_radius=6)
    tela.blit(
        f_crt.render("BOLETIM DE PROTOCOLO DO TURNO:", True, BRANCO),
        (caixa.x + 22, caixa.y + 18),
    )

    regras = [
        "- 6 visitantes aguardam triagem na comporta externa.",
        "- Caixa de Correio: confira identidade, funcao e peso declarado.",
        "- Microfone: faca as perguntas padronizadas e leia as falas.",
        "- Computador: consulte Batimentos (BPM), Temperatura (C) e Peso (kg).",
        "- Painel de Botoes: VERDE libera entrada | VERMELHO aciona incinerador.",
        "- Cada decisao e registrada e avanca para o proximo visitante.",
    ]
    y = caixa.y + 54
    for regra in regras:
        for linha in _quebrar_linhas(regra, f_crt, caixa.width - 44):
            tela.blit(f_crt.render(linha, True, VERDE_CRT), (caixa.x + 22, y))
            y += 28
        y += 4

    if (tempo_atual_ms // 450) % 2 == 0:
        aviso = f_menu.render("PRESSIONE [ESPACO] PARA INICIAR", True, BRANCO)
        tela.blit(aviso, aviso.get_rect(center=(LARGURA_TELA // 2, 496)))


def _desenhar_fim_turno(tela, estado_fase, fontes, pos_mouse):
    """
    Desenha a tela de encerramento do turno sem revelar acertos ou erros.

    Parâmetros:
        tela (pygame.Surface): superfície principal do jogo.
        estado_fase (dict): estado atual da fase.
        fontes (dict): dicionário de fontes da SalaGuarita.
        pos_mouse (tuple): posição atual do mouse.

    Saída:
        rect_menu (pygame.Rect): retângulo do botão de voltar ao menu.
    """
    tela.fill(PRETO)
    painel = pygame.Rect(70, 55, LARGURA_TELA - 140, ALTURA_TELA - 110)
    pygame.draw.rect(tela, (8, 22, 12), painel, border_radius=8)
    pygame.draw.rect(tela, VERDE_CRT, painel, 2, border_radius=8)

    f_tit, f_menu, f_crt = fontes["titulo"], fontes["menu"], fontes["crt"]
    dia = estado_fase.get("fase", 1)
    tit = f_tit.render(f"FIM DO TURNO - DIA {dia}", True, VERDE_CRT)
    tela.blit(tit, tit.get_rect(center=(LARGURA_TELA // 2, 122)))
    pygame.draw.line(
        tela, VERDE_CRT_ESCURO, (painel.x + 36, 166), (painel.right - 36, 166), 1
    )

    caixa = pygame.Rect(106, 194, LARGURA_TELA - 212, 214)
    pygame.draw.rect(tela, (4, 14, 8), caixa, border_radius=6)
    pygame.draw.rect(tela, VERDE_CRT_ESCURO, caixa, 1, border_radius=6)

    total = len(estado_fase["fila"])
    linhas = [
        (f"VISITANTES TRIADOS: {total} / {total}", BRANCO),
        ("REGISTROS ENVIADOS AO TERMINAL ALPHA-04.", VERDE_CRT),
        (f"EXPEDIENTE DO DIA {dia} CONCLUIDO.", CINZA),
    ]
    y = caixa.y + 50
    for texto, cor in linhas:
        surf = f_menu.render(texto, True, cor)
        tela.blit(surf, surf.get_rect(center=(LARGURA_TELA // 2, y)))
        y += 56

    rect_menu = pygame.Rect(LARGURA_TELA // 2 - 145, 452, 290, 50)
    _desenhar_botao_terminal(
        tela, rect_menu, "VOLTAR AO MENU (ESPACO)", f_crt, rect_menu.collidepoint(pos_mouse)
    )
    return rect_menu


def renderizar_frame_fase(tela, estado_fase, sala, pos_mouse, tempo_atual_ms):
    """
    Renderiza um frame completo da fase usando as classes de SalaGuarita.

    Parâmetros:
        tela (pygame.Surface): superfície principal do jogo.
        estado_fase (dict): estado atual da fase.
        sala (SalaGuarita): instância da sala com os 4 objetos.
        pos_mouse (tuple): posição atual do mouse.
        tempo_atual_ms (int): instante atual em ms.

    Saída:
        controles (dict): hitboxes ativas no frame atual.
    """
    controles = {
        "voltar": None,
        "voltar_monitor": None,
        "perguntas": [],
        "apps_monitor": {},
        "menu": None,
    }
    estado_atual = estado_fase["estado_atual"]
    dia = estado_fase.get("fase", 1)

    if estado_atual == "inicio_turno":
        _desenhar_inicio_turno(tela, sala.fontes, tempo_atual_ms, dia=dia)
        return controles

    if estado_atual == "fim_turno":
        controles["menu"] = _desenhar_fim_turno(tela, estado_fase, sala.fontes, pos_mouse)
        return controles

    hover_obj = (
        sala.detectar_hover(pos_mouse)
        if estado_atual == "triagem" and estado_fase["subtela"] == "guarita"
        else None
    )
    sala.desenhar_mesa(tela, hover_objeto=hover_obj)

    f_peq = sala.fontes["crt_pequena"]
    idx_vis = min(estado_fase["indice_visitante"] + 1, len(estado_fase["fila"]))
    hud_surf = f_peq.render(f"DIA {dia} | VISITANTE {idx_vis}/{len(estado_fase['fila'])}", True, VERDE_CRT)
    hud_box = pygame.Rect(14, 12, hud_surf.get_width() + 24, 28)
    pygame.draw.rect(tela, (10, 18, 12), hud_box, border_radius=4)
    pygame.draw.rect(tela, VERDE_CRT_ESCURO, hud_box, 1, border_radius=4)
    tela.blit(hud_surf, hud_surf.get_rect(center=hud_box.center))

    if estado_atual == "auditoria":
        veu = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        veu.fill((0, 0, 0, 110))
        tela.blit(veu, (0, 0))

        banner = pygame.Rect(90, 492, LARGURA_TELA - 180, 76)
        pygame.draw.rect(tela, (8, 18, 10), banner, border_radius=6)
        pygame.draw.rect(tela, VERDE_CRT, banner, 2, border_radius=6)
        linhas_aud = _quebrar_linhas(
            estado_fase["relatorio_auditoria"], sala.fontes["crt"], banner.width - 32
        )[:2]
        y_aud = banner.centery - (len(linhas_aud) * 24) // 2 + 12
        for linha in linhas_aud:
            s_aud = sala.fontes["crt"].render(linha, True, VERDE_CRT)
            tela.blit(s_aud, s_aud.get_rect(center=(banner.centerx, y_aud)))
            y_aud += 24
        return controles

    subtela = estado_fase["subtela"]
    if subtela == "correio":
        controles["voltar"] = sala.caixa_correio.desenhar_popup(
            tela, obter_visitante_atual(estado_fase), sala.fontes, pos_mouse
        )
    elif subtela == "microfone":
        controles["perguntas"], controles["voltar"] = sala.microfone.desenhar_overlay(
            tela, estado_fase, sala.fontes, pos_mouse, tempo_atual_ms
        )
    elif subtela == "computador":
        c_mon, controles["voltar"] = sala.computador.desenhar_overlay(
            tela, estado_fase, sala.fontes, pos_mouse, tempo_atual_ms
        )
        controles["apps_monitor"] = c_mon["apps"]
        controles["voltar_monitor"] = c_mon["voltar_monitor"]
    elif subtela == "botoes":
        _, controles["voltar"] = sala.painel_botoes.desenhar_tela_cheia(
            tela, sala.fontes, pos_mouse
        )

    return controles


def _tocar_bip_monitor(som_monitor, dados):
    """
    Toca o efeito sonoro curto do monitor respeitando o volume configurado.

    Parâmetros:
        som_monitor (pygame.mixer.Sound | None): efeito sonoro carregado.
        dados (dict): dicionário de dados do jogador.

    Saída:
        None
    """
    if som_monitor is not None:
        som_monitor.set_volume(float(dados.get("volume", 0.8)))
        som_monitor.stop()
        som_monitor.play(maxtime=550)


def executar_fase_1(tela, clock, dados):
    """
    Executa o loop principal da Fase (inicio_turno, triagem, auditoria e fim_turno).

    Parâmetros:
        tela (pygame.Surface): superfície principal do jogo.
        clock (pygame.time.Clock): relógio para controle de FPS.
        dados (dict): dicionário de estado e configurações do jogador.

    Saída:
        dados (dict): dicionário atualizado ao retornar ao menu.
    """
    estado_fase = iniciar_estado_fase_1(dados, fase=dados.get("fase", 1))
    sala = SalaGuarita(estado_fase["fila"])

    # Config de áudio
    executar_musica(dados, SOM_FUNDO)
    som_monitor = pygame.mixer.Sound(SOM_MONITOR)
    musica_fim_tocando = False
    controles = {"voltar": None, "voltar_monitor": None, "perguntas": [], "apps_monitor": {}, "menu": None}

    while True:
        tempo_atual_ms = pygame.time.get_ticks()
        pos_mouse = pygame.mouse.get_pos()

        if estado_fase["estado_atual"] == "auditoria":
            avancar_pos_auditoria(estado_fase, tempo_atual_ms)
            if estado_fase["estado_atual"] == "fim_turno" and not musica_fim_tocando:
                executar_musica(dados, MUSICA_FIM_FASE)
                musica_fim_tocando = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo(dados)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif evento.key == pygame.K_ESCAPE:
                    if estado_fase["subtela"] == "computador" and estado_fase.get("app_monitor"):
                        estado_fase["app_monitor"] = None
                    elif estado_fase["estado_atual"] == "triagem" and estado_fase["subtela"] != "guarita":
                        estado_fase["subtela"] = "guarita"
                    elif estado_fase["estado_atual"] in ("inicio_turno", "fim_turno"):
                        pygame.mixer.music.stop()
                        dados["tela"] = "menu"
                        registrar_dados(dados, DADOS)
                        return dados
                elif evento.key == pygame.K_SPACE:
                    if estado_fase["estado_atual"] == "inicio_turno":
                        avancar_inicio_turno(estado_fase, dados)
                        registrar_dados(dados, DADOS)
                    elif estado_fase["subtela"] == "microfone" and estado_fase["texto_monitor"]:
                        estado_fase["inicio_digitacao_ms"] = (
                            tempo_atual_ms - len(estado_fase["texto_monitor"]) * 30 - 100
                        )
                    elif estado_fase["estado_atual"] == "fim_turno":
                        pygame.mixer.music.stop()
                        dados["tela"] = "menu"
                        registrar_dados(dados, DADOS)
                        return dados

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                est = estado_fase["estado_atual"]
                sub = estado_fase["subtela"]

                if est == "fim_turno" and controles["menu"] and controles["menu"].collidepoint(pos):
                    pygame.mixer.music.stop()
                    dados["tela"] = "menu"
                    registrar_dados(dados, DADOS)
                    return dados

                elif est == "triagem" and not estado_fase["botoes_travados"]:
                    if sub == "guarita":
                        mapa = {
                            "caixa_correio": "correio",
                            "microfone": "microfone",
                            "computador": "computador",
                            "botao": "botoes",
                        }
                        alvo = sala.detectar_hover(pos)
                        if alvo in mapa:
                            estado_fase["subtela"] = mapa[alvo]
                            estado_fase["app_monitor"] = None

                    elif controles["voltar"] and controles["voltar"].collidepoint(pos):
                        estado_fase["subtela"] = "guarita"
                        estado_fase["app_monitor"] = None

                    elif sub == "microfone":
                        for idx, rect_q in enumerate(controles["perguntas"]):
                            if rect_q.collidepoint(pos):
                                selecionar_pergunta_microfone(estado_fase, idx, tempo_atual_ms)
                                _tocar_bip_monitor(som_monitor, dados)
                                break

                    elif sub == "computador":
                        if controles["voltar_monitor"] and controles["voltar_monitor"].collidepoint(pos):
                            estado_fase["app_monitor"] = None
                            _tocar_bip_monitor(som_monitor, dados)
                        else:
                            for app, rect_app in controles["apps_monitor"].items():
                                if rect_app.collidepoint(pos):
                                    estado_fase["app_monitor"] = app
                                    _tocar_bip_monitor(som_monitor, dados)
                                    break

                    elif sub == "botoes":
                        escolhido = sala.painel_botoes.detectar_hover_cheia(pos)
                        if escolhido in ("verde", "vermelho"):
                            decisao = "aprovar" if escolhido == "verde" else "incinerar"
                            avaliar_decisao_visitante(estado_fase, dados, decisao, tempo_atual_ms)
                            _tocar_bip_monitor(som_monitor, dados)
                            registrar_dados(dados, DADOS)

        controles = renderizar_frame_fase(
            tela, estado_fase, sala, pos_mouse, tempo_atual_ms
        )
        pygame.display.update()
        clock.tick(FPS)


def executar_fase(tela, clock, dados):
    """
    Direciona a execução para a fase correspondente ao progresso atual do jogador.

    Parâmetros:
        tela (pygame.Surface): superfície principal do jogo.
        clock (pygame.time.Clock): relógio usado para controlar o FPS.
        dados (dict): dicionário de estado e configurações do jogador.

    Saída:
        None
    """
    if dados["fase"] in (1, 2, 3):
        executar_fase_1(tela, clock, dados)
