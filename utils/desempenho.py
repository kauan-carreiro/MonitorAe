import json
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DESEMPENHO = os.path.join(PASTA_ATUAL, "..", "data", "desempenho.json")

def carregar_desempenho():
    if not os.path.exists(CAMINHO_DESEMPENHO):
        return {}
    with open(CAMINHO_DESEMPENHO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_desempenho(dados):
    with open(CAMINHO_DESEMPENHO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def inicializar_estatisticas_usuario(email):
    return {
        "total_questoes": 0,
        "total_acertos": 0,
        "por_assunto": {}
    }

def registrar_simulado(email, questoes_resultados):
    dados = carregar_desempenho()
    if email not in dados:
        dados[email] = inicializar_estatisticas_usuario(email)
    
    stats = dados[email]
    total_questoes = len(questoes_resultados)
    total_acertos = sum(1 for q in questoes_resultados if q["acertou"])
    
    stats["total_questoes"] += total_questoes
    stats["total_acertos"] += total_acertos
    
    for q in questoes_resultados:
        chave_assunto = f"{q['materia']} - {q['descritor_chave']} - {q['descritor_nome']}"
        if chave_assunto not in stats["por_assunto"]:
            stats["por_assunto"][chave_assunto] = {"acertos": 0, "erros": 0}
        if q["acertou"]:
            stats["por_assunto"][chave_assunto]["acertos"] += 1
        else:
            stats["por_assunto"][chave_assunto]["erros"] += 1
    
    salvar_desempenho(dados)

def obter_desempenho_usuario(email):
    dados = carregar_desempenho()
    return dados.get(email, inicializar_estatisticas_usuario(email))