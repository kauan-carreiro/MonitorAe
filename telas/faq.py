import json
import os
import unicodedata
import urllib.request

from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao, pedir_texto,
    sucesso, erro, info, pausar,
    AMARELO, CINZA, RESET, NEGRITO
)
from utils.emojis import (
    CADERNO, AVISO, RAIO, ESTRELA
)

# ── Caminhos dos arquivos ────────────────────────────────────────────────────

PASTA_ATUAL      = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FAQ      = os.path.join(PASTA_ATUAL, "..", "data", "faq.json")
CAMINHO_SUGEST   = os.path.join(PASTA_ATUAL, "..", "data", "sugestoes_faq.json")


# ── Funções de acesso aos arquivos ───────────────────────────────────────────

def carregar_faq():
    """Lê o arquivo faq.json e retorna o conteúdo."""
    if not os.path.exists(CAMINHO_FAQ):
        return {"perguntas": []}
    try:
        with open(CAMINHO_FAQ, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"perguntas": []}


def salvar_faq(dados):
    """Salva o conteúdo atualizado no faq.json."""
    try:
        with open(CAMINHO_FAQ, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except OSError:
        pass


def carregar_sugestoes():
    """Lê o arquivo sugestoes_faq.json."""
    if not os.path.exists(CAMINHO_SUGEST):
        return {"sugestoes": []}
    try:
        with open(CAMINHO_SUGEST, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"sugestoes": []}


def salvar_sugestoes(dados):
    """Salva as sugestões atualizadas."""
    try:
        with open(CAMINHO_SUGEST, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except OSError:
        pass


# ── Normalização de texto (remove acentos) ──────────────────────────────────

def _sem_acento(texto):
    """
    Remove acentos do texto para permitir busca sem acentuação.
    Ex: "número" → "numero", "divisível" → "divisivel"
    """
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")


# ── Palavras genéricas ignoradas na busca ────────────────────────────────────

PALAVRAS_IGNORADAS = {
    _sem_acento(p) for p in {
        "como", "saber", "se", "um", "uma", "e", "por", "de", "do", "da",
        "o", "a", "os", "as", "que", "qual", "quais", "para", "pra", "com",
        "em", "no", "na", "nos", "nas", "ao", "aos", "a", "as", "ou",
        "nao", "sim", "eu", "me", "meu", "minha", "meus", "minhas", "seu",
        "sua", "seus", "suas", "ele", "ela", "eles", "elas", "isso", "isto",
        "aqui", "la", "mais", "menos", "muito", "pouco", "ja", "ainda",
        "quando", "onde", "quem", "por", "porque", "porque", "fazer", "feito",
        "ter", "ser", "estar", "tem", "sao", "foi", "esta", "posso", "pode",
        "devo", "preciso", "quero", "tenho",
    }
}


# ── Busca por palavras-chave ─────────────────────────────────────────────────

def _filtrar_palavras(texto):
    """
    Separa o texto em palavras, remove acentos, descarta as genéricas e as muito curtas.
    Retorna um conjunto (set) com as palavras relevantes normalizadas.
    """
    palavras = _sem_acento(texto.lower()).split()
    return {p for p in palavras if p not in PALAVRAS_IGNORADAS and len(p) > 2}


def _palavras_parecidas(palavra1, palavra2):
    """
    Verifica se duas palavras têm a mesma raiz comparando os primeiros 5
    caracteres. Isso ajuda a reconhecer conjugações do mesmo verbo.
    Exemplos: "excluir" e "excluo" -> ambas começam com "exclu" -> match.
    Só compara palavras com pelo menos 5 letras para evitar erros.
    """
    if len(palavra1) < 5 or len(palavra2) < 5:
        return False
    return palavra1[:5] == palavra2[:5]


def buscar_faq(duvida, perguntas):
    """
    Busca as perguntas da FAQ cujo texto contenha ao menos uma palavra
    relevante da dúvida digitada. Compara por igualdade exata e também
    por raiz (primeiros 5 caracteres) para lidar com conjugações verbais.

    Retorna a lista em ordem alfabética.
    """
    palavras_duvida = _filtrar_palavras(duvida)

    if not palavras_duvida:
        return []

    encontradas = []
    for pergunta in perguntas:
        palavras_pergunta = _filtrar_palavras(pergunta.get("pergunta", ""))

        # Verifica se alguma palavra da dúvida bate com alguma da pergunta
        tem_match = False
        for pd in palavras_duvida:
            for pp in palavras_pergunta:
                if pd == pp or _palavras_parecidas(pd, pp):
                    tem_match = True
                    break
            if tem_match:
                break

        if tem_match:
            encontradas.append(pergunta)

    return sorted(encontradas, key=lambda p: p["pergunta"].lower())


# ── Chamada à LLM (API do Groq) ─────────────────────────────────────────────

def _carregar_env():
    """
    Lê o arquivo .env na raiz do projeto e carrega as variáveis
    de ambiente, sem depender de nenhuma lib externa.
    """
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    caminho_env = os.path.normpath(os.path.join(raiz, ".env"))

    if not os.path.exists(caminho_env):
        return

    with open(caminho_env, "r", encoding="utf-8") as f:
        for linha_env in f:
            linha_env = linha_env.strip()
            # Ignora linhas vazias e comentários
            if not linha_env or linha_env.startswith("#"):
                continue
            if "=" in linha_env:
                chave, _, valor = linha_env.partition("=")
                chave  = chave.strip()
                valor  = valor.strip().strip('"').strip("'")
                # Só define se ainda não estiver no ambiente
                if chave and chave not in os.environ:
                    os.environ[chave] = valor


def consultar_llm(duvida):
    """
    Envia a dúvida para a API do Groq e retorna a resposta gerada.
    Retorna None em caso de falha.
    """
    _carregar_env()

    url     = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        return None

    corpo = json.dumps({
        "model": "llama-3.1-8b-instant",
        "max_tokens": 512,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um assistente educacional do sistema MonitorAê, "
                    "uma plataforma que conecta alunos e monitores de escolas públicas de Pernambuco. "
                    "Responda de forma clara, simples e direta. "
                    "Se a dúvida não for sobre o sistema ou sobre conteúdos escolares, "
                    "informe educadamente que só pode ajudar nesses temas."
                )
            },
            {
                "role": "user",
                "content": duvida
            }
        ]
    }).encode("utf-8")

    requisicao = urllib.request.Request(
        url,
        data=corpo,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=15) as resposta:
            dados = json.load(resposta)
            return dados["choices"][0]["message"]["content"]
    except Exception:
        return None


