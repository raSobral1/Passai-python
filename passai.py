
import json
from pathlib import Path

ARQUIVO_DADOS = Path(__file__).resolve().with_name("dados.json")
LARGURA_TELA = 72
DIFICULDADES = (
    "O sinal fechou antes de eu terminar",
    "A rampa estava ausente ou bloqueada",
    "A calçada ou a faixa tinha obstáculos",
    "Tive dificuldade para perceber a sinalização",
    "Outra dificuldade",
)
FREQUENCIAS = ("Uma vez", "Mais de uma vez", "Não sei informar")
ORIGENS = ("Relato informado", "Fonte pública", "Exemplo fictício")
SITUACOES = ("Preparada", "Encaminhada", "Resposta recebida", "Encerrada")
TRANSICOES_SITUACAO = {
    "Preparada": ("Encaminhada", "Encerrada"),
    "Encaminhada": ("Resposta recebida", "Encerrada"),
    "Resposta recebida": ("Encerrada",),
    "Encerrada": (),
}
REGRAS_ANALISE = {
    DIFICULDADES[0]: "Avaliação do tempo destinado à travessia de pedestres.",
    DIFICULDADES[1]: "Avaliação das condições de acesso à faixa, incluindo rampas e obstáculos.",
    DIFICULDADES[2]: "Avaliação das condições de acesso à faixa, incluindo rampas e obstáculos.",
    DIFICULDADES[3]: "Avaliação da sinalização para pedestres e de sua acessibilidade.",
    DIFICULDADES[4]: "Avaliação da dificuldade adicional descrita nos relatos.",
}


def nova_base():
    return {"versao": 3, "proximo_local_id": 1, "proximo_relato_id": 1,
            "proxima_solicitacao_id": 1, "locais": [], "relatos": [], "solicitacoes": []}


def buscar_por_id(registros, identificador):
    for registro in registros:
        if registro["id"] == identificador:
            return registro
    return None


def normalizar_local(texto):
    return " ".join(texto.split()).casefold()


def buscar_local_por_descricao(locais, descricao):
    descricao_normalizada = normalizar_local(descricao)
    for local in locais:
        if normalizar_local(local["descricao"]) == descricao_normalizada:
            return local
    return None


def exigir(condicao, mensagem):
    """Centraliza as validações e mantém as regras fáceis de localizar."""
    if not condicao:
        raise ValueError(mensagem)


def validar_colecao(base, colecao, contador):
    registros = base.get(colecao)
    proximo_id = base.get(contador)
    exigir(isinstance(registros, list), f"Estrutura de {colecao} inválida.")
    exigir(type(proximo_id) is int and proximo_id >= 1, f"Contador de {colecao} inválido.")

    ids = []
    for item in registros:
        identificador = item.get("id") if isinstance(item, dict) else None
        exigir(type(identificador) is int and identificador >= 1, f"Identificação inválida em {colecao}.")
        exigir(identificador not in ids, f"Identificação repetida em {colecao}.")
        ids.append(identificador)

    exigir(not ids or proximo_id > max(ids), f"Contador inconsistente em {colecao}.")


def validar_local(local, nomes_existentes):
    descricao = local.get("descricao")
    exigir(isinstance(descricao, str) and bool(descricao.strip()), "Local sem descrição.")
    exigir(type(local.get("referencia_confirmada")) is bool, "Confirmação do local inválida.")
    nome_normalizado = normalizar_local(descricao)
    exigir(nome_normalizado not in nomes_existentes, "Local repetido.")
    nomes_existentes.append(nome_normalizado)


def validar_relato(relato):
    exigir(isinstance(relato, dict), "Relato inválido.")
    exigir(type(relato.get("id")) is int and relato["id"] >= 1, "Identificação do relato inválida.")
    exigir(type(relato.get("local_id")) is int and relato["local_id"] >= 1, "Identificação de local inválida.")
    exigir(relato.get("dificuldade") in DIFICULDADES, "Dificuldade inválida.")
    exigir(relato.get("frequencia") in FREQUENCIAS, "Frequência inválida.")
    exigir(relato.get("origem") in ORIGENS + ("Não identificada",), "Origem inválida.")

    for campo in ("detalhes", "fonte"):
        exigir(isinstance(relato.get(campo), str), f"Campo {campo} inválido.")

    exige_detalhes = relato["dificuldade"] == DIFICULDADES[-1]
    exige_fonte = relato["origem"] == "Fonte pública"
    exigir(not exige_detalhes or bool(relato["detalhes"].strip()), "Outra dificuldade precisa de uma descrição.")
    exigir(not exige_fonte or bool(relato["fonte"].strip()), "Relato público precisa de fonte.")


