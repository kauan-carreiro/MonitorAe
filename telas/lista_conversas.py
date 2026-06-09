from utils.terminal import cabecalho_app, titulo, linha, imprimir_menu, pedir_opcao, pausar, info, AMARELO, CINZA, RESET, NEGRITO
from utils.chat import listar_conversas_ativas_por_monitor, obter_conversa_por_id
from utils.usuarios import buscar_por_email
from telas.chat import TelaChat

class TelaListaConversas:
    def __init__(self, router, usuario):
        self.router = router
        self.usuario = usuario

    def mostrar(self):
        while True:
            cabecalho_app()
            titulo("📬 MINHAS CONVERSAS ATIVAS")
            conversas = listar_conversas_ativas_por_monitor(self.usuario["email"])
            if not conversas:
                info("Nenhuma conversa ativa no momento.")
                pausar()
                return

            print(f"  {CINZA}Selecione uma conversa para abrir:{RESET}\n")
            opcoes = []
            for c in conversas:
                aluno = buscar_por_email(c["aluno_email"])
                nome_aluno = aluno["nome"] if aluno else c["aluno_email"]
                opcoes.append(f"{nome_aluno} ({c['mensagens'][-1]['texto'][:40]}...)" if c["mensagens"] else nome_aluno)
            opcoes.append("---")
            opcoes.append("Voltar")

            imprimir_menu(opcoes)
            opcao = pedir_opcao(len(opcoes) - 1)
            if opcao == len(conversas) + 1:
                return

            conversa = conversas[opcao - 1]
            aluno = buscar_por_email(conversa["aluno_email"])
            if aluno:
                TelaChat(self.router, self.usuario, aluno, conversa["id"]).mostrar()