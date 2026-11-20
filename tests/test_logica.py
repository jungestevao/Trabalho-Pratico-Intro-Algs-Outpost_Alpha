import os
import pygame
from src.config import (
    ALTURA_TELA,
    AVATARES_PERSONAGENS,
    FONTE_TITULO,
    LARGURA_TELA,
    SPRITE_AVATAR_ID_PERSONAGENS,
    SPRITE_AVATAR_LAERTE_XAVIER,
    SPRITE_AVATAR_MARCOS_SILVAR,
    SPRITE_ICONE_BPM_HOVER,
    SPRITE_ICONE_BPM_NORMAL,
    SPRITE_ICONE_PESO_HOVER,
    SPRITE_ICONE_PESO_NORMAL,
    SPRITE_ICONE_TEMP_HOVER,
    SPRITE_ICONE_TEMP_NORMAL,
    SPRITE_MONITOR_APP_BPM,
    SPRITE_MONITOR_APP_PESO,
    SPRITE_MONITOR_APP_TEMP,
    SPRITE_MONITOR_CRT_BASE,
)
from src.dados import (
    iniciar_dados,
    iniciar_personagens,
    ler_dados,
    registrar_dados,
)
from src.fase import (
    CaixaCorreio,
    ComputadorMonitor,
    METODOS_POR_FASE,
    METODOS_VERIFICACAO,
    Microfone,
    ObjetoInterativo,
    PERGUNTAS_MICROFONE,
    PainelBotoes,
    RECTS_ICONES_MONITOR,
    RECT_MONITOR_CRT,
    SalaGuarita,
    ajustar_render_campo_cartao,
    avaliar_decisao_visitante,
    avancar_inicio_turno,
    avancar_pos_auditoria,
    extrair_dados_cartao,
    iniciar_estado_fase_1,
    montar_fila_fase,
    obter_especificacoes_campos_cartao,
    obter_leitura_monitor,
    obter_texto_digitado,
    obter_visitante_atual,
    renderizar_frame_fase,
    selecionar_pergunta_microfone,
)


def _dados_padrao():
    """Cria um dicionario base de progresso do jogador para testes."""
    return {
        "tela": "jogo",
        "fase": 1,
        "erros": 0,
        "acertos": 0,
        "historia": False,
        "volume": 0.7,
    }


def test_iniciar_personagens_carrega_21_incluindo_laerte():
    """Deve carregar os 21 personagens com Laerte Xavier definido como humano."""
    personagens = iniciar_personagens()
    assert len(personagens) == 21
    assert "Laerte Xavier" in personagens
    laerte = personagens["Laerte Xavier"]
    assert laerte["humano"] is True
    assert laerte["passou"] is False
    assert len(laerte["falas"]) == 3
    assert len(laerte["identidade"]) == 6
    assert len(laerte["registro"]) == 7
    assert isinstance(laerte["Peso"], int)


def test_dados_jogador_round_trip(tmp_path):
    """Deve criar, atualizar e reler dados_jogador mantendo os tipos originais."""
    caminho = str(tmp_path / "dados_teste.txt")
    iniciar_dados(caminho)
    lido = ler_dados(caminho)
    assert lido["fase"] == 1
    assert lido["historia"] is True
    assert lido["volume"] == 0.8

    lido["acertos"] = 4
    lido["erros"] = 2
    lido["tela"] = "jogo"
    registrar_dados(lido, caminho)

    relido = ler_dados(caminho)
    assert relido["acertos"] == 4
    assert relido["erros"] == 2
    assert relido["tela"] == "jogo"


def test_montar_fila_fase_seis_visitantes_e_avatares():
    """Deve montar fila com os 5 primeiros personagens seguidos de Laerte Xavier."""
    fila = montar_fila_fase(1)
    nomes = [visitante["nome"] for visitante in fila]
    assert nomes == [
        "Marcos Silva",
        "Elena Vance",
        "Jonas Ribeiro",
        "Clara Mendes",
        "Artur Kovic",
        "Laerte Xavier",
    ]
    assert AVATARES_PERSONAGENS["Marcos Silva"] == SPRITE_AVATAR_MARCOS_SILVAR
    assert AVATARES_PERSONAGENS["Laerte Xavier"] == SPRITE_AVATAR_LAERTE_XAVIER
    for visitante in fila:
        assert os.path.exists(visitante["avatar"])


