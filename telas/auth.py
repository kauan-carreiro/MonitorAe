from utils.terminal import (
    cabecalho_app, titulo,
    imprimir_menu, pedir_opcao, pedir_texto,
    escolher_da_lista, sucesso, erro, pausar,
    CINZA, RESET
)
from utils.usuarios import (
    adicionar_usuario, buscar_usuario, buscar_por_email, atualizar_senha
)
from validacoes.validadores import (
    validar_nome, validar_email, validar_senha,
    validar_id_monitor,
    MATERIAS_PERMITIDAS, ESCOLAS_PERMITIDAS
)
 
 
# =============================================================================
# TELA DE LOGIN
# =============================================================================
 
class TelaLogin:
    
    def __init__(self, router):
        self.router = router
    
    def mostrar(self):
        """
        Exibe a tela de login e processa a escolha do usuário.
        """
        cabecalho_app()
        titulo("🔐  ENTRAR NA CONTA")
        
        print(f"\n  {CINZA}Escolha seu tipo de perfil:{RESET}\n")
        imprimir_menu(["Aluno", "Monitor", "---", "Voltar"])
        
        opcao = pedir_opcao(3)
        
        if opcao == 1:
            self._fazer_login("Aluno")
        elif opcao == 2:
            self._fazer_login("Monitor")
        elif opcao == 3:
            return  # Volta para a tela inicial
    
    def _fazer_login(self, tipo):
        """
        Realiza o login para o tipo de usuário especificado.
        """
        cabecalho_app()
        titulo(f"🔐  LOGIN — {tipo.upper()}")
        
        # Coleta os dados
        email = pedir_texto("E-mail")
        senha = pedir_texto("Senha", senha=True)
        
        # ID extra para monitor
        id_monitor = None
        if tipo == "Monitor":
            id_monitor = pedir_texto("ID de Monitor")
        
        # Tenta encontrar o usuário
        usuario = buscar_usuario(email, senha)
        
        if not usuario:
            erro("E-mail ou senha incorretos.")
            pausar()
            return
        
        if usuario.get("tipo") != tipo:
            erro(f"Este e-mail não está cadastrado como {tipo}.")
            pausar()
            return
        
        # Valida ID do monitor
        if tipo == "Monitor":
            if usuario.get("id") != id_monitor:
                erro("ID de monitor incorreto.")
                pausar()
                return
        
        sucesso(f"Bem-vindo(a), {usuario['nome'].split()[0]}!")
        pausar("  Pressione ENTER para entrar no sistema...")
        
        # Navega para o menu principal, passando os dados do usuário logado
        self.router.ir_para("menu", usuario=usuario)
 
 
# =============================================================================
# TELA DE CADASTRO
# =============================================================================
 
