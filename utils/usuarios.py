import json
import os

# =============================================================================
# Responsável por todas as operações com o arquivo de usuários.
# Aqui ficam as funções de: carregar, salvar, adicionar, buscar e remover usuários.
# =============================================================================

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_USUARIOS = os.path.join(PASTA_ATUAL, "..", "data", "usuarios.json")


def carregar_usuarios():
    """
    Lê o arquivo usuarios.json e retorna o conteúdo como dicionário Python.
    
    Se o arquivo não existir, retorna um dicionário vazio com a chave 'usuarios'.
    """
    if not os.path.exists(CAMINHO_USUARIOS):
        return {"usuarios": []}
    
    with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_usuarios(dados):
    """
    Recebe o dicionário com todos os usuários e salva no arquivo.
    O parâmetro indent=4 faz o arquivo ficar bem formatado.
    ensure_ascii=False permite salvar acentos corretamente.
    """
    with open(CAMINHO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def adicionar_usuario(novo_usuario):
    """
    Adiciona um novo usuário ao sistema.
    Antes de adicionar, verifica se já existe um usuário com o mesmo e-mail.
    Retorna:
      - True -> usuário adicionado com sucesso
      - String de erro -> se o e-mail já estiver cadastrado
    """
    dados = carregar_usuarios()
    
    # Verifica se o e-mail já está em uso
    for usuario in dados["usuarios"]:
        if usuario["email"].lower() == novo_usuario["email"].lower():
            return "Este e-mail já está cadastrado. Tente fazer login."
    
    dados["usuarios"].append(novo_usuario)
    salvar_usuarios(dados)
    return True


def buscar_usuario(email, senha):
    """
    Procura um usuário pelo e-mail e senha.
    Retorna:
      - O dicionário do usuário se encontrar
      - None se não encontrar
    """
    dados = carregar_usuarios()
    
    for usuario in dados["usuarios"]:
        # Compara e-mail (ignorando maiúsculas/minúsculas) e senha
        if usuario["email"].lower() == email.lower() and usuario["senha"] == senha:
            return usuario
    
    return None  # Não encontrou


def buscar_por_email(email):
    """
    Procura um usuário somente pelo e-mail (sem verificar senha).
    Útil para redefinição de senha.
    Retorna o usuário ou None.
    """
    dados = carregar_usuarios()
    
    for usuario in dados["usuarios"]:
        if usuario["email"].lower() == email.lower():
            return usuario
    
    return None


def atualizar_senha(email, nova_senha):
    """
    Atualiza a senha de um usuário identificado pelo e-mail.
    Retorna:
      - True -> senha atualizada com sucesso
      - False -> usuário não encontrado
    """
    dados = carregar_usuarios()
    
    for usuario in dados["usuarios"]:
        if usuario["email"].lower() == email.lower():
            usuario["senha"] = nova_senha
            salvar_usuarios(dados)
            return True
    
    return False


def remover_usuario(email):
    """
    Remove um usuário do sistema pelo e-mail.
    """
    dados = carregar_usuarios()
    lista_original = dados["usuarios"]
    
    # Cria uma nova lista sem o usuário que queremos remover
    nova_lista = [u for u in lista_original if u["email"].lower() != email.lower()]
    
    if len(nova_lista) == len(lista_original):
        return False  # Nenhum usuário foi removido
    
    dados["usuarios"] = nova_lista
    salvar_usuarios(dados)
    return True


def listar_monitores():
    """
    Retorna uma lista com todos os usuários do tipo 'Monitor'.
    """
    dados = carregar_usuarios()
    return [u for u in dados["usuarios"] if u.get("tipo") == "Monitor"]


def listar_alunos():
    """
    Retorna uma lista com todos os usuários do tipo 'Aluno'.
    """
    dados = carregar_usuarios()
    return [u for u in dados["usuarios"] if u.get("tipo") == "Aluno"]


def listar_alunos_mesma_escola(escola, email_atual):
    """
    Retorna alunos que estudam na mesma escola,
    excluindo o próprio usuário logado.
    """
    dados = carregar_usuarios()
    return [
        u for u in dados["usuarios"]
        if u.get("tipo") == "Aluno"
        and u.get("escola") == escola
        and u.get("email", "").lower() != email_atual.lower()
    ]