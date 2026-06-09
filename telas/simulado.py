import json
import os
import random

from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao, pedir_texto,
    escolher_da_lista, erro, sucesso, info, pausar,
    AMARELO, VERDE, VERMELHO, CINZA, RESET, NEGRITO
)
from utils.emojis import (
    LIVRO, CADERNO, ROSTO_FELIZ, ROSTO_NEU, ROSTO_PUTO,
    CHECK, ERRADO, TROFEU, ESTRELA, ACENO, AVISO
)
# NOVO: importar a função para registrar o desempenho
from utils.desempenho import registrar_simulado

# Caminho para o banco de questões
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_QUESTOES = os.path.join(PASTA_ATUAL, "..", "questoes", "banco_questoes.json")

def _carregar_banco():
    """Retorna o dicionário com todas as questões."""
    try:
        with open(CAMINHO_QUESTOES, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

class TelaSimulado:
    """
    Permite montar um simulado combinando descritores e níveis de dificuldade.
    """
    def __init__(self, router, usuario):
        self.router = router
        self.usuario = usuario
        self.banco = _carregar_banco()
        # Lista de blocos selecionados. Cada bloco: (materia, chave_desc, nome_desc, nivel)
        self.selecionados = []

    def mostrar(self):
        while True:
            cabecalho_app()
            titulo(f"{LIVRO}  SIMULADO PERSONALIZADO")

            self._exibir_descritores_selecionados()

            print(f"\n  {CINZA}Opções disponíveis:{RESET}\n")
            imprimir_menu([
                "Adicionar descritor",
                "Remover descritor",
                "Começar simulado",
                "---",
                "Voltar ao menu"
            ])

            opcao = pedir_opcao(4)

            if opcao == 1:
                self._adicionar_descritor()
            elif opcao == 2:
                self._remover_descritor()
            elif opcao == 3:
                self._executar_simulado()
            elif opcao == 4:
                return

    def _exibir_descritores_selecionados(self):
        """Mostra a lista atual de blocos no topo da tela."""
        if not self.selecionados:
            print(f"\n  {CINZA}Nenhum descritor adicionado ainda.{RESET}")
            return

        nivel_icone = {"facil": ROSTO_FELIZ, "medio": ROSTO_NEU, "dificil": ROSTO_PUTO}
        print(f"\n  {AMARELO}{NEGRITO}📋 DESCRITORES SELECIONADOS:{RESET}")
        for i, (materia, _, nome_desc, nivel) in enumerate(self.selecionados, 1):
            icone = nivel_icone.get(nivel, "")
            print(f"  {AMARELO}[{i}]{RESET} {materia} – {nome_desc} {icone} ({nivel.capitalize()})")
        linha("─", 50)

    def _adicionar_descritor(self):
        """Fluxo para adicionar um novo bloco (matéria → descritor → dificuldade)."""
        # 1. Escolher matéria
        materias = ["Matemática", "Português"]
        materia = escolher_da_lista("Matéria:", materias)
        if not materia:
            return

        chave_materia = "Matematica" if materia == "Matemática" else "Portugues"
        if chave_materia not in self.banco:
            erro("Nenhuma questão cadastrada para esta matéria.")
            pausar()
            return

        # 2. Escolher descritor
        descritores_itens = list(self.banco[chave_materia].items())
        if not descritores_itens:
            erro("Nenhum descritor disponível.")
            pausar()
            return

        opcoes_desc = [f"{chave} - {dados['nome']}" for chave, dados in descritores_itens]
        escolha_desc = escolher_da_lista("Descritor:", opcoes_desc)
        if not escolha_desc:
            return

        chave_desc = escolha_desc.split(" - ")[0]
        dados_desc = self.banco[chave_materia][chave_desc]

        # 3. Escolher dificuldade
        niveis = [
            (f"Fácil {ROSTO_FELIZ}", "facil"),
            (f"Médio {ROSTO_NEU}", "medio"),
            (f"Difícil {ROSTO_PUTO}", "dificil")
        ]
        opcoes_nivel = [n[0] for n in niveis]
        escolha_nivel = escolher_da_lista("Nível de dificuldade:", opcoes_nivel)
        if not escolha_nivel:
            return

        nivel = next(n[1] for n in niveis if n[0] == escolha_nivel)

        # 4. Verificar se o bloco já foi adicionado
        for item in self.selecionados:
            if (item[0] == materia and item[1] == chave_desc and item[3] == nivel):
                erro("Este descritor e nível já foi adicionado ao simulado.")
                pausar()
                return

        # 5. Adicionar
        nome_desc = dados_desc["nome"]
        self.selecionados.append((materia, chave_desc, nome_desc, nivel))
        sucesso(f"Adicionado: {materia} – {nome_desc} ({nivel.capitalize()})")
        pausar("  Pressione ENTER para continuar...")

    def _remover_descritor(self):
        """Remove um bloco da lista de selecionados."""
        if not self.selecionados:
            info("Nenhum descritor foi adicionado ainda.")
            pausar()
            return

        cabecalho_app()
        titulo("REMOVER DESCRITOR")
        self._exibir_descritores_selecionados()

        print(f"\n  {CINZA}Digite o número do descritor que deseja remover:{RESET}")
        try:
            idx = int(input(f"  {AMARELO}Número: {RESET}")) - 1
            if 0 <= idx < len(self.selecionados):
                removido = self.selecionados.pop(idx)
                sucesso(f"Removido: {removido[0]} – {removido[2]}")
            else:
                erro("Número inválido.")
        except ValueError:
            erro("Digite um número válido.")
        pausar()

    def _executar_simulado(self):
        """Coleta todas as questões dos blocos selecionados, embaralha e inicia o quiz."""
        if not self.selecionados:
            erro("Adicione pelo menos um descritor antes de começar o simulado.")
            pausar()
            return

        # Monta lista de todas as questões
        todas_questoes = []
        for materia, chave_desc, nome_desc, nivel in self.selecionados:
            chave_materia = "Matematica" if materia == "Matemática" else "Portugues"
            try:
                questoes_bloco = self.banco[chave_materia][chave_desc][nivel]
                # Garante que cada questão receba referências ao descritor
                for q in questoes_bloco:
                    q["_materia"] = materia
                    q["_descritor_chave"] = chave_desc   # NOVO: adiciona chave do descritor
                    q["_descritor_nome"] = nome_desc
                todas_questoes.extend(questoes_bloco)
            except KeyError:
                erro(f"Erro ao carregar questões de {materia} – {nome_desc} ({nivel})")
                continue

        if not todas_questoes:
            erro("Nenhuma questão encontrada para os blocos selecionados.")
            pausar()
            return

        # Embaralha a ordem das questões
        random.shuffle(todas_questoes)

        # Lista para armazenar os resultados (usada no registro de desempenho)
        resultados = []

        # Executa o quiz
        acertos = 0
        total = len(todas_questoes)

        for i, questao in enumerate(todas_questoes, 1):
            cabecalho_app()
            titulo(f"{LIVRO}  SIMULADO — Questão {i}/{total}")

            # Informações do descritor
            materia = questao.get("_materia", "?")
            descritor = questao.get("_descritor_nome", "?")
            print(f"  {CINZA}{materia} – {descritor}{RESET}\n")

            # Enunciado
            print(f"  {NEGRITO}{questao['enunciado']}{RESET}\n")

            # Alternativas
            for alt in questao["alternativas"]:
                print(f"  {alt}")

            # Resposta
            while True:
                resp = input(f"\n  {AMARELO}Sua resposta (A/B/C/D): {RESET}").strip().upper()
                if resp in ("A", "B", "C", "D"):
                    break
                erro("Digite apenas A, B, C ou D.")

            # Correção
            correta = questao["resposta"].upper()
            acertou = (resp == correta)
            if acertou:
                acertos += 1
                print(f"\n  {VERDE}{CHECK} Correto!{RESET}")
            else:
                print(f"\n  {VERMELHO}{ERRADO} Errado! Resposta correta: {correta}{RESET}")

            #Registra o resultado desta questão para o desempenho
            resultados.append({
                "materia": materia,
                "descritor_chave": questao.get("_descritor_chave", ""),
                "descritor_nome": descritor,
                "acertou": acertou
            })

            if i < total:
                input(f"\n  {CINZA}Pressione ENTER para a próxima questão...{RESET}")

        #Salva os resultados no histórico de desempenho
        registrar_simulado(self.usuario["email"], resultados)

        # Resultado final
        cabecalho_app()
        titulo(f"{TROFEU}  RESULTADO DO SIMULADO")

        percentual = (acertos / total) * 100
        print(f"\n  {NEGRITO}Você acertou {acertos} de {total} questões!{RESET}")
        print(f"  {NEGRITO}Aproveitamento: {percentual:.1f}%{RESET}\n")
        linha()

        if percentual >= 80:
            print(f"  {VERDE}{ESTRELA} Excelente! Continue assim!{RESET}")
        elif percentual >= 60:
            print(f"  {AMARELO}{ACENO} Bom trabalho! Dá para melhorar ainda mais.{RESET}")
        else:
            print(f"  {VERMELHO}{CADERNO} Revise os conteúdos e tente novamente.{RESET}")

        pausar("  Pressione ENTER para voltar ao menu do simulado...")