# Passaí - Apoio à acessibilidade nas travessias

## Introdução

O **Passaí** é uma aplicação de terminal desenvolvida em Python para ajudar a organizar dificuldades encontradas por pedestres em travessias urbanas.

O sistema permite registrar situações como tempo insuficiente no semáforo, rampas ausentes ou bloqueadas, obstáculos no caminho e dificuldade para perceber a sinalização. A partir dessas informações, o programa cria um texto organizado de solicitação de melhoria e permite registrar o envio e a resposta recebida.

O Passaí representa a parte de **Computational Thinking with Python** do projeto **Travessia**, desenvolvido para a Global Solution CitizenTech. Seu papel é processar dados, aplicar regras simples de decisão e conservar as informações em um arquivo JSON.

## Visão geral

| Item | Descrição |
|---|---|
| Projeto integrado | Travessia |
| Aplicação em Python | Passaí |
| Tema | Acessibilidade e segurança nas travessias de pedestres |
| Problema | Dificuldades ficam dispersas e nem sempre são transformadas em pedidos claros de avaliação. |
| Solução | Registrar dificuldades, organizá-las por local, gerar um pedido e acompanhar o retorno. |
| Usuários | Comunidades, coletivos, associações ou equipes que organizam informações sobre travessias. |
| Público beneficiado | Pedestres, especialmente idosos e pessoas com mobilidade reduzida. |
| Armazenamento | Arquivo local `dados.json`. |

## Problema e objetivo

Uma pessoa pode não conseguir terminar a travessia antes de o sinal fechar, encontrar uma rampa bloqueada ou ter dificuldade para perceber a sinalização. Mesmo quando essas situações são relatadas, as informações podem ficar espalhadas e sem acompanhamento.

O objetivo do Passaí é facilitar essa organização. Em vez de exigir termos técnicos, o programa apresenta escolhas em linguagem simples, reúne os registros de um mesmo local e gera um pedido solicitando a avaliação dos pontos informados.

O programa não substitui uma vistoria profissional e não declara que uma travessia está irregular. Ele organiza relatos e produz pedidos de avaliação que podem ser encaminhados pelo próprio usuário.

## Como o sistema funciona

O fluxo principal possui quatro etapas:

1. **Registrar:** a pessoa informa o local e a dificuldade encontrada.
2. **Organizar:** o sistema agrupa as dificuldades cadastradas por local.
3. **Gerar o pedido:** o programa transforma as informações em um texto organizado.
4. **Acompanhar:** a pessoa registra o envio, o protocolo, a resposta e o encerramento.

O envio não é realizado automaticamente. O texto é exibido no terminal para que o usuário possa copiá-lo e encaminhá-lo pelo canal de atendimento escolhido.

## Funcionalidades

```text
1. Registrar uma dificuldade
2. Ver dificuldades cadastradas
3. Alterar uma dificuldade
4. Excluir uma dificuldade
5. Criar um pedido de melhoria
6. Registrar envio ou resposta
7. Ver painel geral e pendências
8. Excluir todos os dados e reiniciar
0. Sair
```

| Opção | O que faz |
|---|---|
| 1 | Cadastra uma dificuldade, o local, a frequência, os detalhes e a origem da informação. |
| 2 | Mostra todas as dificuldades cadastradas. |
| 3 | Permite corrigir dificuldade, frequência, detalhes, origem ou local. |
| 4 | Exclui uma dificuldade após confirmação. |
| 5 | Reúne as dificuldades de um local e cria o texto do pedido de melhoria. |
| 6 | Conduz o pedido pelas etapas de envio, resposta recebida e encerramento. |
| 7 | Apresenta as quantidades cadastradas e as próximas ações de cada local. |
| 8 | Apaga todos os registros após confirmação e reinicia o sistema. |
| 0 | Encerra o programa. |

Nos submenus e campos de texto, o número `0` cancela a operação atual. Confirmações utilizam `s` ou `n`. Campos opcionais podem ser ignorados pressionando Enter.

