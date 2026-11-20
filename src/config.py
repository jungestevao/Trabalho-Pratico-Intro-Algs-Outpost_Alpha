# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Outpost-Alpha"
FONTE_TITULO = ("assets/fontes/Asimovian/Asimovian-Regular.ttf", 50)
FONTE_MENU = ("assets/fontes/Asimovian/commando.ttf", 30)
FONTE_CARTAO = ("assets/fontes/VCR_OSD_MONO_1.001.ttf", 18)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212,212,212)

DADOS = "data/dados_jogador.txt"

# Caminho das musicas
MUSICA_MENU = "assets/sons/MainTheme.mp3"
MUSICA_HISTORIA = "assets/sons/HistoryReading.mp3"
MUSICA_FIM_FASE = "assets/sons/ShiftConclusion.mp3"

# Caminho FX
SOM_FUNDO = "assets/sons/Som_motor_ambiente_pixabay.mp3"
SOM_MONITOR = "assets/sons/Som-monitor-pixabay.mp3"

# Caminho dos sprites
SPRITE_BTN_DESATIVO = "assets/imagens/botao-sem-selecao.png"
SPRITE_BTN_ATIVO = "assets/imagens/botao-com-selecao.png"
SPRITE_LOGO_JOGO = "assets/imagens/outpost-alpha.png"
SPRITE_LOGO_ES = "assets/imagens/Logo_ES_negativo@4x-1.png"
SPRITE_LOGO_PUC = "assets/imagens/brasao-pucminas.png"
SPRITE_LOGO_G3 = "assets/imagens/logo-grupo-3.png"
SPRITE_FUNDO_MENU = "assets/imagens/imagem-fundo-menu.jpg"
SPRITE_FUNDO_JOGO = "assets/imagens/fundo-jogo.jpg"

# Caminhos dos sprites dos objetos do jogo
SPRITES_OBJETOS = "assets/imagens/objetos_jogo/sprits"
SPRITES_FLUXOS_TELA = f"{SPRITES_OBJETOS}/fluxos_tela"
SPRITES_AVATARES = f"{SPRITES_OBJETOS}/avatares"
SPRITES_MONITOR = f"{SPRITES_OBJETOS}/monitor"

# Monitor CRT e aplicativos
SPRITE_MONITOR_CRT_BASE = f"{SPRITES_MONITOR}/tela-crt-base.png"
SPRITE_ICONE_BPM_NORMAL = f"{SPRITES_MONITOR}/icone-bpm-normal.png"
SPRITE_ICONE_BPM_HOVER = f"{SPRITES_MONITOR}/icone-bpm-hover.png"
SPRITE_ICONE_TEMP_NORMAL = f"{SPRITES_MONITOR}/icone-temperatura-normal.png"
SPRITE_ICONE_TEMP_HOVER = f"{SPRITES_MONITOR}/icone-temperatura-hover.png"
SPRITE_ICONE_PESO_NORMAL = f"{SPRITES_MONITOR}/icone-peso-normal.png"
SPRITE_ICONE_PESO_HOVER = f"{SPRITES_MONITOR}/icone-peso-hover.png"
SPRITE_MONITOR_APP_BPM = f"{SPRITES_MONITOR}/tela-app-bpm.png"
SPRITE_MONITOR_APP_TEMP = f"{SPRITES_MONITOR}/tela-app-temperatura.png"
SPRITE_MONITOR_APP_PESO = f"{SPRITES_MONITOR}/tela-app-peso.png"

# Fluxos de tela
SPRITE_CAIXA_CORREIO_DESATIVADA = f"{SPRITES_FLUXOS_TELA}/Caixa-correio-desselecionada.png"
SPRITE_CAIXA_CORREIO_ATIVA = f"{SPRITES_FLUXOS_TELA}/Caixa-correio-selecionada.png"
SPRITE_BOTAO_SELECIONADO = f"{SPRITES_FLUXOS_TELA}/botao-selecionado.png"
SPRITE_BOTAO = f"{SPRITES_FLUXOS_TELA}/botao.png"
SPRITE_COMPUTADOR_SELECIONADO = f"{SPRITES_FLUXOS_TELA}/computador-selecionado.png"
SPRITE_COMPUTADOR = f"{SPRITES_FLUXOS_TELA}/computador.png"
SPRITE_MICROFONE_SELECIONADO = f"{SPRITES_FLUXOS_TELA}/microfone-selecionado.png"
SPRITE_MICROFONE = f"{SPRITES_FLUXOS_TELA}/microfone.png"
SPRITE_TELA_CHEIA_BOTAO = f"{SPRITES_FLUXOS_TELA}/tela-cheia-botao.jpeg"
SPRITE_TELA_CHEIA_VERDE_APERTADO = f"{SPRITES_FLUXOS_TELA}/tela-cheia-verde-apertado.jpeg"
SPRITE_TELA_CHEIA_VERMELHO_APERTADO = f"{SPRITES_FLUXOS_TELA}/tela-cheia-vermelho-apertado.jpeg"

