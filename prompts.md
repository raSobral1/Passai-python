# Registro de uso de Inteligência Artificial - Passaí

## Objetivo deste documento

Este arquivo documenta como a Inteligência Artificial foi utilizada como ferramenta de apoio durante o desenvolvimento do **Passaí**, aplicação em Python do projeto Travessia.

A equipe definiu o problema, avaliou as funcionalidades, escolheu os fluxos do menu e validou o resultado final. A IA foi utilizada como apoio para organizar ideias, sugerir soluções, revisar o código, gerar cenários de teste e melhorar a documentação. As respostas não foram aceitas automaticamente: as sugestões foram analisadas e ajustadas de acordo com o escopo da disciplina e com a experiência de uso desejada pela equipe.

Os prompts abaixo são versões organizadas das solicitações feitas durante o desenvolvimento. As perguntas foram formuladas para obter orientações e explicações passo a passo. A redação foi ajustada para facilitar a leitura deste documento, preservando a finalidade original de cada pergunta.

## Ferramenta de IA utilizada

| Ferramenta | Finalidades |
|---|---|
| Codex, da OpenAI | Orientações para o planejamento da aplicação, explicações sobre implementação em Python, apoio na revisão do código, elaboração de testes e organização da documentação. |

## Prompts utilizados

### 1. Planejamento da aplicação em Python

> Estou planejando a parte de Python do projeto Travessia e preciso relacioná-la aos requisitos da disciplina Computational Thinking with Python. Como posso transformar essa ideia em uma aplicação de terminal ligada ao problema real das travessias? Preciso utilizar menu, validações, estruturas de decisão e repetição, funções, listas, tuplas, dicionários e persistência em JSON. Explique passo a passo como posso planejar a solução, mostrando alternativas para que eu escolha e desenvolva a aplicação.

**Finalidade:** definir um recorte viável para a disciplina e relacionar a proposta do Travessia aos conteúdos de Python.

**Resultado aproveitado:** a ideia de registrar dificuldades por local, gerar um pedido de melhoria e acompanhar o retorno.

### 2. Salvamento e leitura do JSON

> Preciso entender como salvar os locais, as dificuldades e os pedidos do Passaí em um arquivo JSON. O programa deve funcionar quando o arquivo não existir, estiver vazio ou ainda não tiver cadastros, e não pode perder o conteúdo anterior se ocorrer um erro durante a gravação. Explique passo a passo como posso fazer a leitura e o salvamento, usando apenas recursos adequados à disciplina e bibliotecas padrão do Python.

**Finalidade:** criar uma persistência simples e segura, sem utilizar banco de dados ou bibliotecas externas.

**Resultado aproveitado:** leitura de uma base vazia, validação da estrutura e gravação primeiro em um arquivo temporário antes de substituir o JSON principal.

### 3. Organização do código e do menu

> Meu código do menu possui muitos `if` e `elif`, e algumas ações, como alterar e excluir dificuldades, estão escondidas em submenus. Como posso organizar melhor essa lógica em funções menores e utilizar `match/case` quando fizer sentido? Também quero usar o número 0 para cancelar operações e mostrar exemplos somente quando forem úteis. Explique passo a passo como posso fazer essa reorganização e apresente exemplos pequenos que eu consiga adaptar ao meu código.

**Finalidade:** melhorar a legibilidade do código e tornar a navegação mais simples.

**Resultado aproveitado:** separação das responsabilidades em funções, uso de `match/case`, opções diretas de consulta, alteração e exclusão, além da padronização do cancelamento com `0`.

### 4. Simplificação do fluxo dos pedidos

> O fluxo para analisar o local, preparar a solicitação e atualizar o acompanhamento ficou confuso e com muitas opções internas. Como posso deixar essa parte mais simples, permitindo criar o texto do pedido e depois registrar o que aconteceu? Explique passo a passo como posso organizar esse fluxo para mostrar somente a próxima ação necessária em cada etapa.

**Finalidade:** deixar a criação e o acompanhamento do pedido mais fáceis de entender.

**Resultado aproveitado:** as opções **Criar um pedido de melhoria** e **Registrar envio ou resposta**, seguindo o fluxo preparada, encaminhada, resposta recebida e encerrada.

### 5. Revisão do código e procura por erros

> Quero revisar o arquivo `passai.py` para descobrir possíveis erros de lógica, problemas de validação ou situações em que os dados podem não ser salvos. Preciso verificar cadastro, alteração, exclusão, cancelamento, JSON vazio, pedido desatualizado e falha durante a gravação, sem modificar os dados reais. Explique passo a passo como posso fazer essa revisão e monte uma lista de verificações que eu possa executar no projeto.