## Dificuldades registradas

O usuário pode selecionar uma das seguintes situações:

- O sinal fechou antes de a travessia terminar.
- A rampa estava ausente ou bloqueada.
- A calçada ou a faixa tinha obstáculos.
- Houve dificuldade para perceber a sinalização.
- Outra dificuldade, descrita pelo usuário.

Também são registradas a frequência, informações adicionais e a origem do dado. A origem pode ser um relato informado, uma fonte pública ou um exemplo fictício utilizado na demonstração acadêmica.

## Como o pedido é criado

Cada dificuldade está relacionada a um ponto de avaliação:

| Dificuldade informada | Avaliação incluída no pedido |
|---|---|
| Sinal fechou antes da conclusão | Avaliação do tempo destinado à travessia. |
| Rampa ausente ou bloqueada | Avaliação das condições de acesso à faixa. |
| Obstáculos na calçada ou faixa | Avaliação das condições de acesso e dos obstáculos. |
| Dificuldade com a sinalização | Avaliação da sinalização e de sua acessibilidade. |
| Outra dificuldade | Avaliação da situação descrita pelo usuário. |

Essas regras apenas organizam o pedido. Elas não calculam risco, não verificam o local e não produzem um laudo técnico.

O pedido segue este fluxo:

```text
Preparada -> Encaminhada -> Resposta recebida -> Encerrada
```

- **Preparada:** o texto foi criado e está pronto para copiar.
- **Encaminhada:** o usuário informou que realizou o envio.
- **Resposta recebida:** o retorno foi registrado no sistema.
- **Encerrada:** não existem outras ações de acompanhamento naquele pedido.

## Como executar

### Requisito

Python 3.10 ou superior, devido ao uso de `match/case`.

O projeto utiliza apenas `json` e `pathlib`, que fazem parte da biblioteca padrão do Python. Não é necessário instalar pacotes externos, utilizar banco de dados ou ter conexão com a internet.

### Execução

1. Abra o terminal na pasta do projeto.
2. Execute:

```console
python passai.py
```

No Windows, também pode ser utilizado:

```console
py passai.py
```

## Arquivos do projeto

```text
Passai-python/
├── passai.py
├── dados.json
├── readme.md
└── prompts.md
```

- `passai.py`: contém todo o código da aplicação.
- `dados.json`: guarda os locais, dificuldades, pedidos e históricos.
- `readme.md`: apresenta e explica o projeto.
- `prompts.md`: documenta como a Inteligência Artificial foi utilizada durante o desenvolvimento.

## Uso de Inteligência Artificial

A equipe utilizou o Codex, da OpenAI, como ferramenta de apoio para organizar ideias, revisar o código, sugerir melhorias, gerar cenários de teste e auxiliar na documentação.

As sugestões foram analisadas, testadas e ajustadas pela equipe antes de serem incorporadas. Os prompts utilizados, as funcionalidades que receberam auxílio, o processo de verificação e uma análise crítica estão documentados em `prompts.md`.

## Salvamento dos dados

O arquivo `dados.json` permite continuar o trabalho depois que o programa é fechado. São armazenados:

- Locais cadastrados.
- Dificuldades e suas informações.
- Pedidos gerados.
- Protocolos e situações atuais.
- Histórico de cada pedido.
- Contadores utilizados para criar identificadores únicos.

Se `dados.json` não existir ou estiver vazio, o Passaí começa normalmente sem nenhum cadastro. O arquivo recebe a estrutura necessária quando a primeira alteração é confirmada.

Antes de salvar, o programa verifica se os campos, identificadores e relações entre os registros são válidos. A gravação utiliza primeiro um arquivo temporário e somente depois substitui o JSON principal. Isso reduz o risco de perder os dados caso ocorra uma falha durante a escrita.

## Perguntas sobre o sistema

### Como os dados são carregados e salvos?

Ao iniciar, o programa lê `dados.json` e transforma seu conteúdo em listas e dicionários do Python. Sempre que uma alteração é confirmada, os dados atualizados são gravados novamente no arquivo.

