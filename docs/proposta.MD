# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na etapa inicial do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com **Python e Pygame** dentro do prazo disponível. Consulte o enunciado publicado no Canvas para conhecer o eixo temático e as orientações vigentes.

## 1. Nome provisório do jogo

**Nome:**

> Outpost_Alpha

## 2. Integrantes do grupo

- Nome 1: Estevão de Castro Jung
- Nome 2: Fernando Pereira de Vasconcellos

## 3. Tema escolhido

**Tema:**

> Conteúdos reais e artificiais (reconhecimento de sinais gerados por IA): Este é o pilar da jogabilidade (core loop). O jogador atua constantemente tentando identificar se os sinais de sofrimento, voz e temperatura do visitante são genuinamente humanos ou emulações sintéticas geradas pelas "Réplicas".

> Vieses e justiça nas decisões (efeitos em sistemas automatizados): Abordado no peso moral e no plot twist do jogo, que critica a delegação de escolhas éticas (quem vive ou morre) a sistemas cegos ou, em última instância, à própria inteligência artificial, removendo a empatia do processo de triagem.

> Confiabilidade de sistemas inteligentes (erros e limites das respostas): Representado pela margem de erro da triagem e pela revelação visual pós-decisão (a consequência de confiar apenas em dados de um terminal sem verificação humana completa).

## 4. Tipo de jogo

**Tipo escolhido:**

> Puzzle de Dedução e Triagem (com elementos de sobrevivência simples e análise de informações, focado em cruzamento de dados e tomada de decisão lógica).

## 5. Descrição geral do jogo

**Descrição:**

> O jogo se passa inteiramente na interface de um terminal de triagem (estilo point-and-click). Na tela, o jogador vê um monitor CRT antigo, um painel com botões e ferramentas, e um vidro de guarita bloqueado por uma espessa chapa de chumbo. Utilizando o mouse, o jogador controla o cruzamento de diálogos em texto, análises de áudio em um osciloscópio e alterações no ambiente da cabine externa (como abaixar a temperatura). O objetivo é interrogar os indivíduos no escuro e decidir se são humanos (pressionando o botão Verde para liberar a entrada) ou IAs disfarçadas (pressionando o Vermelho para incinerar). O principal desafio é usar a dedução lógica e a análise sensorial para não se deixar enganar pelas máquinas que emulam sentimentos e dor humana com perfeição, mantendo a cota de acertos alta para não sofrer Game Over, além de lidar com o peso psicológico de ver a consequência da sua escolha por rápidos dois segundos após a placa de chumbo se abrir.

## 6. Objetivo do jogador

**Objetivo:**

> Sobreviver aos turnos de trabalho na guarita realizando a triagem correta dos visitantes. O jogador deve utilizar dedução lógica e as ferramentas do terminal para descobrir quem é humano (liberando a entrada) e quem é máquina (acionando o incinerador), precisando cumprir as cotas diárias e manter a margem de erro baixa o suficiente para não ser eliminado pelo sistema.

## 7. Regras principais

Liste até cinco regras que expliquem o funcionamento do jogo. Exemplos: o jogador começa com três vidas; acertos somam pontos; colisões retiram vidas.

- Regra 1: O interrogatório ocorre totalmente às cegas; o jogador deve basear sua análise exclusivamente nas ferramentas do terminal (áudio, termostato e cruzamento de textos).
- Regra 2: Cada turno só pode ser encerrado quando o jogador toma a decisão binária e irreversível: botão Verde (liberar entrada) ou botão Vermelho (incinerar).
- Regra 3: Julgamentos incorretos (matar um humano ou salvar uma máquina) não podem ser desfeitos e aumentam a barra de "Margem de Erro" do Inspetor.
- Regra 4: O jogo termina (Game Over) se o jogador acumular falhas suficientes para estourar o limite da Margem de Erro até o fim dos 3 deias, resultando no seu próprio "descarte".
- Regra 5: A cada dia/turno será liberado uma nova forma de verificação para o jogador.

## 8. Condição de vitória

**Condição de vitória:**

> Sobreviver a todos os turnos de triagem da campanha sem deixar que a barra de margem de erro atinja o limite máximo. Ao concluir o último dia de trabalho com sucesso, o jogador finaliza a história e alcança a revelação narrativa final (o plot twist de que o próprio Inspetor é uma IA).

## 9. Condição de derrota ou encerramento