def validar_historico(pedido):
    historico = pedido.get("historico")
    exigir(isinstance(historico, list) and bool(historico), "Histórico ausente.")

    for evento in historico:
        exigir(isinstance(evento, dict), "Evento de histórico inválido.")
        exigir(evento.get("situacao") in SITUACOES, "Situação do histórico inválida.")
        exigir(isinstance(evento.get("observacao"), str), "Observação do histórico inválida.")
        exigir(isinstance(evento.get("protocolo"), str), "Protocolo do histórico inválido.")

    ultimo_evento = historico[-1]
    exigir(ultimo_evento["situacao"] == pedido["situacao"], "Situação atual diferente do histórico.")
    exigir(ultimo_evento["protocolo"] == pedido["protocolo"], "Protocolo atual diferente do histórico.")


def validar_solicitacao(pedido, locais):
    exigir(buscar_por_id(locais, pedido.get("local_id")) is not None, "Solicitação sem local válido.")
    exigir(pedido.get("situacao") in SITUACOES, "Situação de solicitação inválida.")

    for campo in ("texto", "local_descricao", "protocolo"):
        exigir(isinstance(pedido.get(campo), str), f"Campo {campo} inválido na solicitação.")

    exigir(bool(pedido["texto"].strip()), "Solicitação sem texto.")
    exigir(bool(pedido["local_descricao"].strip()), "Solicitação sem localização.")

    relatos = pedido.get("relatos_snapshot")
    exigir(isinstance(relatos, list) and bool(relatos), "Solicitação sem cópia dos relatos utilizados.")
    ids = []
    for relato in relatos:
        validar_relato(relato)
        exigir(relato["local_id"] == pedido["local_id"], "Relato associado ao local errado na solicitação.")
        exigir(relato["id"] not in ids, "Relato repetido na solicitação.")
        ids.append(relato["id"])

    validar_historico(pedido)


def validar_base(base):
    """Coordena validações pequenas, cada uma com uma responsabilidade."""
    exigir(isinstance(base, dict) and base.get("versao") == 3, "Formato de dados não reconhecido.")

    estruturas = (
        ("locais", "proximo_local_id"),
        ("relatos", "proximo_relato_id"),
        ("solicitacoes", "proxima_solicitacao_id"),
    )
    for colecao, contador in estruturas:
        validar_colecao(base, colecao, contador)

    nomes = []
    for local in base["locais"]:
        validar_local(local, nomes)

    for relato in base["relatos"]:
        validar_relato(relato)
        exigir(buscar_por_id(base["locais"], relato["local_id"]) is not None,
               "Relato associado a um local inexistente.")

    locais_ativos = []
    for pedido in base["solicitacoes"]:
        validar_solicitacao(pedido, base["locais"])
        if pedido["situacao"] != "Encerrada":
            exigir(pedido["local_id"] not in locais_ativos,
                   "Mais de uma solicitação ativa para o mesmo local.")
            locais_ativos.append(pedido["local_id"])


def migrar_base(antiga):
    """Preserva versões antigas sem inventar origem ou solicitações enviadas."""
    if not isinstance(antiga, dict):
        raise ValueError("Base inválida.")
    match antiga.get("versao"):
        case 3:
            return antiga
        case 2 if isinstance(antiga.get("relatos"), list):
            return migrar_versao_2(antiga)
        case None if isinstance(antiga.get("travessias"), list):
            base = nova_base()
            base["dados_versao_anterior"] = antiga
            return base
        case _:
            raise ValueError("Versão dos dados não reconhecida.")


def migrar_versao_2(antiga):
    base = nova_base()
    base["dados_versao_anterior"] = antiga

    for item in antiga["relatos"]:
        descricao = " ".join(item["local"].split())
        local = buscar_local_por_descricao(base["locais"], descricao)
        if local is None:
            local = {"id": base["proximo_local_id"], "descricao": descricao, "referencia_confirmada": False}
            base["locais"].append(local)
            base["proximo_local_id"] += 1

        base["relatos"].append({
            "id": item["id"],
            "local_id": local["id"],
            "dificuldade": item["dificuldade"],
            "frequencia": item["frequencia"],
            "detalhes": item["detalhes"],
            "origem": "Não identificada",
            "fonte": "",
            "acompanhamento_anterior": {
                "situacao": item["situacao"],
                "protocolo": item["protocolo"],
                "historico": item["historico"],
            },
        })

    base["proximo_relato_id"] = antiga["proximo_id"]
    return base