**Finalidade:** identificar falhas antes da entrega e confirmar a segurança da persistência.

**Resultado aproveitado:** correções no tratamento do JSON, preservação do arquivo anterior em caso de erro e confirmação de que a memória só é atualizada depois de uma gravação bem-sucedida.

### 6. Geração de testes

> Quero aprender a testar as principais funções do Passaí: cadastro, edição, exclusão, criação do pedido, envio, resposta, encerramento, reinicialização e reabertura do JSON. Também preciso verificar cancelamentos, entradas inválidas e uma falha simulada de gravação. Explique o que devo conferir em cada cenário e como interpretar os resultados.

**Finalidade:** verificar automaticamente os fluxos principais e os casos de erro.

**Resultado aproveitado:** criação de cenários de teste para o funcionamento completo do sistema, incluindo persistência, cancelamentos e proteção dos dados.

### 7. Revisão do README

> Meu README possui informações importantes, mas está muito extenso. Como posso reorganizá-lo para ter uma introdução simples e explicar o problema, o objetivo, o menu, o salvamento em JSON e os conceitos de Python utilizados? Pode estruturar o documento, indicando o que é essencial, o que pode ser resumido e quais perguntas técnicas sobre o sistema vale a pena responder.

**Finalidade:** produzir uma documentação clara, completa e adequada para uma entrega acadêmica.

**Resultado aproveitado:** reorganização do README e inclusão de explicações simples sobre carregamento, gravação, identificadores, histórico, cópia dos relatos e reinicialização.

## Funcionalidades desenvolvidas com orientação da IA

Com base nas explicações e alternativas apresentadas pela ferramenta, a equipe escolheu os caminhos adequados, adaptou as orientações ao projeto e desenvolveu ou revisou os seguintes pontos:

- Definição do recorte da aplicação em Python dentro do tema Travessia.
- Organização do menu e redução de submenus desnecessários.
- Separação do código em funções com responsabilidades específicas.
- Uso de `match/case` para organizar fluxos com várias opções.
- Persistência dos dados em JSON.
- Tratamento de arquivo inexistente, vazio ou inválido.
- Gravação por meio de arquivo temporário para proteger o JSON principal.
- Criação do texto de pedido de melhoria a partir das dificuldades cadastradas.
- Simplificação do acompanhamento do pedido.
- Reinicialização completa do sistema com confirmação.
- Aplicação de uma lista de revisão do código e criação de cenários de teste.
- Reorganização do README.

A ferramenta apresentou explicações, exemplos e possibilidades de organização. A equipe foi responsável por decidir o que seria utilizado, adaptar as orientações, executar o programa e verificar os resultados.

## Como os resultados foram verificados e ajustados

A equipe não utilizou as respostas da IA sem revisão. O processo de verificação incluiu:

1. Leitura das orientações e dos exemplos apresentados, comparando-os com os requisitos da disciplina.
2. Execução manual do programa pelo terminal.
3. Testes de cadastro, consulta, alteração e exclusão de dificuldades.
4. Fechamento e reabertura do programa para confirmar o salvamento no JSON.
5. Testes com arquivo inexistente, vazio e inválido.
6. Testes do fluxo completo do pedido: preparação, envio, resposta e encerramento.
7. Testes de cancelamento com o número `0` e com respostas negativas nas confirmações.
8. Simulação de falha durante a gravação para verificar se o arquivo anterior era preservado.
9. Testes da opção de excluir todos os dados e reiniciar o sistema.
10. Ajustes sucessivos no menu após a equipe considerar alguns fluxos confusos.

Ao final, foram executados **28 testes automatizados**, além das verificações manuais no terminal. Os testes abrangeram os fluxos principais, a persistência dos dados e situações de erro.

## Análise crítica sobre o uso da IA

### Benefícios

A IA ajudou a transformar ideias gerais em alternativas mais concretas, sugeriu formas de organizar o código e chamou atenção para casos que poderiam ser esquecidos, como JSON vazio, falha de gravação e cancelamento de operações. Também acelerou a criação de testes e a revisão da documentação.

### Reflexão final

O uso da IA foi positivo como apoio ao raciocínio, à programação e aos testes, mas não substituiu as decisões da equipe. A qualidade do resultado dependeu de perguntas claras, revisão humana, execução do programa e ajustes feitos a partir dos problemas encontrados.