### Por que existe um arquivo temporário na gravação?

O programa primeiro grava tudo em `dados.json.tmp`. Somente quando essa gravação termina corretamente, o temporário substitui o arquivo principal. Assim, uma falha no meio do processo não destrói os dados que já estavam salvos.

### Como os identificadores são criados?

Locais, dificuldades e pedidos recebem números únicos. O JSON guarda qual será o próximo número de cada tipo. Depois de um cadastro, esse contador aumenta para evitar identificadores repetidos.

### Como funciona o histórico dos pedidos?

Cada mudança acrescenta um novo registro ao histórico. Dessa forma, o sistema conserva a sequência: pedido preparado, enviado, respondido e encerrado.

### Por que o pedido guarda uma cópia das dificuldades?

A cópia registra exatamente quais informações foram utilizadas na criação do pedido. Se uma dificuldade for alterada ou excluída depois, o texto que já foi encaminhado continua preservado.

### Como a opção 8 reinicia o sistema?

Ela mostra quantos dados serão apagados e pede confirmação. Depois, grava uma estrutura JSON nova e vazia. A memória do programa só é limpa se essa gravação funcionar corretamente.

### Como as regras transformam dificuldades em pedidos?

Cada tipo de dificuldade possui uma sugestão de avaliação. Por exemplo, um relato sobre o sinal fechar cedo gera um pedido para avaliar o tempo da travessia. O sistema organiza a solicitação, mas não afirma que existe uma irregularidade.

### O que acontece se o JSON estiver incorreto?

O programa informa que não conseguiu abrir os dados e preserva o arquivo. Ele não substitui automaticamente um conteúdo inválido, evitando apagar informações que possam ser recuperadas.

### Por que o projeto usa JSON em vez de banco de dados?

O JSON atende ao requisito da disciplina e é suficiente para uma aplicação local de terminal. Ele permite demonstrar leitura, gravação e manipulação de dados sem depender de serviços externos.

## Conceitos de Python utilizados

| Requisito da disciplina | Aplicação no Passaí |
|---|---|
| Menu de opções | Menu principal e submenus numerados. |
| Validação de entradas | Verificação de números, textos obrigatórios e confirmações. |
| `try/except` | Tratamento de opções inválidas e problemas na leitura ou gravação. |
| `if/elif/else` | Decisões sobre cadastros, pendências e situações dos pedidos. |
| `match/case` | Encaminhamento das opções do menu e outros fluxos com várias escolhas. |
| `while` | Repetição do menu e de perguntas até receber uma entrada válida. |
| `for` | Percurso de locais, dificuldades, pedidos e históricos. |
| Funções | Separação das responsabilidades e reaproveitamento da lógica. |
| Listas | Coleções de locais, dificuldades, pedidos e eventos históricos. |
| Tuplas | Opções fixas apresentadas ao usuário. |
| Dicionários | Representação dos registros e das regras de análise. |
| JSON | Persistência dos dados entre as execuções. |

## Cuidados com as informações

O Passaí não acessa mapas, não verifica fontes públicas automaticamente e não envia pedidos para órgãos externos. As informações são registradas conforme foram fornecidas pelo usuário.

Para demonstrações acadêmicas, recomenda-se utilizar dados fictícios ou públicos e evitar dados pessoais. Exemplos fictícios são identificados no texto para que não sejam confundidos com relatos reais.

## Roteiro curto de demonstração

1. Inicie o programa e informe um nome.
2. Cadastre uma dificuldade fictícia na opção 1.
3. Consulte o cadastro na opção 2.
4. Crie o pedido de melhoria na opção 5.
5. Consulte o painel na opção 7.
6. Feche e abra o programa para mostrar que os dados continuam salvos.

## Integrantes

| Nome completo | RM |
|---|---|
| Rafael Taboada Sobral | 569527 |
| Fabricio Denig De Avila | 570980 |
| Beatriz Perigo | 569654 |