def carregar_dados(caminho):
    try:
        with caminho.open("r", encoding="utf-8-sig") as arquivo:
            base = migrar_base(json.load(arquivo))
        validar_base(base)
        return base
    except FileNotFoundError:
        return nova_base()
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, RecursionError) as erro:
        print(f"Não foi possível abrir os dados: {erro}")
        print("O arquivo foi preservado. Corrija-o ou restaure uma cópia antes de continuar.")
        return None


def salvar_dados(caminho, base):
    try:
        validar_base(base)
        temporario = caminho.with_suffix(".json.tmp")
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(base, arquivo, ensure_ascii=False, indent=2, allow_nan=False)
            arquivo.write("\n")
        temporario.replace(caminho)
        return True
    except (OSError, ValueError) as erro:
        print(f"Não foi possível salvar: {erro}")
        print("A alteração não foi aplicada; os dados anteriores foram mantidos.")
        return False


def aplicar_alteracao(base, nova):
    if salvar_dados(ARQUIVO_DADOS, nova):
        base.update(nova)
        print("Salvo com sucesso.")
        return True
    return False


def substituir(registros, alterado):
    return [alterado if item["id"] == alterado["id"] else item for item in registros]


def exibir_titulo(titulo, caractere="="):
    """Cria uma identidade visual simples para menus e seções."""
    linha = caractere * LARGURA_TELA
    print(f"\n{linha}")
    print(titulo.center(LARGURA_TELA))
    print(linha)


def ler_opcao(titulo, opcoes, voltar="Voltar"):
    exibir_titulo(titulo, "-")
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"  {numero}. {opcao}")
    print(f"  0. {voltar}")
    print("-" * LARGURA_TELA)
    while True:
        try:
            resposta = int(input("Escolha uma opção: ").strip())
            if 0 <= resposta <= len(opcoes):
                return resposta
            print(f"Escolha um número de 0 a {len(opcoes)}.")
        except ValueError:
            print("Digite apenas o número da opção.")


def ler_texto(pergunta, exemplo=None, obrigatorio=True, atual=None):
    print(f"\n{pergunta}")
    if exemplo:
        print(f"Exemplo: {exemplo}")
    if atual is not None:
        print(f"Atual: {atual or 'Não informado'}. Enter mantém este valor.")
        if not obrigatorio:
            print("Digite - para apagar este campo.")
    elif not obrigatorio:
        print("Opcional: pressione Enter para pular.")
    print("Digite 0 para voltar.")
    while True:
        resposta = input("Sua resposta: ").strip()
        if resposta == "0":
            return None
        if not resposta and atual is not None:
            resposta = atual
        if resposta == "-" and not obrigatorio:
            return ""
        if resposta or not obrigatorio:
            return resposta
        mensagem = "Este campo é obrigatório."
        if exemplo:
            mensagem += f" Exemplo: {exemplo}"
        print(mensagem)