def test_extrair_dados_cartao_visitante():
    """Deve extrair identidade, funcao e peso formatado do visitante atual."""
    fila = montar_fila_fase(1)
    laerte = fila[-1]
    cartao = extrair_dados_cartao(laerte)
    assert cartao["nome"] == "Laerte Xavier"
    assert cartao["id"] == "4210-L"
    assert cartao["origem"] == "Zona Central"
    assert "Engenharia de Software" in cartao["funcao"]
    assert cartao["peso"] == f"{laerte['Peso']} kg"


def test_transicao_inicio_turno_para_triagem():
    """Deve reiniciar contadores e iniciar triagem no indice 0 ao avancar inicio_turno."""
    dados = _dados_padrao()
    dados["acertos"] = 3
    dados["erros"] = 2
    estado = iniciar_estado_fase_1(dados)
    assert estado["estado_atual"] == "inicio_turno"

    avancar_inicio_turno(estado, dados)
    assert estado["estado_atual"] == "triagem"
    assert estado["indice_visitante"] == 0
    assert dados["acertos"] == 0
    assert dados["erros"] == 0
    assert obter_visitante_atual(estado)["nome"] == "Marcos Silva"


def test_auditoria_quatro_combinacoes_pontuacao():
    """Deve contabilizar acertos e erros corretamente para todas as combinacoes."""
    combinacoes = [
        ("Marcos Silva", "aprovar", 1, 0),
        ("Elena Vance", "incinerar", 1, 0),
        ("Jonas Ribeiro", "aprovar", 0, 1),
        ("Clara Mendes", "incinerar", 0, 1),
    ]
    por_nome = {v["nome"]: v for v in montar_fila_fase(1)}

    for nome, decisao, esp_acertos, esp_erros in combinacoes:
        dados = _dados_padrao()
        estado = iniciar_estado_fase_1(dados, fila=[por_nome[nome]])
        avancar_inicio_turno(estado, dados)
        avaliar_decisao_visitante(estado, dados, decisao, tempo_atual_ms=100)
        assert estado["estado_atual"] == "auditoria"
        assert estado["botoes_travados"] is True
        assert dados["acertos"] == esp_acertos
        assert dados["erros"] == esp_erros


def test_turno_completo_seis_visitantes_sem_game_over_precoce():
    """Deve percorrer todos os 6 visitantes ate fim_turno mesmo com 6 erros."""
    dados = _dados_padrao()
    estado = iniciar_estado_fase_1(dados)
    avancar_inicio_turno(estado, dados)

    for i in range(6):
        visitante = obter_visitante_atual(estado)
        decisao_errada = "incinerar" if visitante["humano"] else "aprovar"
        avaliar_decisao_visitante(estado, dados, decisao_errada, tempo_atual_ms=1000)
        assert estado["estado_atual"] == "auditoria"

        avancar_pos_auditoria(estado, tempo_atual_ms=1500)
        assert estado["estado_atual"] == "auditoria"
        assert estado["indice_visitante"] == i

        avancar_pos_auditoria(estado, tempo_atual_ms=4000)
        if i < 5:
            assert estado["estado_atual"] == "triagem"
            assert estado["indice_visitante"] == i + 1
        else:
            assert estado["estado_atual"] == "fim_turno"
            assert estado["indice_visitante"] == 6

    assert dados["acertos"] == 0
    assert dados["erros"] == 6