# ── Salvar sugestão pendente ─────────────────────────────────────────────────

def salvar_sugestao(duvida, resposta_llm):
    """
    Salva a dúvida respondida pela LLM como sugestão pendente,
    aguardando aprovação de um monitor.
    Ignora silenciosamente se a mesma pergunta já foi sugerida antes.
    """
    dados = carregar_sugestoes()

    # Evita duplicatas: não salva se a pergunta já estiver pendente
    ja_existe = any(
        s["pergunta"].strip().lower() == duvida.strip().lower()
        for s in dados["sugestoes"]
    )
    if ja_existe:
        return

    nova_sugestao = {
        "pergunta": duvida,
        "resposta": resposta_llm,
        "aprovada": False
    }
    dados["sugestoes"].append(nova_sugestao)
    salvar_sugestoes(dados)


# ── Tela principal da FAQ ────────────────────────────────────────────────────

class TelaFaq:
    """Tela de perguntas frequentes com busca e suporte da LLM."""

    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario

    def mostrar(self):
        # Loop externo: menu principal do FAQ
        while True:
            cabecalho_app()
            titulo(f"{CADERNO}  FAQ — PERGUNTAS FREQUENTES")

            print(f"  {CINZA}Digite sua dúvida para buscarmos uma resposta.{RESET}\n")

            imprimir_menu(["Buscar resposta", "Ver todas as dúvidas", "---", "Voltar"])
            opcao = pedir_opcao(3)

            if opcao == 3:
                return

            if opcao == 2:
                self._exibir_todas()
                continue

            # Loop interno: fica no campo de busca até o usuário sair (Enter vazio)
            while True:
                cabecalho_app()
                titulo(f"{CADERNO}  FAQ — BUSCAR DÚVIDA")

                print(f"  {CINZA}(Deixe em branco e pressione ENTER para voltar ao menu){RESET}")
                duvida = pedir_texto("Sua dúvida", obrigatorio=False)

                # Enter vazio: sai do loop de busca e volta ao menu do FAQ
                if not duvida.strip():
                    break

                # Dúvida muito genérica: avisa e volta direto para o campo de busca
                if not _filtrar_palavras(duvida):
                    info("Sua dúvida ficou muito genérica. Tente ser mais específico.")
                    pausar()
                    continue

                dados_faq   = carregar_faq()
                perguntas   = dados_faq.get("perguntas", [])
                encontradas = buscar_faq(duvida, perguntas)

                if encontradas:
                    buscar_novamente = self._exibir_resultados(duvida, encontradas)
                else:
                    buscar_novamente = self._sem_resultados(duvida)

                if buscar_novamente:
                    continue  # volta direto para o campo de busca
                else:
                    break     # volta para o menu do FAQ

    def _exibir_todas(self):
        """Exibe todas as perguntas cadastradas na FAQ."""
        dados_faq = carregar_faq()
        perguntas = sorted(dados_faq.get("perguntas", []), key=lambda p: p["pergunta"].lower())

        while True:
            cabecalho_app()
            titulo(f"{CADERNO}  TODAS AS DÚVIDAS")

            if not perguntas:
                info("Nenhuma dúvida cadastrada na FAQ ainda.")
                pausar()
                return

            print(f"  {CINZA}Selecione uma pergunta para ver a resposta:{RESET}\n")

            opcoes_menu = [p["pergunta"] for p in perguntas]
            opcoes_menu.append("---")
            opcoes_menu.append("Voltar")

            print()
            imprimir_menu(opcoes_menu)
            opcao = pedir_opcao(len(opcoes_menu) - 1)

            if opcao == len(perguntas) + 1:
                return

            self._exibir_resposta(perguntas[opcao - 1])

    def _sem_resultados(self, duvida):
        """Sem resultado: oferece buscar de novo, consultar a LLM ou ver todas.
        Retorna True se o usuário quer buscar novamente, False para voltar ao menu."""
        cabecalho_app()
        titulo(f"{CADERNO}  NENHUM RESULTADO ENCONTRADO")

        print(f"  {CINZA}Não encontramos perguntas relacionadas a:{RESET}")
        print(f"  {AMARELO}\"{duvida}\"{RESET}\n")
        linha("─", 50)
        print()

        imprimir_menu([
            "Buscar novamente",
            "Consultar assistente (IA)",
            "Ver todas as dúvidas cadastradas",
            "---",
            "Voltar"
        ])
        opcao = pedir_opcao(4)

        if opcao == 1:
            return True             # vai direto para o campo de busca
        elif opcao == 2:
            self._acionar_llm(duvida)
            return False            # após a LLM, volta ao menu do FAQ
        elif opcao == 3:
            self._exibir_todas()
            return True             # após ver todas, volta para o campo de busca
        else:
            return False            # Voltar: vai para o menu do FAQ

    def _exibir_resultados(self, duvida, encontradas):
        """Exibe as perguntas encontradas e permite o usuário escolher uma."""
        encontradas = sorted(encontradas, key=lambda p: p["pergunta"].lower())
        while True:
            cabecalho_app()
            titulo(f"{CADERNO}  RESULTADOS DA BUSCA")

            print(f"  {CINZA}Encontramos {len(encontradas)} pergunta(s) relacionada(s):{RESET}\n")

            opcoes_menu = [p["pergunta"] for p in encontradas]
            opcoes_menu.append("---")
            opcoes_menu.append("Não encontrei minha dúvida — buscar novamente")
            opcoes_menu.append("Consultar assistente (IA)")
            opcoes_menu.append("Ver todas as dúvidas cadastradas")
            opcoes_menu.append("---")
            opcoes_menu.append("Voltar")

            print()
            imprimir_menu(opcoes_menu)
            n         = len(encontradas)
            opcao     = pedir_opcao(n + 4)

            if opcao <= n:
                self._exibir_resposta(encontradas[opcao - 1])
                # fica no loop: usuário pode escolher outra pergunta dos resultados
            elif opcao == n + 1:
                return True     # buscar novamente: vai direto para o campo de busca
            elif opcao == n + 2:
                self._acionar_llm(duvida)
                return False    # após a LLM, volta ao menu do FAQ
            elif opcao == n + 3:
                self._exibir_todas()
                # fica no loop: usuário pode ainda escolher um resultado
            elif opcao == n + 4:
                return False    # Voltar: vai para o menu do FAQ

    def _exibir_resposta(self, pergunta):
        """Mostra a resposta completa de uma pergunta da FAQ."""
        cabecalho_app()
        titulo(f"{CADERNO}  RESPOSTA")

        print(f"\n  {AMARELO}{NEGRITO}{pergunta['pergunta']}{RESET}\n")
        linha("─", 50)
        print(f"\n  {pergunta['resposta']}\n")
        linha("─", 50)

        pausar()

    def _acionar_llm(self, duvida):
        """Consulta a LLM e oferece salvar a resposta como sugestão."""
        cabecalho_app()
        titulo(f"{RAIO}  CONSULTANDO ASSISTENTE")

        print(f"  {CINZA}Buscando resposta para:{RESET}")
        print(f"  {AMARELO}\"{duvida}\"{RESET}\n")
        print(f"  {CINZA}Aguarde um momento...{RESET}\n")

        resposta = consultar_llm(duvida)

        cabecalho_app()
        titulo(f"{ESTRELA}  RESPOSTA DO ASSISTENTE")

        if not resposta:
            # Fluxo de Erro: LLM indisponível
            erro("O assistente está indisponível no momento. Tente novamente mais tarde.")
            pausar()
            return

        print(f"\n  {AMARELO}{NEGRITO}Sua dúvida:{RESET}")
        print(f"  {CINZA}\"{duvida}\"{RESET}\n")
        linha("─", 50)
        print(f"\n  {resposta}\n")
        linha("─", 50)

        # Oferece salvar como sugestão para revisão do monitor
        print(f"\n  {CINZA}Esta resposta pode ser sugerida para a FAQ.{RESET}")
        print(f"  {CINZA}Um monitor irá revisar e aprovar, se adequada.{RESET}\n")

        imprimir_menu(["Sugerir esta resposta para a FAQ", "---", "Voltar sem sugerir"])
        opcao = pedir_opcao(2)

        if opcao == 1:
            salvar_sugestao(duvida, resposta)
            sucesso("Sugestão enviada! Um monitor irá analisá-la em breve.")
            pausar()
        else:
            pausar()


