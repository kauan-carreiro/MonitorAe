import json
import os

# =============================================================================
# Responsável por todas as operações com o arquivo de avaliações.
# Aqui ficam as funções de: carregar, salvar e calcular média das avaliações.
# =============================================================================

PASTA_ATUAL       = os.path.dirname(os.path.abspath(__file__))
CAMINHO_AVALIACOES = os.path.join(PASTA_ATUAL, "..", "data", "avaliacoes.json")


def carregar_avaliacoes():
    """
    Lê o arquivo avaliacoes.json e retorna o conteúdo como dicionário Python.
    Se o arquivo não existir, retorna um dicionário vazio com a chave 'avaliacoes'.
    """
    if not os.path.exists(CAMINHO_AVALIACOES):
        return {"avaliacoes": []}

    with open(CAMINHO_AVALIACOES, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_avaliacoes(dados):
    """
    Recebe o dicionário com todas as avaliações e salva no arquivo.
    """
    with open(CAMINHO_AVALIACOES, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def buscar_avaliacao(email_avaliador, email_monitor):
    """
    Verifica se o avaliador já avaliou esse monitor.
    Retorna a avaliação encontrada ou None.
    """
    dados = carregar_avaliacoes()

    for av in dados["avaliacoes"]:
        mesmo_avaliador = av["email_avaliador"].lower() == email_avaliador.lower()
        mesmo_monitor   = av["email_monitor"].lower()   == email_monitor.lower()
        if mesmo_avaliador and mesmo_monitor:
            return av

    return None


def registrar_avaliacao(email_avaliador, email_monitor, nota):
    """
    Salva ou atualiza a avaliação de um monitor.
    Se o avaliador já avaliou esse monitor antes, a nota é substituída.
    Retorna True em caso de sucesso.
    """
    dados = carregar_avaliacoes()

    # Remove a avaliação anterior desse par avaliador/monitor, se existir
    dados["avaliacoes"] = [
        av for av in dados["avaliacoes"]
        if not (
            av["email_avaliador"].lower() == email_avaliador.lower()
            and av["email_monitor"].lower() == email_monitor.lower()
        )
    ]

    dados["avaliacoes"].append({
        "email_avaliador": email_avaliador,
        "email_monitor":   email_monitor,
        "nota":            nota
    })

    salvar_avaliacoes(dados)
    return True


def calcular_media(email_monitor):
    """
    Calcula a média aritmética de todas as notas recebidas por um monitor.
    Retorna a média como float, ou None se o monitor não tiver avaliações.
    """
    dados = carregar_avaliacoes()

    notas = [
        av["nota"] for av in dados["avaliacoes"]
        if av["email_monitor"].lower() == email_monitor.lower()
    ]

    if not notas:
        return None

    return sum(notas) / len(notas)
