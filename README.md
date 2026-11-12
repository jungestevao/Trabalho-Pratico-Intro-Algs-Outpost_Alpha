# Outpost Alpha-04

<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/15be7931-0144-4a48-ac8b-0ce10aef2a40" />

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Estêvão de Castro Jung
- Fernando Pereira de Vasconcelos

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

> Outpost Alpha-04 é um thriller psicológico de triagem em que você julga, às cegas, quem entra na última Cidade-Refúgio da humanidade e quem morre no incinerador.

> No passado, humanos criaram "Réplicas" (IAs em corpos biológicos) para substituir parentes mortos. Após um surto coletivo no código dessas máquinas, o mundo colapsou. O grande terror do jogo é a evolução destas IAs: elas aprenderam a emular a miséria humana. 
> Elas gravam áudios de choro real, quantizam o gaguejar do medo e forçam falhas em seus motores para simular tremores de frio. O desespero virou uma tática matemática de infiltração.

> Trancado em uma guarita de chumbo sem contato visual, você usa apenas o áudio, um termostato e o cruzamento de diálogos para diferenciar um humano traumatizado de uma rede neural atuando perfeitamente. Apenas após tomar sua decisão (salvar ou incinerar), a parede se ergue por 2 segundos, revelando se você descartou um robô ou assassinou um humano inocente.

> No clímax, a crítica final sobre a nossa terceirização da dor: o jogador descobre que ele próprio é uma Inteligência Artificial, colocada na guarita porque a humanidade era empática demais para fazer o próprio trabalho sujo.

## Objetivo do jogador

> Objetivo Principal (A Missão): Filtrar os indivíduos na Guarita Alpha-04, garantindo que apenas humanos reais entrem na Cidade-Refúgio (Botão Verde) e que todas as Réplicas de Luto sejam descartadas no incinerador (Botão Vermelho).
> Objetivo Mecânico (A Investigação): Usar as ferramentas do terminal (osciloscópio de frequência de voz, controle térmico da cabine e cruzamento de falas) para forçar o visitante ao erro e identificar se o sofrimento apresentado é genuíno ou uma emulação calculada por uma rede neural.
> Condição de Vitória / Sobrevivência: Cumprir a cota diária de triagens mantendo a margem de erro abaixo do limite tolerado. Deixar uma Réplica infiltrar-se na cidade causa mortes lá dentro; executar humanos reais por engano gera penalidades severas e aproxima o Inspetor do seu próprio "descarte" por falha de protocolo.
> Conflito Interno (Meta-objetivo): Manter a precisão fria e analítica mesmo após os choques visuais de dois segundos a cada fim de turno, sem deixar que a evolução do comportamento das máquinas — ou o peso de ter condenado um inocente no turno anterior — comprometa o julgamento do próximo da fila.

## Regras do jogo

- Interação com o Terminal: O jogador controla os equipamentos da guarita (osciloscópio, controle térmico e cruzamento de dados) usando o mouse para encontrar inconsistências no áudio ou no depoimento do visitante.

- Tomada de Decisão: Para encerrar um turno, o jogador deve obrigatoriamente apertar um dos dois botões: o Verde (libera a entrada para a Cidade-Refúgio) ou o Vermelho (aciona o alçapão do incinerador).

- A Revelação (Consequência Visual): Imediatamente após a escolha, a placa de chumbo se abre por exatos 2 segundos, revelando se o jogador acertou (salvou um humano/destruiu uma máquina) ou errou (matou um humano/salvou uma máquina), sem possibilidade de reverter a ação.

- Evolução da Ameaça: A cada novo dia no jogo (ou turno), as Réplicas aprimoram suas táticas, copiando os padrões, forçando o jogador a ser mais crítico.

- Margem de Erro (Sistema de Vida): Errar um julgamento (incinerar um humano ou aprovar uma IA) aumenta a quantidade de "Falha de Protocolo" do Inspetor.

- Condição de Derrota / Fim de Jogo: A partida termina (Game Over) se a Margem de Erro atingir o limite máximo, resultando no "descarte" do próprio jogador pelo sistema da Cidade-Refúgio.

- Condição de Vitória: Sobreviver até o final da campanha completando as cotas diárias de triagem, o que culminará na revelação final de que o próprio Inspetor é uma Inteligência Artificial.

## Controles

- Mouse (Botão Esquerdo): Interagir com os botões físicos da mesa (incluindo os botões Verde e Vermelho de decisão), ligar/desligar painéis e selecionar trechos de texto na tela.

- Mouse (Scroll / Roda do Mouse): Rolar para cima e para baixo o histórico da transcrição de áudio no monitor para reler depoimentos antigos.

- Barra de Espaço: Acelerar o preenchimento de texto no terminal (pular a animação de máquina de escrever) para agilizar o interrogatório.

- ESC: Abrir o menu do sistema (Pausar / Configurações / Sair do jogo).

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