def confirmar(pergunta):
    while True:
        resposta = input(f"{pergunta} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        elif resposta in ("n", "nao", "não"):
            return False
        else:
            print("Digite s para confirmar ou n para cancelar.")


def ler_nome():
    """Identifica a pessoa apenas durante a execução atual."""
    print("\nAntes de começar, como você gostaria de ser chamado?")
    print("Digite 0 para sair.")
    while True:
        nome = input("Nome: ").strip()
        if nome == "0":
            return None
        if nome:
            return " ".join(nome.split())
        print("Digite seu nome para continuar.")


def selecionar_local(base, permitir_novo=False):
    locais = base["locais"]
    opcoes = [item["descricao"] for item in locais]
    if permitir_novo:
        opcoes.append("Informar outro local")
    if not opcoes:
        print("Ainda não há locais. Registre uma dificuldade na opção 1.")
        return None
    if locais or not permitir_novo:
        escolha = ler_opcao("Escolha o local:", opcoes)
        if escolha == 0:
            return None
        if escolha <= len(locais):
            return locais[escolha - 1]
    descricao = ler_texto("Onde aconteceu? Informe rua e ponto de referência.",
                         "Rua Exemplo, em frente ao mercado, perto do número 100, Santana")
    if descricao is None:
        return None
    descricao = " ".join(descricao.split())
    local_existente = buscar_local_por_descricao(locais, descricao)
    if local_existente is not None:
        return local_existente
    return {"id": base["proximo_local_id"], "descricao": descricao, "referencia_confirmada": False}


def ler_origem():
    opcao = ler_opcao("Qual é a origem deste registro?", ORIGENS)
    if opcao == 0:
        return None
    fonte = ""
    if ORIGENS[opcao - 1] == "Fonte pública":
        fonte = ler_texto("Qual fonte pública descreve a dificuldade?", "Título da publicação e seu endereço na internet")
        if fonte is None:
            return None
    return {"origem": ORIGENS[opcao - 1], "fonte": fonte}


def registrar_relato(base):
    opcao = ler_opcao("O que dificultou a travessia?", DIFICULDADES)
    if opcao == 0:
        return
    local = selecionar_local(base, permitir_novo=True)
    if local is None:
        return
    frequencia = ler_opcao("Com que frequência isso aconteceu, segundo o relato?", FREQUENCIAS)
    if frequencia == 0:
        return
    detalhes = ler_texto(
        "Conte mais algum detalhe:",
        obrigatorio=DIFICULDADES[opcao - 1] == DIFICULDADES[-1],
    )
    if detalhes is None:
        return
    origem = ler_origem()
    if origem is None:
        return
    relato = {"id": base["proximo_relato_id"], "local_id": local["id"], "dificuldade": DIFICULDADES[opcao - 1],
              "frequencia": FREQUENCIAS[frequencia - 1], "detalhes": detalhes, **origem}
    exibir_relato(relato)
    print(f"Local: {local['descricao']}")
    if confirmar("Salvar este relato?"):
        nova = base.copy()
        nova["relatos"] = base["relatos"] + [relato]
        nova["proximo_relato_id"] += 1
        if buscar_por_id(base["locais"], local["id"]) is None:
            nova["locais"] = base["locais"] + [local]
            nova["proximo_local_id"] += 1
        if aplicar_alteracao(base, nova):
            print(f"Relato {relato['id']:03d} registrado. Analise o local na opção 3.")


def exibir_relato(relato):
    print(f"\nRELATO {relato['id']:03d} — {relato['dificuldade']}")
    print(f"Frequência informada: {relato['frequencia']}")
    print(f"Detalhes: {relato['detalhes'] or 'Não informados'}")
    print(f"Origem: {relato['origem']} | Fonte: {relato['fonte'] or 'Não se aplica/não informada'}")
    if "acompanhamento_anterior" in relato:
        anterior = relato["acompanhamento_anterior"]
        print(f"Acompanhamento da versão anterior: {anterior['situacao']} | Protocolo: {anterior['protocolo'] or 'Não informado'}")
        for evento in anterior["historico"]:
            print(f"  {evento['situacao']}: {evento['observacao']}")


def relatos_do_local(base, local_id):
    return [relato for relato in base["relatos"] if relato["local_id"] == local_id]


def corrigir_relato(base, relato):
    opcao = ler_opcao("O que deseja corrigir?", ("Dificuldade", "Frequência", "Detalhes", "Origem dos dados", "Mover para outro local"))
    if opcao == 0:
        return
    alterado = relato.copy()
    nova = base.copy()

    match opcao:
        case 1:
            escolha = ler_opcao("Escolha a dificuldade:", DIFICULDADES)
            if escolha == 0:
                return
            alterado["dificuldade"] = DIFICULDADES[escolha - 1]
        case 2:
            escolha = ler_opcao("Escolha a frequência:", FREQUENCIAS)
            if escolha == 0:
                return
            alterado["frequencia"] = FREQUENCIAS[escolha - 1]
        case 3:
            valor = ler_texto(
                "Conte o que aconteceu:",
                obrigatorio=relato["dificuldade"] == DIFICULDADES[-1],
                atual=relato["detalhes"],
            )
            if valor is None:
                return
            alterado["detalhes"] = valor
        case 4:
            origem = ler_origem()
            if origem is None:
                return
            alterado.update(origem)
        case 5:
            local = selecionar_local(base, permitir_novo=True)
            if local is None:
                return
            alterado["local_id"] = local["id"]
            if buscar_por_id(base["locais"], local["id"]) is None:
                nova["locais"] = base["locais"] + [local]
                nova["proximo_local_id"] += 1
    if alterado["dificuldade"] == DIFICULDADES[-1] and not alterado["detalhes"]:
        detalhes = ler_texto("Descreva a outra dificuldade:")
        if detalhes is None:
            return
        alterado["detalhes"] = detalhes
    exibir_relato(alterado)
    if confirmar("Salvar correção?"):
        nova["relatos"] = substituir(base["relatos"], alterado)
        aplicar_alteracao(base, nova)


def completar_local(base, local):
    descricao = ler_texto("Identifique o local com rua, bairro e um número ou ponto de referência:",
                         "Rua Exemplo, perto do número 100, em frente ao mercado, Santana", atual=local["descricao"])
    if descricao is None:
        return None
    descricao = " ".join(descricao.split())
    for outro in base["locais"]:
        if outro["id"] != local["id"] and normalizar_local(outro["descricao"]) == normalizar_local(descricao):
            print("Este local já existe. Use 'Mover para outro local' ao corrigir cada relato.")
            return None
    confirmado = confirmar("Com essa descrição, outra pessoa consegue identificar a travessia?")
    alterado = {**local, "descricao": descricao, "referencia_confirmada": confirmado}
    if confirmar("Salvar informações do local?"):
        nova = base.copy()
        nova["locais"] = substituir(base["locais"], alterado)
        if aplicar_alteracao(base, nova):
            return alterado
    return None


def consultar_relatos(base):
    local = selecionar_local(base)
    if local is None:
        return
    while True:
        relatos = relatos_do_local(base, local["id"])
        opcoes = [f"Relato {r['id']:03d} — {r['dificuldade']} [{r['origem']}]" for r in relatos]
        escolha = ler_opcao(f"RELATOS: {local['descricao']}", opcoes + ["Completar/corrigir referência do local"])
        if escolha == 0:
            return
        if escolha == len(opcoes) + 1:
            local = completar_local(base, local) or local
            continue
        relato = relatos[escolha - 1]
        exibir_relato(relato)
        acao = ler_opcao("O que deseja fazer?", ("Corrigir relato", "Excluir relato"))
        match acao:
            case 1:
                corrigir_relato(base, relato)
            case 2:
                excluir_relato(base, relato)


def excluir_relato(base, relato):
    print("Solicitações já preparadas conservam sua cópia histórica deste relato.")
    if not confirmar("Excluir o relato da lista atual?"):
        return
    nova = base.copy()
    nova["relatos"] = [item for item in base["relatos"] if item["id"] != relato["id"]]
    aplicar_alteracao(base, nova)


def analisar_local(base, local):
    """Regras explicáveis; não calcula risco nem verifica a veracidade do relato."""
    relatos = relatos_do_local(base, local["id"])
    pontos, pendencias, contagem = [], [], {}
    if not relatos:
        pendencias.append("Registrar ao menos uma dificuldade neste local.")
    if not local["referencia_confirmada"]:
        pendencias.append("Completar e confirmar a referência do local.")
    for relato in relatos:
        dificuldade = relato["dificuldade"]
        contagem[dificuldade] = contagem.get(dificuldade, 0) + 1
        ponto = REGRAS_ANALISE[dificuldade]
        if ponto not in pontos:
            pontos.append(ponto)
        if relato["origem"] == "Não identificada":
            pendencias.append(f"Identificar a origem do relato {relato['id']:03d} na opção 2.")
    return {"relatos": relatos, "pontos": pontos, "pendencias": pendencias, "contagem": contagem}


def solicitacao_ativa(base, local_id):
    for pedido in base["solicitacoes"]:
        if pedido["local_id"] == local_id and pedido["situacao"] != "Encerrada":
            return pedido
    return None


def conteudo_atualizado(base, pedido):
    local = buscar_por_id(base["locais"], pedido["local_id"])
    return local["descricao"] == pedido["local_descricao"] and relatos_do_local(base, local["id"]) == pedido["relatos_snapshot"]


def gerar_solicitacao(local, analise):
    linhas = ["SOLICITAÇÃO DE AVALIAÇÃO DE ACESSIBILIDADE", f"Local informado: {local['descricao']}"]
    if any(r["origem"] == "Exemplo fictício" for r in analise["relatos"]):
        linhas.insert(0, "DEMONSTRAÇÃO — CONTÉM DADOS FICTÍCIOS; NÃO ENCAMINHAR COMO RELATO REAL.")
    linhas.append(f"Registros relacionados: {len(analise['relatos'])} (não equivalem a pessoas distintas).")
    linhas.append("\nDificuldades informadas:")
    for relato in analise["relatos"]:
        linhas.append(f"- Relato {relato['id']:03d}: {relato['dificuldade']}. Frequência informada: {relato['frequencia']}.")
        linhas.append(f"  Origem: {relato['origem']}.")
        if relato["fonte"]:
            linhas.append(f"  Fonte: {relato['fonte']}")
        if relato["detalhes"]:
            linhas.append(f"  Detalhes: {relato['detalhes']}")
    linhas.append("\nSolicita-se:")
    for ponto in analise["pontos"]:
        linhas.append(f"- {ponto}")
    linhas.append("\nAs informações são relatos sem verificação ou medição técnica pelo Passaí. Não constituem laudo nem avaliação de legalidade.")
    return "\n".join(linhas)


def exibir_pedido(pedido):
    print(f"\nSOLICITAÇÃO {pedido['id']:03d} — {pedido['situacao']}")
    print("--- INÍCIO DO TEXTO PARA COPIAR ---")
    print(pedido["texto"])
    print("--- FIM DO TEXTO PARA COPIAR ---")
    print(f"Protocolo externo: {pedido['protocolo'] or 'Não informado'}")
    print("Nada é enviado automaticamente pelo programa.")


def preparar_solicitacao(base):
    local = selecionar_local(base)
    if local is None:
        return
    analise = analisar_local(base, local)
    print(f"\nANÁLISE DOS RELATOS — {local['descricao']}")
    for dificuldade, total in analise["contagem"].items():
        print(f"{total} registro(s): {dificuldade}")
    for ponto in analise["pontos"]:
        print(f"Pedido sugerido: {ponto}")
    ativo = solicitacao_ativa(base, local["id"])
    if ativo is not None and ativo["situacao"] != "Preparada":
        print("Já existe solicitação encaminhada ou respondida. Acompanhe-a na opção 4.")
        if not conteudo_atualizado(base, ativo):
            print("Há alterações nos relatos/local que não constam no texto anteriormente preparado.")
        exibir_pedido(ativo)
        return
    if analise["pendencias"]:
        for pendencia in analise["pendencias"]:
            print(f"Pendente: {pendencia}")
        if not local["referencia_confirmada"] and confirmar("Deseja completar a referência agora?"):
            local = completar_local(base, local) or local
            analise = analisar_local(base, local)
        if analise["pendencias"]:
            print("Complete as informações indicadas antes de preparar o pedido.")
            return
    texto = gerar_solicitacao(local, analise)
    print("\nPRÉVIA DO PEDIDO\n" + texto)
    if ativo is not None and conteudo_atualizado(base, ativo):
        print(f"Este conteúdo já está salvo na solicitação {ativo['id']:03d}. Registre o envio na opção 4 após encaminhá-lo.")
        return
    if not confirmar("Salvar o pedido como preparado" + (", atualizando o rascunho existente?" if ativo else "?")):
        return
    pedido = ativo.copy() if ativo else {"id": base["proxima_solicitacao_id"], "local_id": local["id"],
                                        "situacao": "Preparada", "protocolo": "", "historico": []}
    pedido.update({"local_descricao": local["descricao"], "relatos_snapshot": [r.copy() for r in analise["relatos"]], "texto": texto})
    pedido["historico"] = pedido["historico"] + [{"situacao": "Preparada", "protocolo": "",
        "observacao": "Rascunho atualizado com os relatos atuais." if ativo else "Solicitação preparada, ainda não encaminhada."}]
    nova = base.copy()
    nova["solicitacoes"] = substituir(base["solicitacoes"], pedido) if ativo else base["solicitacoes"] + [pedido]
    if ativo is None:
        nova["proxima_solicitacao_id"] += 1
    if aplicar_alteracao(base, nova):
        print(f"Solicitação {pedido['id']:03d} preparada. O envio é feito por você fora do programa.")


def atualizar_andamento(base):
    if not base["solicitacoes"]:
        print("Nenhuma solicitação preparada. Use a opção 3 primeiro.")
        return
    escolha = ler_opcao("Escolha uma solicitação:", [f"{p['id']:03d} — {p['local_descricao']} | {p['situacao']}" for p in base["solicitacoes"]])
    if escolha == 0:
        return
    pedido = base["solicitacoes"][escolha - 1]
    exibir_pedido(pedido)
    for numero, evento in enumerate(pedido["historico"], start=1):
        print(f"{numero}. {evento['situacao']} | Protocolo: {evento['protocolo'] or 'Não informado'} | {evento['observacao']}")
    if pedido["situacao"] == "Encerrada":
        print("Histórico encerrado. Se necessário, prepare uma nova solicitação na opção 3.")
        return
    destinos = TRANSICOES_SITUACAO[pedido["situacao"]]
    opcoes = [f"Registrar: {estado}" for estado in destinos] + ["Adicionar observação sem mudar a situação"]
    acao = ler_opcao("Como deseja atualizar?", opcoes)
    if acao == 0:
        return
    situacao = destinos[acao - 1] if acao <= len(destinos) else pedido["situacao"]
    if situacao == "Encaminhada" and pedido["situacao"] == "Preparada":
        if not conteudo_atualizado(base, pedido):
            print("O rascunho está desatualizado. Revise e prepare o texto atual na opção 3 antes do envio.")
            return
        ficticio = any(r["origem"] == "Exemplo fictício" for r in pedido["relatos_snapshot"])
        pergunta = "Registrar encaminhamento fictício somente para testar o acompanhamento?" if ficticio else "Você já encaminhou esse texto pelo canal de atendimento escolhido?"
        if not confirmar(pergunta):
            return
    if situacao == "Encerrada":
        print("Encerrar finaliza o acompanhamento; não comprova que o problema foi resolvido.")
    protocolo = pedido["protocolo"]
    if situacao in ("Encaminhada", "Resposta recebida"):
        protocolo = ler_texto("Protocolo fornecido pelo atendimento, se houver:", "2026-001234", False, pedido["protocolo"])
        if protocolo is None:
            return
    observacao = ler_texto("Registre o que mudou:", obrigatorio=situacao == "Encerrada")
    if observacao is None:
        return
    print(f"Novo andamento: {situacao} | Protocolo: {protocolo or 'Não informado'}")
    if confirmar("Salvar atualização?"):
        alterado = {**pedido, "situacao": situacao, "protocolo": protocolo,
            "historico": pedido["historico"] + [{"situacao": situacao, "protocolo": protocolo, "observacao": observacao}]}
        nova = base.copy()
        nova["solicitacoes"] = substituir(base["solicitacoes"], alterado)
        aplicar_alteracao(base, nova)


def classificar_pendencia(base, local):
    analise = analisar_local(base, local)
    ativo = solicitacao_ativa(base, local["id"])
    if ativo:
        return classificar_solicitacao_ativa(base, ativo, analise)
    if not analise["relatos"]:
        return "Sem relatos atuais", "Cadastre uma dificuldade na opção 1, se necessário."
    encerradas = [p for p in base["solicitacoes"] if p["local_id"] == local["id"] and p["situacao"] == "Encerrada"]
    if encerradas and conteudo_atualizado(base, encerradas[-1]):
        return "Acompanhamento encerrado", "Consulte o histórico na opção 4; nova solicitação pode ser preparada se necessário."
    if analise["pendencias"]:
        return "Informações a completar", " ".join(analise["pendencias"])
    return "Pedido a preparar", "Analise o local e prepare a solicitação na opção 3."


def classificar_solicitacao_ativa(base, pedido, analise):
    match pedido["situacao"]:
        case "Preparada" if analise["pendencias"] or not conteudo_atualizado(base, pedido):
            return "Revisar rascunho", "Atualize informações e prepare novamente na opção 3."
        case "Preparada" if any(r["origem"] == "Exemplo fictício" for r in analise["relatos"]):
            return "Demonstração", "Pedido fictício preparado; teste o acompanhamento na opção 4, sem envio real."
        case "Preparada":
            return "Aguardando encaminhamento", "Copie o pedido e, após o envio, registre o andamento na opção 4."
        case "Encaminhada":
            return "Aguardando resposta", "Consulte o atendimento com o protocolo e registre o retorno na opção 4."
        case "Resposta recebida":
            return "Resposta a avaliar", "Leia o retorno e registre o próximo passo ou encerramento na opção 4."


def contar_solicitacoes(solicitacoes, situacao):
    contagem = {"informadas": 0, "demonstracao": 0}
    for pedido in solicitacoes:
        if pedido["situacao"] != situacao:
            continue
        chave = "demonstracao" if any(
            relato["origem"] == "Exemplo fictício" for relato in pedido["relatos_snapshot"]
        ) else "informadas"
        contagem[chave] += 1
    return contagem


def exibir_pendencias(base):
    if not base["locais"]:
        print("Ainda não há relatos. Comece pela opção 1.")
        return
    print("\nPENDÊNCIAS E PRÓXIMOS PASSOS POR LOCAL")
    print("A ordem é a de cadastro; não representa prioridade de risco.")
    for local in base["locais"]:
        categoria, acao = classificar_pendencia(base, local)
        print(f"\n{local['descricao']} — {categoria}\nPróxima ação: {acao}")
        ativo = solicitacao_ativa(base, local["id"])
        if ativo:
            print(f"Solicitação {ativo['id']:03d} | Protocolo: {ativo['protocolo'] or 'Não informado'}")
            if any(r["origem"] == "Exemplo fictício" for r in ativo["relatos_snapshot"]):
                print("DEMONSTRAÇÃO: este acompanhamento contém dados fictícios.")
            if ativo["situacao"] != "Preparada" and not conteudo_atualizado(base, ativo):
                print("Há alterações nos dados atuais que não estão no texto já encaminhado.")
    print("\nINDICADORES DE ACOMPANHAMENTO")
    for situacao in SITUACOES:
        contagem = contar_solicitacoes(base["solicitacoes"], situacao)
        print(f"{situacao}: {contagem['informadas']} informada(s)/documental(is) | "
              f"{contagem['demonstracao']} de demonstração")
    print("Contagens de solicitações por situação atual; não medem pessoas beneficiadas nem melhorias verificadas.")


def contar_por_campo(registros, campo, opcoes):
    """Monta contagens sem repetir a mesma lógica em cada relatório."""
    return {
        opcao: sum(1 for registro in registros if registro[campo] == opcao)
        for opcao in opcoes
    }


def exibir_contagens(titulo, contagens):
    print(f"\n{titulo}:")
    exibiu_item = False
    for nome, quantidade in contagens.items():
        if quantidade > 0:
            print(f"  - {nome}: {quantidade}")
            exibiu_item = True
    if not exibiu_item:
        print("  - Nenhum registro.")


def exibir_resumo_geral(base):
    exibir_titulo("RESUMO GERAL DO PASSAÍ")
    total_ativas = sum(
        1 for pedido in base["solicitacoes"] if pedido["situacao"] != "Encerrada"
    )
    print(f"Locais cadastrados: {len(base['locais'])}")
    print(f"Relatos registrados: {len(base['relatos'])}")
    print(f"Solicitações criadas: {len(base['solicitacoes'])}")
    print(f"Solicitações em acompanhamento: {total_ativas}")

    origens = ORIGENS + ("Não identificada",)
    exibir_contagens(
        "Relatos por dificuldade",
        contar_por_campo(base["relatos"], "dificuldade", DIFICULDADES),
    )
    exibir_contagens(
        "Relatos por origem",
        contar_por_campo(base["relatos"], "origem", origens),
    )
    exibir_contagens(
        "Solicitações por situação atual",
        contar_por_campo(base["solicitacoes"], "situacao", SITUACOES),
    )

    print("\nEssas contagens organizam os registros do sistema; não medem risco")
    print("nem comprovam melhorias realizadas nas travessias.")


def main():
    exibir_titulo("PASSAÍ — APOIO À ACESSIBILIDADE NAS TRAVESSIAS")
    print("Relate dificuldades, prepare pedidos e acompanhe o retorno.".center(LARGURA_TELA))
    nome = ler_nome()
    if nome is None:
        print("Programa encerrado.")
        return
    print(f"\nOlá, {nome}! Vamos começar.")
    base = carregar_dados(ARQUIVO_DADOS)
    if base is None:
        return
    try:
        while True:
            opcao = ler_opcao(f"MENU PRINCIPAL — {nome}", (
                "Registrar uma dificuldade", "Consultar relatos de um local",
                "Analisar relatos e preparar solicitação", "Atualizar acompanhamento",
                "Ver solicitações pendentes", "Ver resumo geral do sistema",
            ), voltar="Sair")
            match opcao:
                case 1:
                    registrar_relato(base)
                case 2:
                    consultar_relatos(base)
                case 3:
                    preparar_solicitacao(base)
                case 4:
                    atualizar_andamento(base)
                case 5:
                    exibir_pendencias(base)
                case 6:
                    exibir_resumo_geral(base)
                case 0:
                    exibir_titulo("ATÉ LOGO", "-")
                    print("Alterações confirmadas foram salvas.")
                    break
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado. Alterações já salvas foram preservadas.")


if __name__ == "__main__":
    main()