def test_microfone_perguntas_padronizadas_e_maquina_escrever():
    """Deve fornecer 3 perguntas padronizadas e revelar resposta gradualmente."""
    assert len(PERGUNTAS_MICROFONE) == 3
    dados = _dados_padrao()
    estado = iniciar_estado_fase_1(dados)
    avancar_inicio_turno(estado, dados)

    resp = selecionar_pergunta_microfone(estado, 2, tempo_atual_ms=200)
    assert resp == estado["fila"][0]["falas"][2]
    assert estado["pergunta_selecionada"] == 2

    parcial, concluido = obter_texto_digitado(resp, decorrido_ms=125, ms_por_letra=25)
    assert parcial == resp[:5]
    assert concluido is False

    completo, concluido_fim = obter_texto_digitado(
        resp, decorrido_ms=len(resp) * 30, ms_por_letra=25
    )
    assert completo == resp
    assert concluido_fim is True


def test_classes_guarita_monitor_e_leituras(monkeypatch):
    """Deve instanciar SalaGuarita e validar objetos, monitor CRT e leituras."""
    caminhos = (
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
    )
    for caminho in caminhos:
        assert os.path.exists(caminho), f"Asset ausente: {caminho}"

    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    fila = montar_fila_fase(1)
    sala = SalaGuarita(fila)
    assert isinstance(sala.caixa_correio, CaixaCorreio)
    assert isinstance(sala.computador, ComputadorMonitor)
    assert isinstance(sala.microfone, Microfone)
    assert isinstance(sala.painel_botoes, PainelBotoes)
    for obj in sala.objetos_ordenados:
        assert isinstance(obj, ObjetoInterativo)

    assert sala.computador.base.get_size() == RECT_MONITOR_CRT.size
    for metodo in METODOS_VERIFICACAO:
        btn = sala.computador.botoes_apps[metodo]
        assert btn.em_hover(RECTS_ICONES_MONITOR[metodo].center) is True
        assert btn.img_normal.get_at((0, 0)).a == 0

    assert sala.detectar_hover((120, 200)) == "caixa_correio"
    assert sala.detectar_hover((380, 300)) == "computador"
    assert sala.detectar_hover((130, 420)) == "microfone"
    assert sala.detectar_hover((620, 480)) == "botao"
    assert sala.painel_botoes.detectar_hover_cheia((296, 219)) == "verde"
    assert sala.painel_botoes.detectar_hover_cheia((501, 220)) == "vermelho"

    elena = fila[1]
    assert extrair_dados_cartao(elena)["peso"] == "58 kg"
    assert obter_leitura_monitor(elena, "peso", 500)["valor"] == 108


def test_ocultacao_total_acertos_erros_e_cartao(monkeypatch):
    """Nao deve expor acertos/erros na tela e deve manter os textos dentro do cartao."""
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    tela_a = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    tela_b = pygame.Surface((LARGURA_TELA, ALTURA_TELA))

    fila = montar_fila_fase(1)
    sala = SalaGuarita(fila)

    dados_6a = _dados_padrao()
    est_6a = iniciar_estado_fase_1(dados_6a, fila=fila)
    est_6a["estado_atual"] = "fim_turno"
    dados_6a["acertos"], dados_6a["erros"] = 6, 0

    dados_6e = _dados_padrao()
    est_6e = iniciar_estado_fase_1(dados_6e, fila=fila)
    est_6e["estado_atual"] = "fim_turno"
    dados_6e["acertos"], dados_6e["erros"] = 0, 6

    renderizar_frame_fase(tela_a, est_6a, sala, (0, 0), 1000)
    renderizar_frame_fase(tela_b, est_6e, sala, (0, 0), 1000)
    assert pygame.image.tobytes(tela_a, "RGB") == pygame.image.tobytes(tela_b, "RGB")

    cartao_rect = sala.caixa_correio.cartao_id.get_rect(center=(LARGURA_TELA // 2, 232))
    for visitante in fila:
        dados_cartao = extrair_dados_cartao(visitante)
        for campo in obter_especificacoes_campos_cartao(dados_cartao, cartao_rect):
            fonte_c, linhas = ajustar_render_campo_cartao(
                campo["valor"], campo["largura_disponivel"]
            )
            for linha in linhas:
                assert campo["pos_x"] + fonte_c.size(linha)[0] <= campo["limite_direito"]
