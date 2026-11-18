# Passaí — Apoio à acessibilidade nas travessias

O Passaí é um assistente de terminal que transforma dificuldades relatadas em travessias de pedestres em pedidos de avaliação organizados e acompanháveis. Ele reúne informações por local, identifica quais aspectos devem aparecer na solicitação e ajuda a acompanhar o encaminhamento e o retorno.

Este programa representa a parte de **Computational Thinking with Python** do projeto **Travessia**, desenvolvido para a Global Solution CitizenTech. O Travessia contempla análise cidadã e um protótipo semafórico experimental; o Passaí concentra o trabalho em Python na organização e interpretação dos relatos.

## Ficha da CitizenTech

| Item | Descrição |
|---|---|
| Projeto integrado | Travessia |
| Aplicação Python | Passaí — Apoio à acessibilidade nas travessias |
| Território de referência | São Paulo, com recorte inicial de estudo em Santana, Zona Norte. O programa permite cadastrar outros locais. |
| Cidadão beneficiado | Pedestres, especialmente idosos e pessoas com mobilidade reduzida, que enfrentam dificuldades nas travessias. |
| Usuário do terminal | Pessoa de um coletivo, associação, equipe de pesquisa ou comunidade que organiza informações sobre os locais. |
| Problema em uma frase | Dificuldades de travessia ficam dispersas em relatos, sem uma descrição organizada do que precisa ser avaliado e sem acompanhamento dos encaminhamentos. |
| Como funciona | Registrar dificuldade → reunir relatos do local → sugerir pontos de avaliação → preparar solicitação → acompanhar retorno. |
| Papel do Python | Processar relatos, aplicar regras de análise, organizar pendências e conservar os dados. |
| Indicador inicial | Quantidades de solicitações preparadas, encaminhadas, respondidas e encerradas, separadas dos exemplos fictícios. |
| ODS relacionados | ODS 11 — Cidades e comunidades sustentáveis; ODS 10 — Redução das desigualdades. |
| Repositório | Preencher com o endereço do repositório da equipe. |

O vínculo com o ODS 11 está no apoio à identificação de barreiras de mobilidade e acesso aos espaços urbanos. A contribuição pretendida ao ODS 10 está em facilitar a participação e a expressão de necessidades de pessoas que encontram barreiras de acesso à cidade. Essas são contribuições esperadas do projeto, não impactos já comprovados.

## Por que o projeto existe

Uma pessoa pode ter dificuldade para concluir a travessia antes de o sinal fechar, perceber a sinalização ou chegar até a faixa por uma rampa. Entretanto, transformar essa experiência em uma solicitação compreensível exige organizar o local, explicar a dificuldade e guardar o andamento do atendimento.

O Passaí apoia esse processo. A pessoa não precisa informar largura da rua, velocidade de deslocamento, tempo semafórico ou termos técnicos. Ela escolhe opções em linguagem comum, informa uma referência do local e pode acrescentar detalhes.

O benefício imediato é tornar as informações consultáveis e produzir um pedido coerente com as dificuldades relatadas. A melhoria física de uma travessia depende de avaliação e atuação externa. O programa, sozinho, não modifica a rua nem comprova que um problema foi resolvido.

## O que o Passaí faz

- Registra dificuldades com opções numeradas e orientações somente nos campos que podem gerar dúvida.
- Reutiliza locais cadastrados para reduzir digitação e agrupar relatos.
- Distingue relatos informados, fontes públicas e exemplos fictícios.
- Permite consultar, corrigir e excluir relatos, além de completar a referência do local.
- Reúne os relatos de um local e sugere quais avaliações incluir no pedido.
- Salva uma solicitação preparada, mantendo o texto que foi produzido.
- Registra protocolo, situação e histórico do acompanhamento.
- Mostra pendências e próximos passos por local.
- Salva os dados em JSON para continuar o trabalho após fechar o programa.

## Como executar

**Requisito:** Python 3.10 ou superior, devido ao uso de `match/case`.

O projeto utiliza apenas `json` e `pathlib`, da biblioteca padrão. Não é necessário instalar pacotes com `pip`, configurar banco de dados ou ter internet para usar o programa.

1. Abra um terminal na pasta que contém `passai.py`.
2. Execute:

```console
python passai.py
```

No Windows, se o launcher estiver disponível, também é possível executar:

```console
py passai.py
```

Para conferir a versão instalada:

```console
python --version
```

