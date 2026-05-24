from utils.usuarios import listar_monitores
from validacoes.validadores import MATERIAS_PERMITIDAS, ESCOLAS_PERMITIDAS
from utils.terminal import (
    cabecalho_app, titulo, linha,
    imprimir_menu, pedir_opcao, pedir_texto,
    escolher_da_lista, info,
    AMARELO, CINZA, AZUL, RESET, NEGRITO
)
from utils.emojis import (
    LUPA, ESCOLA, CADERNO
)
 
class TelaMonitores:
    """Exibe todos os monitores cadastrados com opção de filtrar."""
    def __init__(self, router, usuario):
        self.router  = router
        self.usuario = usuario
    
    def mostrar(self):
        """Loop principal: exibe filtros e lista de monitores."""
        # Filtros ativos - começa com nenhum filtro
        filtro_materia = None
        filtro_escola  = None
        filtro_nome    = None
        
        while True:
            cabecalho_app()
            titulo(f"{LUPA}  MONITORES CADASTRADOS")
            
            todos_monitores = listar_monitores()
            
            resultado = self._aplicar_filtros(todos_monitores, filtro_materia, filtro_escola, filtro_nome)
            
            # Mostra filtros ativos
            self._exibir_filtros_ativos(filtro_materia, filtro_escola, filtro_nome)
            self._exibir_monitores(resultado)

            print()
            imprimir_menu([
                "Filtrar por Matéria",
                "Filtrar por Escola",
                "Buscar por Nome",
                "Limpar Filtros",
                "---",
                "Voltar"
            ])
            
            opcao = pedir_opcao(5)
            
            if opcao == 1:
                escolha = escolher_da_lista("Filtrar por matéria:", MATERIAS_PERMITIDAS)
                if escolha:
                    filtro_materia = escolha
            
            elif opcao == 2:
                escolha = escolher_da_lista("Filtrar por escola:", ESCOLAS_PERMITIDAS)
                if escolha:
                    filtro_escola = escolha
            
            elif opcao == 3:
                nome = pedir_texto("Buscar por nome (parte do nome)", obrigatorio=False)
                filtro_nome = nome.strip() if nome.strip() else None
            
            elif opcao == 4:
                filtro_materia = None
                filtro_escola  = None
                filtro_nome    = None
                info("Filtros removidos.")
            
            elif opcao == 5:
                return
    
    def _aplicar_filtros(self, monitores, materia, escola, nome):
        resultado = []
        for m in monitores:
            # Verifica filtro de matéria
            if materia and m.get("materia") != materia:
                continue  # 'continue' pula para o próximo da lista
            
            # Verifica filtro de escola
            if escola and m.get("escola") != escola:
                continue
            
            # Verifica filtro de nome (busca parcial, sem diferenciar maiúsculas)
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
        """Formata e imprime cada monitor da lista."""
        
        print(f"\n  {AMARELO}Total encontrado: {len(monitores)} monitor(es){RESET}\n")
        
        if not monitores:
            print(f"  {CINZA}Nenhum monitor encontrado com esses filtros.{RESET}")
            return
        
        linha("─", 55)
        for i, m in enumerate(monitores, start=1):
            nome    = m.get("nome",    "—")
            escola  = m.get("escola",  "—")
            materia = m.get("materia", "—")
            
            # Inicial do nome para o "avatar" textual
            inicial = nome[0].upper() if nome else "?"
            
            print(f"\n  {AMARELO}{NEGRITO}[{i}] {inicial} — {nome}{RESET}")
            print(f"  {CINZA}    {ESCOLA} {escola}{RESET}")
            print(f"  {CINZA}    {CADERNO} Matéria: {RESET}{AMARELO}{materia}{RESET}")
            linha("─", 55)
 