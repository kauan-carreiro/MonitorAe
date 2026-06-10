from utils.usuarios    import listar_monitores
from utils.avaliacoes  import buscar_avaliacao, registrar_avaliacao, calcular_media
from validacoes.validadores import MATERIAS_PERMITIDAS, ESCOLAS_PERMITIDAS
from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao, pedir_texto,
    escolher_da_lista, info, sucesso, erro, pausar,
    AMARELO, CINZA, AZUL, VERDE, RESET, NEGRITO
)
from utils.emojis import (
    LUPA, ESCOLA, CADERNO, ESTRELA
)

class TelaMonitores:
    """Exibe todos os monitores cadastrados com opção de filtrar e avaliar."""
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario

    def mostrar(self):
        """Loop principal: exibe filtros e lista de monitores."""
        filtro_materia = None
        filtro_escola  = None
        filtro_nome    = None

        while True:
            cabecalho_app()
            titulo(f"{LUPA}  MONITORES CADASTRADOS")

            todos_monitores = listar_monitores()
            resultado = self._aplicar_filtros(todos_monitores, filtro_materia, filtro_escola, filtro_nome)

            self._exibir_filtros_ativos(filtro_materia, filtro_escola, filtro_nome)
            self._exibir_monitores(resultado)

            print()
            imprimir_menu([
                "Selecionar monitor",
                "Filtrar por Matéria",
                "Filtrar por Escola",
                "Buscar por Nome",
                "Limpar Filtros",
                "---",
                "Voltar"
            ])

            opcao = pedir_opcao(5)

            if opcao == 1:
                self._selecionar_monitor(resultado)

            elif opcao == 2:
                escolha = escolher_da_lista("Filtrar por matéria:", MATERIAS_PERMITIDAS)
                if escolha:
                    filtro_materia = escolha

            elif opcao == 3:
                escolha = escolher_da_lista("Filtrar por escola:", ESCOLAS_PERMITIDAS)
                if escolha:
                    filtro_escola = escolha

            elif opcao == 4:
                nome = pedir_texto("Buscar por nome (parte do nome)", obrigatorio=False)
                filtro_nome = nome.strip() if nome.strip() else None

            elif opcao == 5:
                filtro_materia = None
                filtro_escola  = None
                filtro_nome    = None
                info("Filtros removidos.")

            elif opcao == 0:
                return

    def _selecionar_monitor(self, monitores):
        """Pede o número do monitor e abre o perfil dele."""
        if not monitores:
            info("Nenhum monitor disponível para selecionar.")
            pausar()
            return

        numero = pedir_texto(f"Digite o número do monitor (1 a {len(monitores)})", obrigatorio=False)

        if not numero.strip():
            return

        if not numero.strip().isdigit():
            erro("Digite apenas o número do monitor.")
            pausar()
            return

        indice = int(numero.strip()) - 1

        if indice < 0 or indice >= len(monitores):
            erro(f"Número inválido. Escolha entre 1 e {len(monitores)}.")
            pausar()
            return

        self._ver_perfil(monitores[indice])

    def _ver_perfil(self, monitor):
        """Exibe o perfil completo do monitor com nota média, opção de avaliar e (se for aluno) iniciar conversa."""
        while True:
            cabecalho_app()
            titulo(f"{ESTRELA}  PERFIL DO MONITOR")

            nome    = monitor.get("nome",    "—")
            escola  = monitor.get("escola",  "—")
            materia = monitor.get("materia", "—")
            email   = monitor.get("email",   "")

            media = calcular_media(email)
            if media is None:
                nota_exibida = f"{CINZA}Sem avaliações ainda{RESET}"
            else:
                nota_exibida = f"{AMARELO}{NEGRITO}{media:.1f} / 10{RESET}"

            avaliacao_atual = buscar_avaliacao(self.usuario["email"], email)

            print(f"\n  {AMARELO}{NEGRITO}{nome}{RESET}")
            print(f"  {CINZA}{ESCOLA} {escola}{RESET}")
            print(f"  {CINZA}{CADERNO} Matéria: {RESET}{AMARELO}{materia}{RESET}")
            print()
            linha("─", 50)
            print(f"\n  {ESTRELA} Nota média: {nota_exibida}")

            if avaliacao_atual:
                print(f"  {CINZA}Sua avaliação atual: {RESET}{AMARELO}{avaliacao_atual['nota']} / 10{RESET}")

            print()

            # Monta menu conforme o contexto
            opcoes = []
            if avaliacao_atual:
                opcoes.append("Alterar minha avaliação")
            else:
                opcoes.append("Avaliar este monitor")

            # Alunos podem iniciar conversa
            if self.usuario.get("tipo") == "Aluno":
                opcoes.append("Iniciar conversa")

            opcoes += ["---", "Voltar"]

            imprimir_menu(opcoes)
            # Total de opções = tamanho da lista menos 2 (por causa do "---" e "Voltar")
            total_opcoes = len(opcoes) - 2
            opcao = pedir_opcao(total_opcoes)

            # Mapeamento: a opção 0 é sempre "Voltar"
            if opcao == 0:
                return

            # Opção 1: avaliar/alterar avaliação
            if opcao == 1:
                self._avaliar(monitor)

            # Opção 2: iniciar conversa (se existir)
            elif self.usuario.get("tipo") == "Aluno" and opcao == 2:
                from telas.chat import TelaChat
                TelaChat(self.router, self.usuario, monitor).mostrar()

    def _avaliar(self, monitor):
        """Fluxo completo de avaliação de um monitor."""
        email_monitor   = monitor.get("email", "")
        email_avaliador = self.usuario["email"]

        # Erro: usuário tentando se autoavaliar
        if email_avaliador.lower() == email_monitor.lower():
            erro("Você não pode se avaliar.")
            pausar()
            return

        # Restrição: apenas alunos podem avaliar monitores
        if self.usuario.get("tipo") != "Aluno":
            erro("Apenas alunos podem avaliar monitores.")
            pausar()
            return

        # Restrição: aluno só avalia monitores da mesma escola
        if self.usuario.get("escola") != monitor.get("escola"):
            erro("Você só pode avaliar monitores da sua escola.")
            pausar()
            return

        avaliacao_existente = buscar_avaliacao(email_avaliador, email_monitor)

        cabecalho_app()
        titulo(f"{ESTRELA}  AVALIAR MONITOR")

        print(f"\n  Avaliando: {AMARELO}{NEGRITO}{monitor.get('nome', '—')}{RESET}")

        if avaliacao_existente:
            print(f"  {CINZA}Você já avaliou este monitor com nota {AMARELO}{avaliacao_existente['nota']}{CINZA}.")
            print(f"  Ao confirmar, a nota antiga será substituída.{RESET}")

        print()
        linha("─", 50)
        print(f"  {CINZA}(Deixe em branco e pressione ENTER para voltar){RESET}")

        while True:
            nota_digitada = pedir_texto("Digite a nota (0 a 10)", obrigatorio=False)

            # Usuário deixou em branco: cancela
            if not nota_digitada.strip():
                info("Avaliação cancelada.")
                pausar()
                return

            # Valida se é número inteiro
            if not nota_digitada.strip().isdigit():
                erro("Digite apenas um número inteiro entre 0 e 10.")
                continue

            nota = int(nota_digitada.strip())

            # Erro: nota fora do intervalo
            if nota < 0 or nota > 10:
                erro("Nota fora do intervalo. Digite um valor entre 0 e 10.")
                continue

            break

        # Confirmação antes de salvar
        print(f"\n  Nota escolhida: {AMARELO}{NEGRITO}{nota} / 10{RESET}")
        imprimir_menu(["Confirmar avaliação", "---", "Cancelar"])
        opcao = pedir_opcao(2)

        if opcao == 2:
            info("Avaliação cancelada.")
            pausar()
            return

        # Salva a avaliação
        try:
            registrar_avaliacao(email_avaliador, email_monitor, nota)
            sucesso("Obrigado por avaliar!")
        except Exception:
            erro("Falha ao salvar avaliação. Tente novamente.")

        pausar()

    def _aplicar_filtros(self, monitores, materia, escola, nome):
        resultado = []
        for m in monitores:
            if materia and m.get("materia") != materia:
                continue
            if escola and m.get("escola") != escola:
                continue
            if nome and nome.lower() not in m.get("nome", "").lower():
                continue
            resultado.append(m)
        return resultado

    def _exibir_filtros_ativos(self, materia, escola, nome):
        """Mostra quais filtros estão ativos no momento."""
        ativos = []
        if materia:
            ativos.append(f"Matéria: {materia}")
        if escola:
            ativos.append(f"Escola: {escola}")
        if nome:
            ativos.append(f"Nome contém: '{nome}'")

        if ativos:
            print(f"  {AZUL}{LUPA} Filtros ativos: {' | '.join(ativos)}{RESET}")
        else:
            print(f"  {CINZA}(Sem filtros — exibindo todos os monitores){RESET}")

    def _exibir_monitores(self, monitores):
        """Formata e imprime cada monitor da lista com sua nota média."""
        print(f"\n  {AMARELO}Total encontrado: {len(monitores)} monitor(es){RESET}\n")

        if not monitores:
            print(f"  {CINZA}Nenhum monitor encontrado com esses filtros.{RESET}")
            return

        linha("─", 55)
        for i, m in enumerate(monitores, start=1):
            nome    = m.get("nome",    "—")
            escola  = m.get("escola",  "—")
            materia = m.get("materia", "—")
            email   = m.get("email",   "")
            inicial = nome[0].upper() if nome else "?"

            media = calcular_media(email)
            if media is None:
                nota_str = f"{CINZA}sem avaliações{RESET}"
            else:
                nota_str = f"{AMARELO}{media:.1f}/10{RESET}"

            print(f"\n  {AMARELO}{NEGRITO}[{i}] {inicial} — {nome}{RESET}")
            print(f"  {CINZA}    {ESCOLA} {escola}{RESET}")
            print(f"  {CINZA}    {CADERNO} Matéria: {RESET}{AMARELO}{materia}{RESET}")
            print(f"  {CINZA}    {ESTRELA} Nota: {RESET}{nota_str}")
            linha("─", 55)