class TelaCadastro:
    def __init__(self, router):
        self.router = router
    
    def mostrar(self):
        """
        Exibe o menu de cadastro (Aluno, Monitor ou Voltar).
        """
        cabecalho_app()
        titulo("📝  CRIAR CONTA")
        
        print(f"\n  {CINZA}Qual tipo de conta deseja criar?{RESET}\n")
        imprimir_menu(["Aluno", "Monitor", "---", "Voltar"])
        
        opcao = pedir_opcao(3)
        
        if opcao == 1:
            self._cadastrar_aluno()
        elif opcao == 2:
            self._cadastrar_monitor()
        elif opcao == 3:
            return  # Volta
    
    def _cadastrar_aluno(self):
        """
        Coleta os dados e valida para cadastro de Aluno.
        """
        cabecalho_app()
        titulo("📝  CADASTRO — ALUNO")
        
        print(f"  {CINZA}Preencha os campos abaixo. Todos são obrigatórios.{RESET}\n")
        
        # ── Nome ──────────────────────────────────────────────────────
        while True:
            nome = pedir_texto("Nome completo")
            resultado = validar_nome(nome)
            if resultado is True:
                break
            erro(resultado)
        
        # ── Escola ────────────────────────────────────────────────────
        print()
        escola = escolher_da_lista("Instituição de ensino:", ESCOLAS_PERMITIDAS)
        if not escola:
            return  # Usuário cancelou
        
        # ── E-mail ────────────────────────────────────────────────────
        while True:
            email = pedir_texto("E-mail")
            resultado = validar_email(email)
            if resultado is True:
                break
            erro(resultado)
        
        # ── Senha ─────────────────────────────────────────────────────
        self._mostrar_regras_senha()
        
        while True:
            senha = pedir_texto("Senha", senha=True)
            resultado = validar_senha(senha)
            if resultado is True:
                break
            erro(resultado)
        
        while True:
            confirmar_senha = pedir_texto("Confirmar senha", senha=True)
            if senha == confirmar_senha:
                break
            erro("As senhas não coincidem. Tente novamente.")
        
        # ── Montar dicionário do usuário ──────────────────────────────
        novo_usuario = {
            "tipo": "Aluno",
            "nome": nome.strip(),
            "escola": escola,
            "email": email.strip().lower(),
            "senha": senha
        }
        
        # ── Salvar ────────────────────────────────────────────────────
        resultado = adicionar_usuario(novo_usuario)
        if resultado is True:
            sucesso("Conta criada com sucesso! Agora faça login.")
        else:
            erro(resultado)
        
        pausar()
    
    def _cadastrar_monitor(self):
        """
        Coleta os dados e valida para cadastro de Monitor.
        Além dos campos do Aluno, o monitor precisa de: matéria e ID.
        """
        cabecalho_app()
        titulo("📝  CADASTRO — MONITOR")
        
        print(f"  {CINZA}Preencha os campos abaixo. Todos são obrigatórios.{RESET}\n")
        
        # ── Nome ──────────────────────────────────────────────────────
        while True:
            nome = pedir_texto("Nome completo")
            resultado = validar_nome(nome)
            if resultado is True:
                break
            erro(resultado)
        
        # ── Escola ────────────────────────────────────────────────────
        print()
        escola = escolher_da_lista("Instituição de ensino:", ESCOLAS_PERMITIDAS)
        if not escola:
            return
        
        # ── Matéria ───────────────────────────────────────────────────
        print()
        materia = escolher_da_lista("Matéria que você monitora:", MATERIAS_PERMITIDAS)
        if not materia:
            return
        
        # ── ID de Monitor ─────────────────────────────────────────────
        print(f"\n  {CINZA}O ID de Monitor é fornecido pela instituição.{RESET}")
        while True:
            id_monitor = pedir_texto("ID de Monitor")
            resultado = validar_id_monitor(id_monitor)
            if resultado is True:
                break
            erro(resultado)
        
        # ── E-mail ────────────────────────────────────────────────────
        while True:
            email = pedir_texto("E-mail")
            resultado = validar_email(email)
            if resultado is True:
                break
            erro(resultado)
        
        # ── Senha ─────────────────────────────────────────────────────
        self._mostrar_regras_senha()
        
        while True:
            senha = pedir_texto("Senha", senha=True)
            resultado = validar_senha(senha)
            if resultado is True:
                break
            erro(resultado)
        
        while True:
            confirmar_s = pedir_texto("Confirmar senha", senha=True)
            if senha == confirmar_s:
                break
            erro("As senhas não coincidem. Tente novamente.")
        
        # ── Montar dicionário ─────────────────────────────────────────
        novo_usuario = {
            "tipo": "Monitor",
            "nome": nome.strip(),
            "escola": escola,
            "materia": materia,
            "id": id_monitor.strip(),
            "email": email.strip().lower(),
            "senha": senha
        }
        
        resultado = adicionar_usuario(novo_usuario)
        if resultado is True:
            sucesso("Conta de monitor criada com sucesso! Agora faça login.")
        else:
            erro(resultado)
        
        pausar()
    
    def _mostrar_regras_senha(self):
        """
        Exibe as regras de senha antes de pedir que o usuário crie uma.
        """
        print(f"\n  {CINZA}Regras da senha:{RESET}")
        print(f"  {CINZA}  • Mínimo de 6 caracteres{RESET}")
        print(f"  {CINZA}  • Pelo menos um número{RESET}")
        print(f"  {CINZA}  • Pelo menos uma letra maiúscula{RESET}")
        print(f"  {CINZA}  • Pelo menos um caractere especial (!@#$%...){RESET}\n")
 
 
# =============================================================================
# TELA DE REDEFINIÇÃO DE SENHA
# =============================================================================
 
class TelaRedefinirSenha:
    """
    Permite ao usuário redefinir sua senha.
    Neste sistema, a verificação é feita pelo e-mail + nome completo
    (sem envio de e-mail real, pois é um sistema local).
    """
    
    def __init__(self, router):
        self.router = router
    
    def mostrar(self):
        """
        Exibe o fluxo de redefinição de senha.
        """
        cabecalho_app()
        titulo("🔑  REDEFINIR SENHA")
        
        print(f"  {CINZA}Para redefinir sua senha, confirme seus dados.{RESET}\n")
        
        # Pede o e-mail
        email = pedir_texto("E-mail cadastrado")
        
        # Verifica se o e-mail existe
        usuario = buscar_por_email(email)
        if not usuario:
            erro("Nenhuma conta encontrada com este e-mail.")
            pausar()
            return
        
        # Confirmação pelo nome (evita que qualquer um redefina a senha de outro)
        nome_digitado = pedir_texto("Nome completo (para confirmação)")
        
        # Compara ignorando maiúsculas/minúsculas e espaços extras
        if nome_digitado.strip().lower() != usuario["nome"].strip().lower():
            erro("Nome não confere com o cadastro.")
            pausar()
            return
        
        # Pede a nova senha
        print(f"\n  {CINZA}Crie uma nova senha forte:{RESET}")
        print(f"  {CINZA}  • Mínimo 6 caracteres, 1 número, 1 maiúscula, 1 especial{RESET}\n")
        
        while True:
            nova_senha = pedir_texto("Nova senha", senha=True)
            resultado = validar_senha(nova_senha)
            if resultado is True:
                break
            erro(resultado)
        
        while True:
            confirmar_s = pedir_texto("Confirmar nova senha", senha=True)
            if nova_senha == confirmar_s:
                break
            erro("As senhas não coincidem.")
        
        # Atualiza no arquivo
        atualizar_senha(email, nova_senha)
        sucesso("Senha redefinida com sucesso! Faça login com a nova senha.")
        pausar()
    