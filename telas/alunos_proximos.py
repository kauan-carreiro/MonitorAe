from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao,
    info, pausar,
    AMARELO, CINZA, RESET, NEGRITO
)
from utils.emojis import (
    ESCOLA
)
from utils.usuarios import listar_alunos_mesma_escola

class TelaAlunosProximos:
    """Exibe alunos que estudam na mesma escola do usuário logado."""
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario
    
    def mostrar(self):
        cabecalho_app()
        titulo(f"{ESCOLA}  ALUNOS DA MESMA ESCOLA")
        
        escola     = self.usuario.get("escola", "")
        email_meu  = self.usuario.get("email", "")
        
        if not escola:
            info("Sua escola não está cadastrada. Não é possível listar.")
            pausar()
            return
        
        print(f"  {CINZA}Mostrando alunos de: {RESET}{AMARELO}{escola}{RESET}\n")
        
        alunos = listar_alunos_mesma_escola(escola, email_meu)
        
        if not alunos:
            print(f"  {CINZA}Nenhum outro aluno desta escola encontrado.{RESET}")
        else:
            print(f"  {AMARELO}Total: {len(alunos)} aluno(s) encontrado(s){RESET}\n")
            linha("─", 50)
            
            for i, a in enumerate(alunos, start=1):
                nome   = a.get("nome",  "—")
                inicial = nome[0].upper() if nome else "?"
                
                print(f"\n  {NEGRITO}[{i}] {inicial} — {nome}{RESET}")
                print(f"  {CINZA}    {ESCOLA} {escola}{RESET}")
                linha("─", 50)
        
        print()
        imprimir_menu(["Voltar"])
        pedir_opcao(1)
