from utils.terminal import (
    cabecalho_app, linha,
    imprimir_menu, pedir_opcao,
    AMARELO, CINZA, RESET, NEGRITO
)
from utils.emojis import (
    ACENO, PESSOA, LUPA, ESCOLA, PORTA, LIVRO
)
from telas.perfil          import TelaPerfil
from telas.monitores       import TelaMonitores
from telas.alunos_proximos import TelaAlunosProximos
from telas.biblioteca      import TelaBiblioteca
 
 
class TelaMenu:
    """
    Tela principal após o login.
    Mantém o loop enquanto o usuário não sair.
    """
    
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario  # dados do usuário logado
    
    def mostrar(self):
        """
        Loop do menu principal.
        """
        while True:
            cabecalho_app()
            
            # Saudação personalizada — pega só o primeiro nome
            primeiro_nome = self.usuario.get("nome", "Usuário").split()[0]
            tipo          = self.usuario.get("tipo", "Aluno")
            
            print(f"  {AMARELO}{NEGRITO}Olá, {primeiro_nome}! {ACENO}{RESET}")
            print(f"  {CINZA}Você está logado como {tipo}.{RESET}")
            print(f"  {CINZA}O que deseja fazer hoje?{RESET}\n")
            
            linha()
            
            imprimir_menu([
                f"{PESSOA}  Meu Perfil",
                f"{LUPA}  Monitores",
                f"{ESCOLA}  Alunos Próximos (mesma escola)",
                f"{LIVRO}  Biblioteca de Questões",
                "---",
                f"{PORTA}  Sair da conta"
            ])
            
            opcao = pedir_opcao(5)
            
            if opcao == 1:
                TelaPerfil(self.router, self.usuario).mostrar()
                
                # Se a conta foi deletada, o router terá ido para "inicio"
                # checar se ainda estamos logados
                if self.router.tela_atual != "menu":
                    return
            
            elif opcao == 2:
                TelaMonitores(self.router, self.usuario).mostrar()
            
            elif opcao == 3:
                TelaAlunosProximos(self.router, self.usuario).mostrar()
            
            elif opcao == 4:
                TelaBiblioteca(self.router, self.usuario).mostrar()
            
            elif opcao == 5:
                self.router.ir_para("inicio")
                return
            