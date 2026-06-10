from utils.terminal import (
    cabecalho_app, titulo, linha, imprimir_menu, pedir_opcao,
    pedir_texto, info, sucesso, erro, pausar,
    AMARELO, CINZA, RESET, NEGRITO
)
from utils.chat import (
    obter_conversa_por_id, adicionar_mensagem, encerrar_conversa,
    obter_conversa_ativa, criar_conversa, obter_conversa_encerrada
)
from utils.emojis import ACENO, AVISO

class TelaChat:
    def __init__(self, router, usuario, outro_usuario, conversa_id=None):
        self.router = router
        self.usuario = usuario
        self.outro = outro_usuario
        self.eh_monitor = (usuario.get("tipo") == "Monitor")
        self.conversa_id = conversa_id

        if self.conversa_id:
            return

        # Aluno tentando iniciar conversa com monitor
        if not self.eh_monitor:
            # 1º: verifica se existe conversa ATIVA
            ativa = obter_conversa_ativa(usuario["email"], outro_usuario["email"])
            if ativa:
                self.conversa_id = ativa["id"]
                return

            # 2º: verifica se existe conversa ENCERRADA (para avaliação)
            encerrada = obter_conversa_encerrada(usuario["email"], outro_usuario["email"])
            if encerrada:
                # Abre a conversa encerrada (status = encerrada)
                self.conversa_id = encerrada["id"]
                return

            # 3º: nenhuma conversa → cria nova
            self.conversa_id = criar_conversa(usuario["email"], outro_usuario["email"])

        else:
            # Monitor tentando abrir conversa com aluno
            ativa = obter_conversa_ativa(outro_usuario["email"], usuario["email"])
            if ativa:
                self.conversa_id = ativa["id"]
            else:
                # Monitor pode criar conversa com aluno? Por simetria, sim.
                self.conversa_id = criar_conversa(outro_usuario["email"], usuario["email"])

    def mostrar(self):
        conversa = obter_conversa_por_id(self.conversa_id)
        if not conversa:
            erro("Conversa não encontrada.")
            pausar()
            return

        # Se é aluno e conversa está encerrada → fluxo de avaliação
        if not self.eh_monitor and conversa["status"] == "encerrada":
            self._conversa_encerrada_avaliacao(conversa)
            return

        # Se conversa está ativa, segue normalmente
        while True:
            self._exibir_mensagens(conversa)
            print()
            opcoes = ["Enviar mensagem", "Atualizar"]
            if self.eh_monitor:
                opcoes.append("Encerrar conversa")
            opcoes.append("---")
            opcoes.append("Voltar")
            imprimir_menu(opcoes)
            max_opcao = len(opcoes) - 2
            opcao = pedir_opcao(max_opcao)

            if opcao == 0:           # Voltar
                return
            elif opcao == 1:         # Enviar
                texto = pedir_texto("Digite sua mensagem", obrigatorio=False)
                if texto.strip():
                    adicionar_mensagem(self.conversa_id, self.usuario["email"], texto)
            elif opcao == 2:         # Atualizar
                conversa = obter_conversa_por_id(self.conversa_id)
            elif self.eh_monitor and opcao == 3:   # Encerrar
                if self._confirmar_encerramento():
                    encerrar_conversa(self.conversa_id)
                    sucesso("Conversa encerrada.")
                    pausar()
                    return

    def _exibir_mensagens(self, conversa):
        cabecalho_app()
        titulo(f"💬 CHAT com {self.outro['nome'].split()[0]}")
        print(f"  {CINZA}Conversa iniciada em {conversa['criado_em'][:16]}{RESET}")
        if conversa["status"] == "encerrada":
            print(f"  {CINZA}* Conversa encerrada em {conversa['encerrado_em'][:16]} *{RESET}")
        print()
        linha("─", 55)
        for msg in conversa["mensagens"]:
            remetente = "Você" if msg["remetente"] == self.usuario["email"] else self.outro["nome"].split()[0]
            print(f"  {AMARELO}{remetente}:{RESET} {msg['texto']}")
        linha("─", 55)

    def _confirmar_encerramento(self):
        print(f"\n  {AVISO} Tem certeza que deseja encerrar esta conversa?")
        return input(f"  {AMARELO}Digite 's' para confirmar: {RESET}").strip().lower() == 's'

    def _conversa_encerrada_avaliacao(self, conversa):
        """Exibe a conversa encerrada e pergunta se a dúvida foi sanada, depois oferece avaliar e/ou nova conversa."""
        self._exibir_mensagens(conversa)
        print(f"\n  {CINZA}Esta conversa foi encerrada pelo monitor.{RESET}")
        resp = input(f"\n  {AMARELO}O monitor sanou sua dúvida? (s/n): {RESET}").strip().lower()

        if resp in ("s", "sim"):
            sucesso("Que bom! Agradecemos o feedback.")
            print(f"\n  {CINZA}Deseja avaliar o monitor? Você será direcionado ao perfil.{RESET}")
            input(f"  {CINZA}Pressione ENTER para continuar...{RESET}")

            # Reutiliza o método _ver_perfil da TelaMonitores para avaliar
            from telas.monitores import TelaMonitores
            tela_mon = TelaMonitores(self.router, self.usuario)
            tela_mon._ver_perfil(self.outro)
        else:
            info("Que pena! Você pode iniciar uma nova conversa se precisar.")

        # Após avaliação (ou não), oferece iniciar nova conversa
        print()
        opcao = input(f"  {AMARELO}Deseja iniciar uma nova conversa com este monitor? (s/n): {RESET}").strip().lower()
        if opcao in ("s", "sim"):
            # Cria nova conversa
            nova_id = criar_conversa(self.usuario["email"], self.outro["email"])
            self.conversa_id = nova_id
            # Recarrega a tela (agora com conversa ativa)
            self.mostrar()
        else:
            info("Voltando ao menu...")
            pausar()
