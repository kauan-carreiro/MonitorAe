from utils.terminal import (
    cabecalho_app, linha,
    imprimir_menu, pedir_opcao,
    AMARELO, CINZA, RESET, NEGRITO
)
from utils.emojis import (
    ACENO, PESSOA, LUPA, ESCOLA, PORTA, LIVRO, CADERNO, AVISO, DADO
)
from telas.perfil          import TelaPerfil
from telas.monitores       import TelaMonitores
from telas.alunos_proximos import TelaAlunosProximos
from telas.biblioteca      import TelaBiblioteca
from telas.faq             import TelaFaq, TelaAprovarSugestoes
from telas.simulado        import TelaSimulado

class TelaMenu:
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario  # dados do usuário logado

    def mostrar(self):
        """Loop do menu principal."""
        while True:
            cabecalho_app()

            # Saudação personalizada com nome do usuário e tipo (Aluno ou Monitor)
            primeiro_nome = self.usuario.get("nome", "Usuário").split()[0]
            tipo          = self.usuario.get("tipo", "Aluno")

            print(f"  {AMARELO}{NEGRITO}Olá, {primeiro_nome}! {ACENO}{RESET}")
            print(f"  {CINZA}Você está logado como {tipo}.{RESET}")
            print(f"  {CINZA}O que deseja fazer hoje?{RESET}\n")

            linha()

            # O monitor vê uma opção extra de aprovar sugestões da FAQ e outra de conversas
            if tipo == "Monitor":
                imprimir_menu([
                    f"{PESSOA}  Meu Perfil",
                    f"{LUPA}  Monitores",
                    f"{ESCOLA}  Alunos Próximos (mesma escola)",
                    f"{LIVRO}  Biblioteca de Questões",
                    f"{DADO}  Simulado",
                    f"{CADERNO}  FAQ",
                    f"{AVISO}  Aprovar Sugestões da FAQ",
                    f"💬  Minhas Conversas",
                    "---",
                    f"{PORTA}  Sair da conta"
                ])
                opcao = pedir_opcao(9)   # 9 opções (1 a 9)
            else:
                imprimir_menu([
                    f"{PESSOA}  Meu Perfil",
                    f"{LUPA}  Monitores",
                    f"{ESCOLA}  Alunos Próximos (mesma escola)",
                    f"{LIVRO}  Biblioteca de Questões",
                    f"{DADO}  Simulado",
                    f"{CADERNO}  FAQ",
                    "---",
                    f"{PORTA}  Sair da conta"
                ])
                opcao = pedir_opcao(7)   # 7 opções para aluno

            if opcao == 1:
                TelaPerfil(self.router, self.usuario).mostrar()

                # Se a conta foi deletada, o router terá ido para "inicio"
                if self.router.tela_atual != "menu":
                    return

            elif opcao == 2:
                TelaMonitores(self.router, self.usuario).mostrar()

            elif opcao == 3:
                TelaAlunosProximos(self.router, self.usuario).mostrar()

            elif opcao == 4:
                TelaBiblioteca(self.router, self.usuario).mostrar()

            elif opcao == 5:
                TelaSimulado(self.router, self.usuario).mostrar()

            elif opcao == 6:
                TelaFaq(self.router, self.usuario).mostrar()

            elif opcao == 7:
                if tipo == "Monitor":
                    # Monitor: opção 7 é "Aprovar Sugestões da FAQ"
                    TelaAprovarSugestoes(self.router, self.usuario).mostrar()
                else:
                    # Aluno: opção 7 é "Sair da conta"
                    self.router.ir_para("inicio")
                    return

            elif opcao == 8:
                if tipo == "Monitor":
                    # Monitor: opção 8 é "Minhas Conversas"
                    from telas.lista_conversas import TelaListaConversas
                    TelaListaConversas(self.router, self.usuario).mostrar()
                else:
                    # Aluno não chega aqui (só tem 7 opções)
                    pass

            elif opcao == 9:
                # Monitor: opção 9 é "Sair da conta"
                self.router.ir_para("inicio")
                return