> A partida termina em derrota (Game Over) se o jogador atingir o limite máximo de erros de julgamento na triagem (incinerando humanos inocentes ou permitindo a entrada de máquinas). Ao esgotar a tolerância da "Margem de Erro", o sistema considera o Inspetor defeituoso e ele próprio é descartado pela Cidade-Refúgio, encerrando a campanha prematuramente.

## 10. Elementos previstos no jogo

Descreva brevemente os elementos mais importantes, sem precisar detalhar a implementação.

- Personagem ou elemento principal: O protagonista (o Inspetor da Guarita Alpha-04) e a própria interface do terminal retro-futurista (monitor CRT de fósforo), através da qual todas as ações do jogo acontecem.

- Obstáculos ou desafios: As "Réplicas", IAs que aprenderam a emular emoções, choro e falhas biológicas humanas com perfeição. O grande desafio é o julgamento lógico sob pressão psicológica, sem a ajuda da visão.

- Itens ou objetos de interação (se houver): As ferramentas da mesa de controle: o osciloscópio de frequência de voz, o termostato (para alterar a temperatura da cabine externa), os relatórios de transcrição para cruzamento de falas e os dois botões físicos (Verde para aprovar, Vermelho para descartar).

- Pontuação, vidas, tempo ou progresso: O progresso avança ao completar a cota de triagens de cada dia/turno de trabalho. As "vidas" são representadas por um medidor de "Margem de Erro" (ou Nível de Falha do Protocolo), que pune o jogador a cada decisão equivocada.

## 11. Controles previstos

**Controles:**

> Mouse (Botão Esquerdo): Interagir com a interface, como apertar os botões físicos da mesa (Verde e Vermelho) e selecionar opções no monitor.

> Mouse (Scroll): Rolar o histórico de diálogos no monitor para cima ou para baixo.

> Teclado (Espaço): Acelerar a exibição do texto na tela (pular a animação de digitação).

> Teclado (ESC): Pausar o jogo e abrir o menu do sistema.

## 12. Principais dificuldades esperadas

Cite até três dificuldades que o grupo espera enfrentar. Exemplos: movimentação, colisões, controle de tempo, testes ou uso do GitHub.

- Dificuldade 1: Sincronia e manipulação complexa de áudio. Como o jogo se baseia em interrogatórios às cegas, criar a lógica para sincronizar perfeitamente as faixas de áudio (vozes, ruídos de fundo e efeitos do osciloscópio) com os eventos visuais na tela exigirá um controle preciso do pygame.mixer, que pode ser limitado para manipulações dinâmicas.

- Dificuldade 2: O Pygame não possui elementos nativos de interface (como botões clicáveis, barras de rolagem ou caixas de texto selecionáveis). Construir a mecânica de point-and-click, como arrastar blocos de texto para cruzar dados e interagir com o termostato, exigirá a criação de um sistema de colisão e gerenciamento de estados bem robusto.

- Dificuldade 3: Resolução de conflitos de código no GitHub e gerenciamento de arquivos pesados (como áudios e texturas) durante o trabalho colaborativo da equipe.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

> A versão inicial (MVP) focará apenas no ciclo principal de triagem de forma simplificada, garantindo que o jogo tenha começo, meio e fim. A tela exibirá a interface do terminal com o texto do depoimento do visitante aparecendo gradativamente (efeito máquina de escrever) e dois botões clicáveis (Verde/Aprovar e Vermelho/Incinerar).

> Para evitar complexidade técnica inicial, ferramentas avançadas como o termostato e o cruzamento de textos não estarão presentes. O jogador fará a dedução apenas lendo as respostas e ouvindo um áudio básico. Ao clicar em um botão, atualizará a variável da "Margem de Erro" e chamará o próximo visitante. A partida será composta por uma fila curta pré-programada (ex: 5 indivíduos) e terminará na tela de Vitória ou de Game Over, dependendo da quantidade de erros.

## 14. Possíveis melhorias, caso haja tempo


- Melhoria 1: Mecânicas Avançadas de Triagem: Incluir o termostato interativo da cabine externa (obrigando o jogador a testar reações de frio nas IAs) e o sistema de selecionar e cruzar trechos de texto na tela para detectar contradições lógicas no depoimento.
- Melhoria 2: Adicionar filtros visuais via código para simular a tela de tubo antiga (como scanlines, leve cintilação e brilho de fósforo) e animar a subida e descida da placa de chumbo no fim do turno, substituindo as imagens estáticas do escopo mínimo.