O arquivo `dados.json` sempre é procurado na mesma pasta de `passai.py`, independentemente da pasta em que o terminal foi aberto. Se o arquivo não existir, estiver vazio ou contiver apenas espaços, o programa inicia normalmente sem cadastros. Na primeira alteração confirmada, o arquivo é criado ou preenchido automaticamente com a estrutura JSON necessária.

## Arquivos do projeto

```text
Passai-python/
├── passai.py
├── dados.json
├── readme.md
├── prompt.md
└── prompts.md
```

Todo o código está em `passai.py`, organizado em funções. `dados.json` contém os registros. Os Markdown descrevem o projeto e documentam o uso de IA.

Os nomes `prompt.md` e `prompts.md` aparecem em páginas diferentes do enunciado. Foram mantidos os dois, com conteúdo idêntico. Qualquer atualização nesse registro deve ser replicada nos dois arquivos.

## Menu e navegação

Ao iniciar, o Passaí pede o nome da pessoa e mostra uma saudação antes do menu. O nome serve somente para personalizar a execução atual: ele não é gravado no JSON e não é associado aos relatos.

O nome é solicitado diretamente, sem um exemplo desnecessário. Digitar `0` nessa etapa encerra o programa antes de carregar o menu.

```text
PASSAÍ — APOIO À ACESSIBILIDADE NAS TRAVESSIAS

1. Registrar uma dificuldade
2. Ver dificuldades cadastradas
3. Alterar uma dificuldade
4. Excluir uma dificuldade
5. Analisar um local e preparar solicitação
6. Atualizar acompanhamento de solicitação
7. Ver painel geral e pendências
0. Sair
```

Digite o número da **opção exibida**, que pode ser diferente do identificador interno de um relato ou solicitação. Os menus não repetem exemplos como “digite 1”; basta escolher um dos números apresentados.

Nos submenus, `0` volta; no menu principal, encerra. Em todos os campos de texto, `0` também cancela a operação atual e retorna. Campos opcionais aceitam Enter. Quando um valor atual é apresentado, Enter o mantém; `-` apaga um campo opcional. Confirmações usam `s` ou `n`. Exemplos aparecem somente em entradas como endereço, fonte e protocolo, nas quais ajudam a esclarecer o formato esperado. Ctrl+C encerra o programa e preserva o que já foi salvo.

Linhas horizontais separam os títulos, opções e mensagens para facilitar a leitura no terminal. A apresentação utiliza apenas `print`, sem bibliotecas visuais externas.

### 1. Registrar uma dificuldade

O usuário escolhe o que aconteceu:

- O sinal fechou antes de terminar a travessia.
- A rampa estava ausente ou bloqueada.
- A calçada ou a faixa tinha obstáculos.
- Houve dificuldade para perceber a sinalização.
- Outra dificuldade.

Depois, seleciona um local já cadastrado ou informa outro. Um exemplo apresentado pelo programa é: “Rua Exemplo, em frente ao mercado, perto do número 100, Santana”.

A frequência é selecionada entre “Uma vez”, “Mais de uma vez” e “Não sei informar”. Os detalhes são opcionais, exceto para “Outra dificuldade”, que precisa de descrição.

Por último, o usuário indica a origem do registro. Uma fonte pública exige referência. O programa mostra as informações antes da confirmação. Cancelar não deixa um local ou relato salvo pela metade.

### 2. Ver dificuldades cadastradas

Mostra todas as dificuldades atuais em uma única lista, sem exigir que a pessoa entre primeiro em um local. Cada item apresenta número do relato, local, dificuldade, frequência, origem e detalhes.

Essa opção é somente para consulta. Alteração e exclusão possuem opções próprias no menu principal.

### 3. Alterar uma dificuldade

Mostra diretamente a lista de dificuldades cadastradas. Depois de selecionar uma, a pessoa escolhe qual informação deseja alterar: dificuldade, frequência, detalhes, origem dos dados ou local.

Locais com diferenças apenas de maiúsculas/minúsculas e espaços são reaproveitados. Descrições diferentes do mesmo endereço não são unificadas automaticamente. Para corrigir esse caso, mova o relato para o local correto.

### 4. Excluir uma dificuldade

Mostra diretamente a lista de dificuldades e pede confirmação antes da exclusão. Solicitações já preparadas conservam a cópia histórica do relato utilizado; somente a lista atual é alterada.

### 5. Analisar um local e preparar solicitação

Quando existe apenas um local, ele é selecionado automaticamente. Com vários locais, o programa apresenta uma lista simples para escolha.