# ── Tela de aprovação de sugestões (exclusiva para Monitores) ────────────────

class TelaAprovarSugestoes:
    """Permite que monitores aprovem ou rejeitem sugestões enviadas à FAQ."""

    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario

    def mostrar(self):
        while True:
            cabecalho_app()
            titulo(f"{CADERNO}  SUGESTÕES PARA A FAQ")

            dados     = carregar_sugestoes()
            pendentes = [s for s in dados["sugestoes"] if not s.get("aprovada")]

            if not pendentes:
                info("Nenhuma sugestão pendente no momento.")
                pausar()
                return

            print(f"  {AMARELO}Total de sugestões pendentes: {len(pendentes)}{RESET}\n")

            for i, s in enumerate(pendentes, start=1):
                linha("─", 50)
                print(f"\n  {AMARELO}{NEGRITO}[{i}] Pergunta:{RESET} {s['pergunta']}")
                print(f"\n  {CINZA}Resposta da LLM:{RESET}")
                print(f"  {s['resposta']}\n")

            linha("─", 50)
            print()

            opcoes_menu = [f"Analisar sugestão {i}" for i in range(1, len(pendentes) + 1)]
            opcoes_menu.append("---")
            opcoes_menu.append("Voltar")

            imprimir_menu(opcoes_menu)
            opcao = pedir_opcao(len(opcoes_menu) - 1)

            if opcao == len(pendentes) + 1:
                return

            self._analisar_sugestao(pendentes, opcao - 1, dados)

    def _analisar_sugestao(self, pendentes, indice, dados_completos):
        """Permite aprovar, editar pergunta ou resposta, ou rejeitar uma sugestão específica."""
        original = pendentes[indice]
        sugestao = dict(original)  # cópia para não alterar a lista original

        cabecalho_app()
        titulo(f"{CADERNO}  ANALISAR SUGESTÃO")

        print(f"\n  {AMARELO}{NEGRITO}Pergunta:{RESET} {sugestao['pergunta']}\n")
        linha("─", 50)
        print(f"\n  {CINZA}Resposta:{RESET}")
        print(f"  {sugestao['resposta']}\n")
        linha("─", 50)

        print()
        imprimir_menu([
            "Aceitar pergunta e revisar resposta",
            "Editar pergunta e revisar resposta",
            "Rejeitar e remover",
            "---",
            "Voltar"
        ])
        opcao = pedir_opcao(4)

        if opcao == 4:
            return

        if opcao == 3:
            dados_completos["sugestoes"] = [
                s for s in dados_completos["sugestoes"]
                if not (s["pergunta"] == original["pergunta"] and s["resposta"] == original["resposta"])
            ]
            salvar_sugestoes(dados_completos)
            info("Sugestão rejeitada e removida.")
            pausar()
            return

        if opcao == 2:
            cabecalho_app()
            titulo(f"{CADERNO}  EDITAR PERGUNTA")

            print(f"\n  {CINZA}Pergunta atual:{RESET}")
            print(f"  {AMARELO}{sugestao['pergunta']}{RESET}\n")
            print(f"  {CINZA}Digite a versão corrigida (Enter para manter a original):{RESET}")

            nova_pergunta = pedir_texto("Nova pergunta", obrigatorio=False).strip()

            if nova_pergunta:
                sugestao["pergunta"] = nova_pergunta
                sucesso("Pergunta atualizada!")
            else:
                info("Pergunta mantida como estava.")

        # Segundo fluxo: avaliar resposta após a pergunta ter sido aceita/editada
        cabecalho_app()
        titulo(f"{CADERNO}  REVISAR RESPOSTA")

        print(f"\n  {AMARELO}{NEGRITO}Pergunta:{RESET} {sugestao['pergunta']}\n")
        linha("─", 50)
        print(f"\n  {CINZA}Resposta atual:{RESET}")
        print(f"  {sugestao['resposta']}\n")
        linha("─", 50)

        print()
        imprimir_menu([
            "Aceitar resposta e adicionar à FAQ",
            "Editar resposta e aprovar",
            "Rejeitar e remover",
            "---",
            "Voltar"
        ])
        opcao_resposta = pedir_opcao(4)

        if opcao_resposta == 4:
            return

        if opcao_resposta == 3:
            dados_completos["sugestoes"] = [
                s for s in dados_completos["sugestoes"]
                if not (s["pergunta"] == original["pergunta"] and s["resposta"] == original["resposta"])
            ]
            salvar_sugestoes(dados_completos)
            info("Sugestão rejeitada e removida.")
            pausar()
            return

        if opcao_resposta == 2:
            cabecalho_app()
            titulo(f"{CADERNO}  EDITAR RESPOSTA")

            print(f"\n  {CINZA}Resposta atual:{RESET}")
            print(f"  {sugestao['resposta']}\n")
            print(f"  {CINZA}Digite a versão simplificada ou corrigida (Enter para manter a original):{RESET}")

            nova_resposta = pedir_texto("Nova resposta", obrigatorio=False).strip()

            if nova_resposta:
                sugestao["resposta"] = nova_resposta
                sucesso("Resposta atualizada!")
            else:
                info("Resposta mantida como estava.")

        # Aprova e adiciona à FAQ
        dados_completos["sugestoes"] = [
            s for s in dados_completos["sugestoes"]
            if not (s["pergunta"] == original["pergunta"] and s["resposta"] == original["resposta"])
        ]
        dados_faq = carregar_faq()
        novo_id = len(dados_faq["perguntas"]) + 1
        nova_entrada = {
            "id": novo_id,
            "pergunta": sugestao["pergunta"],
            "resposta": sugestao["resposta"]
        }
        dados_faq["perguntas"].append(nova_entrada)
        salvar_faq(dados_faq)
        salvar_sugestoes(dados_completos)
        sucesso("Sugestão aprovada e adicionada à FAQ!")

        if opcao == 1:
            # Aprova: adiciona à FAQ sem palavras-chave (busca por texto direto)
            dados_faq = carregar_faq()
            novo_id   = len(dados_faq["perguntas"]) + 1
            nova_entrada = {
                "id": novo_id,
                "pergunta": sugestao["pergunta"],
                "resposta": sugestao["resposta"]
            }
            dados_faq["perguntas"].append(nova_entrada)
            salvar_faq(dados_faq)
            salvar_sugestoes(dados_completos)
            sucesso("Sugestão aprovada e adicionada à FAQ!")

        elif opcao == 3:
            salvar_sugestoes(dados_completos)
            info("Sugestão rejeitada e removida.")

        pausar()
