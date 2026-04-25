from router import Router
from telas.auth import TelaLogin, TelaCadastro, TelaRedefinirSenha
from telas.menu import TelaMenu
from utils.terminal import (
    cabecalho_app, titulo, linha, imprimir_menu,
    pedir_opcao, AMARELO, CINZA, RESET, NEGRITO,
)
from utils.emojis import (
    ACENO, CASA, CHAPEU,
)
 
 
def tela_inicial(router):
    """
    A primeira tela que o usuário vê.
    Opções: Login, Cadastro, Redefinir Senha, Sair.
    
    Esta função fica em loop até que o usuário faça login ou escolha Sair.
    """
    while True:
        cabecalho_app()
        titulo(f"{CASA}  TELA INICIAL")
        
        print(f"  {CINZA}Bem-vindo(a) ao MonitorAê!{RESET}")
        print(f"  {CINZA}Conectando alunos e monitores. {CHAPEU}{RESET}\n")
        
        imprimir_menu([
            "Entrar na conta",
            "Criar conta",
            "Esqueci minha senha",
            "---",
            "Sair do programa"
        ])
        
        opcao = pedir_opcao(4)
        
        if opcao == 1:
            TelaLogin(router).mostrar()
        
        elif opcao == 2:
            TelaCadastro(router).mostrar()
        
        elif opcao == 3:
            TelaRedefinirSenha(router).mostrar()
        
        elif opcao == 4:
            # Encerra o programa
            cabecalho_app()
            print(f"\n  {AMARELO}{NEGRITO}Até logo! {ACENO}{RESET}")
            print(f"  {CINZA}Obrigado por usar o MonitorAê.{RESET}\n")
            linha()
            break
        
        # Após qualquer ação, verifica se o router redirecionou para o menu
       
        if router.tela_atual == "menu" and router.usuario:
            TelaMenu(router, router.usuario).mostrar()
            
            # Quando o TelaMenu retorna, o usuário saiu da conta
            # O router já foi atualizado para "inicio"
            # O loop continua e mostra a tela inicial novamente
 
 
def main():
    """
    Função principal — ponto de entrada do programa.
    Cria o router e inicia a tela inicial.
    """
    router = Router()

    try:
        tela_inicial(router)
    except KeyboardInterrupt:   # Lançado quando o usuário pressiona Ctrl+C
        print(f"\n\n  {AMARELO}Programa encerrado pelo usuário. Até logo! {ACENO}{RESET}\n")
 
 
if __name__ == "__main__":
    main()