# Avatares dos personagens
SPRITE_AVATAR_ARTUR_KOVIC = f"{SPRITES_AVATARES}/artur-kovic.png"
SPRITE_AVATAR_BEATRIZ_MOURA = f"{SPRITES_AVATARES}/beatriz-moura.png"
SPRITE_AVATAR_CAMILA_DUARTE = f"{SPRITES_AVATARES}/camila-duarte.png"
SPRITE_AVATAR_CAROLINHA_PEIXOTO = f"{SPRITES_AVATARES}/carolinha-peixoto.png"
SPRITE_AVATAR_CLARA_MENDES = f"{SPRITES_AVATARES}/clara-mendes.png"
SPRITE_AVATAR_DANIEL_KRAUSS = f"{SPRITES_AVATARES}/daniel-krauss.png"
SPRITE_AVATAR_DAVI_ALENCAR = f"{SPRITES_AVATARES}/davi-alencar.png"
SPRITE_AVATAR_ELENA_VANCE = f"{SPRITES_AVATARES}/elena-vance.png"
SPRITE_AVATAR_GABRIEL_TORRES = f"{SPRITES_AVATARES}/gabriel-torres.png"
SPRITE_AVATAR_HELENA_NOVAK = f"{SPRITES_AVATARES}/helena-novak.png"
SPRITE_AVATAR_ID_PERSONAGENS = f"{SPRITES_AVATARES}/id-personagens.png"
SPRITE_AVATAR_IGOR_PETROV = f"{SPRITES_AVATARES}/igor-petrov.png"
SPRITE_AVATAR_JONAS_RIBEIRO = f"{SPRITES_AVATARES}/jonas-ribeiro.png"
SPRITE_AVATAR_LAERTE_XAVIER = f"{SPRITES_AVATARES}/laerte-xavier.png"
SPRITE_AVATAR_LIVIA_TEXEIRA = f"{SPRITES_AVATARES}/livia-texeira.png"
SPRITE_AVATAR_LUCAS_FERRAZ = f"{SPRITES_AVATARES}/lucas-ferraz.png"
SPRITE_AVATAR_MARCOS_SILVAR = f"{SPRITES_AVATARES}/marcos-silvar.png"
SPRITE_AVATAR_MATEUS_VIANA = f"{SPRITES_AVATARES}/mateus-viana.png"
SPRITE_AVATAR_RENATO_BARROS = f"{SPRITES_AVATARES}/renato-barros.png"
SPRITE_AVATAR_SAMUEL_NOGUEIRA = f"{SPRITES_AVATARES}/samuel-nogueira.png"
SPRITE_AVATAR_SOFIA_COSTA = f"{SPRITES_AVATARES}/sofia-costa.png"
SPRITE_AVATAR_VALERIA_KLEIN = f"{SPRITES_AVATARES}/valeria-klein.png"

AVATARES_PERSONAGENS = {
    "Marcos Silva": SPRITE_AVATAR_MARCOS_SILVAR,
    "Elena Vance": SPRITE_AVATAR_ELENA_VANCE,
    "Jonas Ribeiro": SPRITE_AVATAR_JONAS_RIBEIRO,
    "Clara Mendes": SPRITE_AVATAR_CLARA_MENDES,
    "Artur Kovic": SPRITE_AVATAR_ARTUR_KOVIC,
    "Sofia Costa": SPRITE_AVATAR_SOFIA_COSTA,
    "Davi Alencar": SPRITE_AVATAR_DAVI_ALENCAR,
    "Beatriz Moura": SPRITE_AVATAR_BEATRIZ_MOURA,
    "Lucas Ferraz": SPRITE_AVATAR_LUCAS_FERRAZ,
    "Helena Novak": SPRITE_AVATAR_HELENA_NOVAK,
    "Gabriel Torres": SPRITE_AVATAR_GABRIEL_TORRES,
    "Valeria Klein": SPRITE_AVATAR_VALERIA_KLEIN,
    "Renato Barros": SPRITE_AVATAR_RENATO_BARROS,
    "Camila Duarte": SPRITE_AVATAR_CAMILA_DUARTE,
    "Mateus Viana": SPRITE_AVATAR_MATEUS_VIANA,
    "Igor Petrov": SPRITE_AVATAR_IGOR_PETROV,
    "Livia Teixeira": SPRITE_AVATAR_LIVIA_TEXEIRA,
    "Samuel Nogueira": SPRITE_AVATAR_SAMUEL_NOGUEIRA,
    "Carolina Peixoto": SPRITE_AVATAR_CAROLINHA_PEIXOTO,
    "Daniel Krauss": SPRITE_AVATAR_DANIEL_KRAUSS,
    "Laerte Xavier": SPRITE_AVATAR_LAERTE_XAVIER,
}
