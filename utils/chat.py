import json
import os
from datetime import datetime

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CONVERSAS = os.path.join(PASTA_ATUAL, "..", "data", "conversas.json")

def carregar_conversas():
    if not os.path.exists(CAMINHO_CONVERSAS):
        return {"conversas": []}
    with open(CAMINHO_CONVERSAS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_conversas(dados):
    with open(CAMINHO_CONVERSAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def _proximo_id():
    dados = carregar_conversas()
    ids = [c["id"] for c in dados["conversas"]]
    return max(ids) + 1 if ids else 1

def criar_conversa(aluno_email, monitor_email):
    dados = carregar_conversas()
    conversa = {
        "id": _proximo_id(),
        "aluno_email": aluno_email,
        "monitor_email": monitor_email,
        "status": "ativa",
        "criado_em": datetime.now().isoformat(),
        "encerrado_em": None,
        "mensagens": []
    }
    dados["conversas"].append(conversa)
    salvar_conversas(dados)
    return conversa["id"]

def obter_conversa_ativa(aluno_email, monitor_email):
    dados = carregar_conversas()
    for c in dados["conversas"]:
        if c["aluno_email"] == aluno_email and c["monitor_email"] == monitor_email and c["status"] == "ativa":
            return c
    return None

def obter_conversa_por_id(conv_id):
    dados = carregar_conversas()
    for c in dados["conversas"]:
        if c["id"] == conv_id:
            return c
    return None

def adicionar_mensagem(conv_id, remetente_email, texto):
    dados = carregar_conversas()
    for c in dados["conversas"]:
        if c["id"] == conv_id:
            c["mensagens"].append({
                "remetente": remetente_email,
                "texto": texto.strip(),
                "timestamp": datetime.now().isoformat()
            })
            salvar_conversas(dados)
            return True
    return False

def encerrar_conversa(conv_id):
    dados = carregar_conversas()
    for c in dados["conversas"]:
        if c["id"] == conv_id and c["status"] == "ativa":
            c["status"] = "encerrada"
            c["encerrado_em"] = datetime.now().isoformat()
            salvar_conversas(dados)
            return True
    return False

def listar_conversas_ativas_por_monitor(monitor_email):
    dados = carregar_conversas()
    return [c for c in dados["conversas"] if c["monitor_email"] == monitor_email and c["status"] == "ativa"]

def obter_conversa_encerrada(aluno_email, monitor_email):
    """Retorna a conversa mais recente encerrada entre aluno e monitor (ou None)."""
    dados = carregar_conversas()
    encerradas = [
        c for c in dados["conversas"]
        if c["aluno_email"] == aluno_email
        and c["monitor_email"] == monitor_email
        and c["status"] == "encerrada"
    ]
    if not encerradas:
        return None
    # Retorna a mais recente (última encerrada)
    encerradas.sort(key=lambda x: x["encerrado_em"], reverse=True)
    return encerradas[0]