O programa reúne os relatos atuais do local, conta os tipos de dificuldade e aplica as regras de análise. Se faltar confirmação da referência ou identificação da origem de um registro migrado, ele mostra o que deve ser completado. A confirmação da referência é humana: o programa não verifica endereços em mapas.

Quando as informações estão prontas, apresenta uma prévia da solicitação. Ao confirmar, salva o pedido com situação **Preparada**. O texto pode ser selecionado e copiado do terminal. Não é gerado um arquivo adicional de relatório.

Se já existir um rascunho para aquele local, a análise atualiza esse rascunho após confirmação. Se nada mudou, apenas informa que o conteúdo já foi preparado. Um pedido encaminhado ou respondido conserva o texto original e deve ser consultado pela opção 6.

### 6. Atualizar acompanhamento de solicitação

Apresenta o texto salvo e o histórico da solicitação. As ações disponíveis dependem da situação atual:

| Situação atual | Ações disponíveis |
|---|---|
| Preparada | Registrar encaminhamento, encerrar ou adicionar observação. |
| Encaminhada | Registrar resposta, encerrar ou adicionar observação. |
| Resposta recebida | Encerrar ou adicionar observação. |
| Encerrada | Consultar o texto e o histórico. Um novo pedido pode ser preparado na opção 5. |

Ao registrar encaminhamento de dados informados/documentais, o programa pergunta se o próprio usuário já fez o envio. O protocolo é opcional, pois pode não ter sido fornecido. Uma observação pode explicar o retorno ou o próximo passo. Para encerrar, a observação é obrigatória.

Receber uma resposta não encerra automaticamente o acompanhamento. Encerrar não significa que a travessia foi corrigida.

Há, no máximo, uma solicitação ativa por local. Esse limite ajuda a manter um acompanhamento claro. Novos relatos podem ser registrados enquanto o pedido está em andamento; o programa avisa quando o conteúdo atual difere do pedido anterior. Para um novo pedido, encerre o acompanhamento anterior com justificativa e prepare outro.

### 7. Ver painel geral e pendências

Reúne em uma única tela o resumo geral e as próximas ações. O painel apresenta quantidades de locais, relatos e solicitações; agrupamentos por dificuldade, origem e situação; e a pendência de cada local.

| Categoria | Significado |
|---|---|
| Informações a completar | Falta confirmar a referência do local ou identificar a origem de registros antigos. |
| Pedido a preparar | Há informações disponíveis e ainda não há solicitação ativa. |
| Revisar rascunho | Os relatos/local mudaram desde a preparação, ou há informações pendentes. |
| Aguardando encaminhamento | O pedido está preparado e atualizado. |
| Aguardando resposta | O usuário registrou o encaminhamento. |
| Resposta a avaliar | Foi registrado retorno e o acompanhamento continua aberto. |
| Demonstração | O rascunho contém exemplo fictício e pode ser usado para testar o fluxo. |
| Acompanhamento encerrado | A última solicitação foi encerrada e os dados atuais não mudaram. |
| Sem relatos atuais | O local existe, mas não tem relatos atuais, por exemplo após uma exclusão. |

Os locais aparecem na ordem de cadastro. Essa ordem não indica perigo, gravidade ou prioridade técnica. As contagens servem para organização e demonstração; não representam pessoas distintas, risco técnico ou melhorias realizadas na cidade.

## Regras de análise e decisões do programa

As regras abaixo são escolhas do projeto, destinadas a organizar pedidos de avaliação. Não são critérios oficiais de engenharia de tráfego.

| Entrada | Resultado sugerido |
|---|---|
| Sinal fechou antes da conclusão | Avaliação do tempo destinado à travessia de pedestres. |
| Dificuldade para perceber sinalização | Avaliação da sinalização para pedestres e de sua acessibilidade. |
| Rampa ausente/bloqueada ou obstáculos | Avaliação das condições de acesso à faixa, incluindo rampas e obstáculos. |
| Outra dificuldade | Avaliação da dificuldade adicional descrita no relato. |

Uma mesma solicitação pode reunir vários pontos. Pedidos de avaliação iguais não são repetidos; os relatos individuais permanecem no texto, com suas origens, detalhes e frequências.

O programa não deduz um defeito técnico a partir de uma experiência. Por exemplo, “o sinal fechou antes de eu terminar” gera um pedido de avaliação do tempo, sem declarar que a duração é ilegal ou que o equipamento está com defeito.

## Origem e uso dos dados

