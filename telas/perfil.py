from utils.desempenho import obter_desempenho_usuario
from telas.desempenho_detalhes import TelaDesempenhoDetalhes
from utils.usuarios import remover_usuario
from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao, pedir_texto,
    sucesso, erro, info, pausar, confirmar,
    AMARELO, VERDE, VERMELHO, CINZA, AZUL, RESET, NEGRITO
)
from utils.emojis import (
    PESSOA, ESCOLA, CARTA, CADERNO, CRACHA, GRAFICO, AVISO,
)

class TelaPerfil:
    """
    Exibe o perfil do usuário e opções como deletar conta.
    Recebe o objeto 'usuario' (dicionário) com os dados de quem está logado.
    """
    
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario  # dicionário com os dados do usuário logado
    
    def mostrar(self):
        while True:
            cabecalho_app()
            titulo(f"{PESSOA}  MEU PERFIL")
            
            self._exibir_dados()
            
            print()
            imprimir_menu(["Mais detalhes","Deletar minha conta", "---", "Voltar ao Menu"])
            
            opcao = pedir_opcao(2)
            
            if opcao == 1:
                tela = TelaDesempenhoDetalhes(self.router, self.usuario)
                tela.mostrar()
            elif opcao == 2:
                if self._deletar_conta():
                    return  # Conta deletada, volta para a tela inicia
            elif opcao == 0:
                return
    
    def _exibir_dados(self):

        u = self.usuario
        tipo = u.get("tipo", "Aluno")
        
        # Cor diferente para monitor e aluno
        cor_tipo = AZUL if tipo == "Monitor" else VERDE
        
        print(f"\n  {NEGRITO}{'─' * 45}{RESET}")
        
        # Nome com inicial em destaque
        iniciais = "".join(p[0].upper() for p in u.get("nome", "?").split()[:2])
        print(f"\n  {AMARELO}{NEGRITO}  [ {iniciais} ]  {RESET}{NEGRITO}{u.get('nome', '—')}{RESET}")
        print(f"  {cor_tipo}  {tipo}{RESET}\n")
        
        linha("─", 48)
        
        # Campos
        campos = [
            (f"{CARTA}", "E-mail",    u.get("email",  "—")),
            (f"{ESCOLA}", "Escola",    u.get("escola", "—")),
        ]
        
        # Se for monitor, adiciona matéria e ID
        if tipo == "Monitor":
            campos.append((f"{CADERNO}", "Matéria",   u.get("materia", "—")))
            campos.append((f"{CRACHA}", "ID Monitor", u.get("id", "—")))
        
        for icone, label, valor in campos:
            print(f"  {icone}  {CINZA}{label}:{RESET}  {valor}")
        
        linha("─", 48)
        
        desempenho = obter_desempenho_usuario(self.usuario["email"])
        total_q = desempenho["total_questoes"]
        total_ac = desempenho["total_acertos"]
        percentual = (total_ac / total_q * 100) if total_q > 0 else 0
        print(f"  {CINZA}Questões respondidas:{RESET}  {total_q}")
        print(f"  {CINZA}Taxa de acerto:{RESET}        {percentual:.1f}%")
    
    def _deletar_conta(self):
        """
        Confirma e deleta a conta do usuário.
        Retorna True se a conta foi deletada (para deslogar).
        Retorna False se o usuário cancelou.
        """
        print(f"\n  {VERMELHO}{AVISO}  ATENÇÃO: Esta ação é irreversível!{RESET}")
        print(f"  {CINZA}Sua conta e todos os seus dados serão removidos.{RESET}")
        
        if not confirmar("Tem certeza que deseja deletar sua conta?"):
            info("Operação cancelada.")
            pausar()
            return False
        
        # Segunda confirmação — digitar a senha
        print(f"\n  {CINZA}Digite sua senha para confirmar a exclusão:{RESET}")
        senha_digitada = pedir_texto("Senha", senha=True)
        
        if senha_digitada != self.usuario.get("senha"):
            erro("Senha incorreta. Conta não foi deletada.")
            pausar()
            return False
        
        # Remove do arquivo
        email = self.usuario.get("email", "")
        remover_usuario(email)
        
        sucesso("Conta deletada com sucesso. Até logo!")
        pausar()
        
        # Navega para o login e limpa o usuário
        self.router.ir_para("inicio")
        return True
    
