# =============================================================================
# validacoes/regras.py
# =============================================================================
# Este arquivo concentra TODAS as regras de validação do sistema.
# Assim fica fácil de encontrar e alterar qualquer restrição.
#
# Como funciona:
#   - Cada função recebe um valor e retorna True se estiver OK,
#     ou uma mensagem de erro (string) se estiver errado.
#   - Depois de chamar a função, basta ecar: if resultado != True: print(erro)
# =============================================================================

import re   # módulo para trabalhar com expressões regulares
import json
import os

# ── Listas de opções permitidas ──────────────────────────────────────────────
# Só essas matérias são aceitas para monitores
MATERIAS_PERMITIDAS = ["Matemática", "Português"]

# Só essas escolas são aceitas no cadastro
ESCOLAS_PERMITIDAS = [
    "EREM Edson Moury Fernandes",
    "EREM Adelaide Pessoa Câmara",
    "EREM Cabo De Santo Agostinho",
    "EREM Diário de Pernambuco",
    "EREM Justino Ferreira Gomes",
]


# ── Validação de nome ────────────────────────────────────────────────────────
def validar_nome(nome):
    """
    Verifica se o nome é válido.
    Regras:
      - Não pode estar vazio
      - Deve ter pelo menos 3 caracteres
      - Não pode conter números
    """
    if not nome or not nome.strip():
        return "O nome não pode estar vazio."
    if len(nome.strip()) < 3:
        return "O nome deve ter pelo menos 3 caracteres."
    if any(caractere.isdigit() for caractere in nome):
        # isdigit() retorna True se o caractere for um dígito (0-9)
        return "O nome não pode conter números."
    return True


# ── Validação de e-mail ──────────────────────────────────────────────────────
def validar_email(email):
    """
    Verifica se o e-mail tem um formato válido.
    Usa uma 'expressão regular' (regex) para checar o padrão:
      texto@texto.texto
    """
    if not email or not email.strip():
        return "O e-mail não pode estar vazio."
    
    # O padrão abaixo verifica se o e-mail tem o formato correto
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(padrao, email):
        return "E-mail inválido. Use o formato: exemplo@email.com"
    return True


# ── Validação de senha ───────────────────────────────────────────────────────
def validar_senha(senha):
    """
    Verifica se a senha é forte o suficiente.
    Regras:
      - Mínimo 6 caracteres
      - Pelo menos um número
      - Pelo menos uma letra maiúscula
      - Pelo menos um caractere especial
    """
    if not senha:
        return "A senha não pode estar vazia."
    if len(senha) < 6:
        return "A senha deve ter pelo menos 6 caracteres."
    if not any(c.isdigit() for c in senha):
        return "A senha deve conter pelo menos um número."
    if not any(c.isupper() for c in senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    caracteres_especiais = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/"
    if not any(c in caracteres_especiais for c in senha):
        return "A senha deve conter pelo menos um caractere especial (!@#$%...)."
    return True


# ── Validação de matéria ─────────────────────────────────────────────────────
def validar_materia(materia):
    """
    Verifica se a matéria escolhida está na lista de opções permitidas.
    Só aceitamos 'Matemática' ou 'Português'.
    """
    if materia not in MATERIAS_PERMITIDAS:
        return f"Matéria inválida. Escolha entre: {', '.join(MATERIAS_PERMITIDAS)}"
    return True


# ── Validação de escola ──────────────────────────────────────────────────────
def validar_escola(escola):
    """
    Verifica se a escola escolhida está na lista de escolas cadastradas.
    """
    if escola not in ESCOLAS_PERMITIDAS:
        return f"Escola não reconhecida. Escolha uma das opções disponíveis."
    return True


# ── Validação de ID de monitor ───────────────────────────────────────────────
def validar_id_monitor(id_digitado):
    """
    Verifica se o ID de monitor existe no arquivo de IDs válidos.
    O arquivo fica em: data/ids_validos.json
    """
    # Monta o caminho até o arquivo de IDs
    # os.path.dirname(__file__) pega a pasta onde este arquivo está
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta_atual, "..", "data", "ids_validos.json")
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if id_digitado in dados["ids"]:
            return True
        else:
            return "ID de monitoria inválido. Verifique o ID fornecido pela instituição."
    except FileNotFoundError:
        return "Arquivo de IDs não encontrado. Contate o administrador."


# ── Verificação de campos obrigatórios ──────────────────────────────────────
def campos_vazios(dicionario, campos_ignorar=None):
    """
    Recebe um dicionário com os dados do formulário e verifica
    se algum campo está vazio.
    """
    if campos_ignorar is None:
        campos_ignorar = []
    
    for chave, valor in dicionario.items():
        if chave in campos_ignorar:
            continue  # pula este campo
        if not str(valor).strip():
            # Formata o nome do campo de forma mais amigável
            nome_amigavel = chave.replace("_", " ").capitalize()
            return f"O campo '{nome_amigavel}' não pode estar vazio."
    return True