| Origem | Como o programa trata |
|---|---|
| Relato informado | Informação fornecida pelo usuário, sem verificação técnica pelo programa. |
| Fonte pública | Registro acompanhado de uma referência escrita pelo usuário. A fonte não é acessada nem verificada automaticamente. |
| Exemplo fictício | Dados para demonstração e testes. A solicitação inteira recebe um aviso explícito de demonstração. |
| Não identificada | Usada somente ao importar relatos de versões antigas. Precisa ser corrigida antes de preparar um novo pedido. |

Se um pedido mistura registros fictícios com outros registros, todo o pedido é tratado como demonstração. É possível percorrer os estados de acompanhamento para apresentar o programa; a confirmação de envio explica que o encaminhamento é fictício. Isso não representa submissão a um órgão público.

Para a entrega acadêmica, utilize dados públicos ou fictícios e identifique suas origens, conforme o briefing. Não inclua dados pessoais reais. Os campos livres não possuem um filtro automático de dados pessoais: revise o conteúdo antes de compartilhar a base.

## Exemplo de demonstração completa

Este roteiro usa um local e informações fictícios. Ele não foi inserido como relato real no arquivo entregue.

1. Na opção 1, registre “O sinal fechou antes de eu terminar”, no local “Rua Exemplo, em frente ao mercado, Santana”. Escolha a frequência, deixe detalhes em branco se quiser e selecione **Exemplo fictício**.
2. Registre uma segunda dificuldade no mesmo local: “A rampa estava ausente ou bloqueada”. Reutilize o local na lista e marque novamente **Exemplo fictício**.
3. Na opção 5, analise o local. Complete/confirme a referência quando solicitado.
4. Confira que o pedido reúne avaliação do tempo e das condições de acesso à faixa, com o aviso de demonstração.
5. Confirme a preparação e consulte o painel na opção 7.
6. Na opção 6, registre o encaminhamento fictício para demonstrar o acompanhamento. Use um protocolo claramente fictício, como `TESTE-001`.
7. Registre uma resposta de demonstração e depois encerre com uma justificativa.
8. Feche e abra o programa. O texto e o histórico continuam disponíveis.

O resultado demonstrado é a organização do trabalho: dois relatos passam a compor um pedido com avaliações específicas e histórico consultável.

## Relatos, solicitações e histórico

Um **relato** é uma informação que pode ser corrigida. Uma **solicitação** é um pedido preparado a partir dos relatos de um local. Cada solicitação guarda uma cópia dos relatos e da descrição do local utilizados no momento da preparação.

Se um relato for editado, movido ou excluído, o texto de uma solicitação já encaminhada permanece preservado. Um rascunho preparado é sinalizado como desatualizado e precisa ser revisto antes de registrar seu envio. Isso evita apresentar silenciosamente um texto novo como se fosse o que já havia sido encaminhado.

Atualizar o rascunho substitui sua prévia e acrescenta um evento ao histórico. As versões anteriores do texto do rascunho não são armazenadas. Depois do encaminhamento, o texto não é regenerado pela aplicação.

O histórico guarda situação, protocolo e observação em ordem de registro. Não há datas automáticas ou controle de prazos nesta versão. Ao excluir um relato atual, sua cópia pode continuar existindo nas solicitações históricas e nos dados preservados de versões antigas.

## Persistência e estrutura do JSON

| Campo principal | Finalidade |
|---|---|
| `versao` | Identifica o formato da base, atualmente 3. |
| `locais` | ID, descrição e confirmação da referência de cada local. |
| `relatos` | ID, vínculo com o local, dificuldade, frequência, detalhes, origem e fonte. |
| `solicitacoes` | ID, local, texto, cópia dos relatos utilizados, situação, protocolo e histórico. |
| `proximo_local_id` | Próximo identificador de local. |
| `proximo_relato_id` | Próximo identificador de relato. |
| `proxima_solicitacao_id` | Próximo identificador de solicitação. |
| `dados_versao_anterior` | Conteúdo preservado de uma versão anterior, quando houver. |

Os identificadores não são reutilizados após exclusões. Antes de ler ou gravar, o programa verifica estrutura, campos obrigatórios, IDs, referências e consistência do histórico.

A gravação primeiro escreve `dados.json.tmp` e depois substitui `dados.json`. Se a gravação falhar, a alteração não é aplicada à base em memória. O temporário pode permanecer após uma falha; o arquivo principal continua sendo a base utilizada pelo programa.

