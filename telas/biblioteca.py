# =============================================================================
# A biblioteca de questões é onde o aluno pode estudar os descritores.
# O conteúdo é carregado do arquivo banco_questoes.json.
# =============================================================================

import json
import os

from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao,
    erro, pausar,
    AMARELO, VERDE, VERMELHO, CINZA, RESET, NEGRITO
)

# Caminho até o banco de questões
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_QUESTOES = os.path.join(PASTA_ATUAL, "..", "questoes", "banco_questoes.json")


def carregar_banco():
    """
    Lê o arquivo banco_questoes.json e retorna o conteúdo.
    """
    try:
        with open(CAMINHO_QUESTOES, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


class TelaBiblioteca:
    """
    Tela principal da Biblioteca.
    Permite escolher entre Matemática e Português.
    """
    
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario
        self.banco   = carregar_banco()
    
    def mostrar(self):
        while True:
            cabecalho_app()
            titulo("📚  BIBLIOTECA")
            
            print(f"  {CINZA}Escolha uma matéria para estudar:{RESET}\n")
            imprimir_menu(["Matemática", "Português", "---", "Voltar"])
            
            opcao = pedir_opcao(3)
            
            if opcao == 1:
                self._menu_materia("Matematica", "Matemática")
            elif opcao == 2:
                self._menu_materia("Portugues", "Português")
            elif opcao == 3:
                return
    
    def _menu_materia(self, chave_json, nome_exibido):
        """
        Exibe os descritores de uma matéria, paginados de 5 em 5.
        chave_json   → como a matéria está escrita no JSON
        nome_exibido → como mostrar ao usuário
        """
        if chave_json not in self.banco:
            erro("Nenhum conteúdo encontrado para esta matéria.")
            pausar()
            return
        
        # Pega os descritores como lista
        # .items() retorna pares (chave, valor) do dicionário
        descritores = list(self.banco[chave_json].items())
        # descritores = [("D01", {...}), ("D02", {...}), ...]
        
        pagina_atual = 0       # índice da primeira questão da página
        por_pagina   = 5       # quantos descritores mostrar por vez
        
        while True:
            cabecalho_app()
            titulo(f"📘  {nome_exibido.upper()} — DESCRITORES")
            
            # Calcula quais descritores mostrar nesta página
            inicio = pagina_atual
            fim    = pagina_atual + por_pagina
            pagina = descritores[inicio:fim]  # slice da lista
            
            # Total de páginas
            total = len(descritores)
            print(f"  {CINZA}Mostrando {inicio+1}–{min(fim, total)} de {total} descritores{RESET}\n")
            
            # Monta a lista de opções (nomes dos descritores desta página)
            nomes_descritores = [dados["nome"] for _, dados in pagina]
            
            opcoes = nomes_descritores.copy()
            
            # Botões de navegação
            if fim < total:
                opcoes.append("➡ Avançar (próximos 5)")
            if pagina_atual > 0:
                opcoes.append("⬅ Voltar (5 anteriores)")
            opcoes.append("---")
            opcoes.append("Voltar à Biblioteca")
            
            imprimir_menu(opcoes)
            opcao = pedir_opcao(len(opcoes) - 1)  # -1 porque "---" não conta
            
            # Verifica o que o usuário escolheu
            idx_avancar = len(nomes_descritores) + 1 if fim < total else None
            idx_voltar  = (len(nomes_descritores) + (2 if idx_avancar else 1)) if pagina_atual > 0 else None
            idx_sair    = len(opcoes) - 1  # último item (Voltar à Biblioteca)
            
            if opcao == idx_sair:
                return
            elif idx_avancar and opcao == idx_avancar:
                pagina_atual += por_pagina
            elif idx_voltar and opcao == idx_voltar:
                pagina_atual -= por_pagina
            elif 1 <= opcao <= len(nomes_descritores):
                # Usuário escolheu um descritor
                chave_desc, dados_desc = pagina[opcao - 1]
                self._menu_dificuldade(dados_desc, nome_exibido)
    
    def _menu_dificuldade(self, dados_descritor, materia):
        """
        Exibe as opções de dificuldade para um descritor.
        """
        cabecalho_app()
        titulo(f"⚡  {dados_descritor['nome']}")
        
        print(f"  {CINZA}Escolha o nível de dificuldade:{RESET}\n")
        imprimir_menu(["😊 Fácil", "😐 Médio", "😤 Difícil", "---", "Voltar"])
        
        opcao = pedir_opcao(4)
        
        if opcao == 4:
            return
        
        niveis = {1: "facil", 2: "medio", 3: "dificil"}
        nivel = niveis[opcao]
        
        questoes = dados_descritor.get(nivel, [])
        
        if not questoes:
            erro("Questões não disponíveis para este nível ainda.")
            pausar()
            return
        
        self._resolver_questoes(questoes, dados_descritor["nome"], nivel, materia)
    
    def _resolver_questoes(self, questoes, nome_descritor, nivel, materia):
        """
        Percorre as 5 questões e exibe uma a uma.
        No final mostra o resultado (pontuação).
        """
        acertos = 0
        total   = len(questoes)
        
        # Níveis de questões
        nivel_bonito = {"facil": "Fácil 😊", "medio": "Médio 😐", "dificil": "Difícil 😤"}
        
        for i, questao in enumerate(questoes, start=1):
            cabecalho_app()
            
            # Cabeçalho da questão
            print(f"  {AMARELO}{NEGRITO}{materia} — {nome_descritor}{RESET}")
            print(f"  {CINZA}Nível: {nivel_bonito[nivel]}  |  Questão {i}/{total}{RESET}")
            linha()
            
            # Enunciado
            print(f"\n  {NEGRITO}{questao['enunciado']}{RESET}\n")
            
            # Alternativas
            for alt in questao["alternativas"]:
                print(f"  {alt}")
            
            # Pede a resposta
            while True:
                resposta = input(f"\n  {AMARELO}Sua resposta (A/B/C/D): {RESET}").strip().upper()
                if resposta in ("A", "B", "C", "D"):
                    break
                erro("Digite apenas A, B, C ou D.")
            
            # Verifica
            correta = questao["resposta"].upper()
            if resposta == correta:
                acertos += 1
                print(f"\n  {VERDE}✅ Correto!{RESET}")
            else:
                print(f"\n  {VERMELHO}❌ Errado! A resposta correta era: {correta}{RESET}")
            
            # Pausa entre questões (menos na última)
            if i < total:
                input(f"\n  {CINZA}Pressione ENTER para a próxima questão...{RESET}")
        
        # ── Resultado Final ────────────────────────────────────────────
        cabecalho_app()
        titulo("🏆  RESULTADO")
        
        porcentagem = (acertos / total) * 100
        
        print(f"\n  {NEGRITO}Você acertou {acertos} de {total} questões!{RESET}")
        print(f"  {NEGRITO}Aproveitamento: {porcentagem:.0f}%{RESET}\n")
        
        linha()
        
        # Mensagem de acordo com o desempenho
        if porcentagem >= 80:
            print(f"  {VERDE}🌟 Excelente! Continue assim!{RESET}")
        elif porcentagem >= 60:
            print(f"  {AMARELO}👍 Bom trabalho! Ainda há espaço para melhorar.{RESET}")
        else:
            print(f"  {VERMELHO}📖 Revise o conteúdo e tente novamente!{RESET}")
        
        pausar()