Um arquivo vazio é considerado uma base nova. Um arquivo com conteúdo que não seja um JSON válido continua protegido: o programa informa o problema e encerra sem substituí-lo. O programa foi projetado para uma pessoa usando uma instância por vez; não possui sincronização entre processos ou computadores. Uma cópia manual de `dados.json`, feita com o programa fechado, permite guardar um backup.

### Compatibilidade com versões anteriores

Cadastros técnicos antigos são preservados como dados anteriores, sem virarem relatos automaticamente. Relatos da versão 2 são importados com seus IDs, locais e informações, e seu acompanhamento antigo permanece consultável. Como a versão 2 não distinguia a origem dos relatos, eles entram como **Não identificada**, exigindo revisão.

Um andamento antigo não é convertido automaticamente em uma solicitação nova: o programa anterior não armazenava o texto consolidado por local. Protocolos e históricos anteriores são preservados, sem inventar esse conteúdo. Antes de preparar um pedido novo para um relato importado, consulte seu acompanhamento anterior para evitar encaminhamento duplicado.

## Organização do código e conteúdos da disciplina

| Requisito | Aplicação no projeto |
|---|---|
| Menu de opções | `main` e `ler_opcao`. |
| `match/case` | Encaminhamento do menu principal, correção de relatos, migração e classificação do acompanhamento. |
| `if/elif/else` | Validações e condições pontuais em que há uma decisão binária simples. |
| `while` | Navegação e repetição de perguntas inválidas. |
| `for` | Leitura das coleções, análise por local e composição de solicitações. |
| Funções com parâmetros e retorno | Busca, análise, classificação de pendências, geração de texto e persistência. |
| Listas | Locais, relatos, solicitações, pontos de avaliação e históricos. |
| Tuplas | Opções fixas de dificuldades, frequências, origens e situações. |
| Dicionários | Registros e contagens por tipo de dificuldade. |
| `try/except` | Conversão de opções e tratamento de falhas de arquivos/JSON. |
| JSON | Leitura e gravação de toda a base. |
| Validação | Campos obrigatórios, escolhas válidas, vínculos e consistência dos dados. |
| Experiência do usuário | Identificação pelo nome, menus com separadores, escolhas numeradas, retorno com `0`, exemplos apenas quando úteis, confirmação e mensagens de próxima ação. |

As funções são organizadas dentro de um único arquivo para atender ao escopo escolhido pela equipe. Validação, entrada, persistência, relatos, análise e acompanhamento possuem funções próprias. Regras repetidas ficam em dicionários como `REGRAS_ANALISE` e `TRANSICOES_SITUACAO`; `match/case` organiza fluxos com várias opções. A lógica de análise e a geração do texto ficam separadas da leitura das entradas, facilitando a explicação e a verificação.

## Relação com as outras partes do Travessia

| Parte | Papel no projeto integrado |
|---|---|
| Python / Passaí | Organizar relatos, aplicar regras e acompanhar pedidos. |
| Front-end e Web Development | Apresentar os locais e informações na aplicação web. |
| Edge Computing | Demonstrar um semáforo experimental com sensoriamento e decisão local. |
| Matemática | Estudar modelos de tempo de travessia e suas hipóteses. |
| Experiência | Definir requisitos e validar a jornada de uso. |
| Storytelling | Comunicar problema, funcionamento e benefício esperado. |

Esta versão Python é local e independente. Não há API, importação/exportação operacional com o site nem conexão com ESP32 implementadas. Seus IDs e campos podem orientar um contrato comum de dados em uma evolução futura. Dados do protótipo semafórico devem continuar identificados como experimentais e separados dos relatos.

## Como medir o resultado

O painel conta solicitações por **situação atual**: preparada, encaminhada, resposta recebida e encerrada. Assim, um pedido que avançou para “Resposta recebida” deixa de ser contado como atualmente “Encaminhada”. Esses números não são totais acumulados de envios.

Solicitações de demonstração aparecem separadas. Mesmo os registros informados/documentais não são verificados automaticamente. Vários relatos podem vir da mesma pessoa e “Mais de uma vez” não informa uma quantidade exata de ocorrências.

Indicadores a avaliar com usuários incluem facilidade de concluir o cadastro, tempo para preparar uma solicitação e capacidade de encontrar pendências. Eles ainda não foram medidos em uso real. Melhorias efetivas nas travessias só poderiam ser apresentadas após verificação externa.

## Integrantes

Preencher antes da entrega:

| Nome completo | RM |
|---|---|
| Rafael Taboada Sobral | 569527 |
| Fabricio Denig De Avila | 570980 |
| Beatriz Perigo| 569654 |
