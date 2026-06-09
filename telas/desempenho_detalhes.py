from utils.terminal import (
    cabecalho_app, titulo, linha, pausar,
    AMARELO, CINZA, RESET, NEGRITO, VERDE, VERMELHO
)
from utils.desempenho import obter_desempenho_usuario
from utils.emojis import GRAFICO, ESTRELA, AVISO

class TelaDesempenhoDetalhes:
    def __init__(self, router, usuario):
        self.router = router
        self.usuario = usuario
    
    def mostrar(self):
        cabecalho_app()
        titulo(f"{GRAFICO}  DESEMPENHO DETALHADO")
        
        desempenho = obter_desempenho_usuario(self.usuario["email"])
        total_q = desempenho["total_questoes"]
        total_ac = desempenho["total_acertos"]
        total_erros = total_q - total_ac
        percentual = (total_ac / total_q * 100) if total_q > 0 else 0
        
        print(f"\n  {NEGRITO}RESUMO GERAL{RESET}")
        print(f"  {CINZA}Questões respondidas:{RESET} {total_q}")
        print(f"  {CINZA}Acertos:{RESET} {total_ac}")
        print(f"  {CINZA}Erros:{RESET} {total_erros}")
        print(f"  {CINZA}Percentual de acerto:{RESET} {percentual:.1f}%\n")
        
        linha()
        
        por_assunto = desempenho["por_assunto"]
        if por_assunto:
            melhor_assunto = max(por_assunto.items(), key=lambda x: x[1]["acertos"])
            pior_assunto = max(por_assunto.items(), key=lambda x: x[1]["erros"])
            
            print(f"\n  {NEGRITO}DESEMPENHO POR ASSUNTO{RESET}")
            for assunto, dados in por_assunto.items():
                acertos = dados["acertos"]
                erros = dados["erros"]
                total = acertos + erros
                perc = (acertos / total * 100) if total > 0 else 0
                if perc >= 70:
                    indicador = f"{VERDE}✔{RESET}"
                elif perc >= 40:
                    indicador = f"{AMARELO}⚠{RESET}"
                else:
                    indicador = f"{VERMELHO}✘{RESET}"
                print(f"  {indicador} {assunto}: {acertos}/{total} ({perc:.0f}%)")
            
            print(f"\n  {NEGRITO}DESTAQUES{RESET}")
            print(f"  {ESTRELA} Assunto com mais acertos: {melhor_assunto[0]} ({melhor_assunto[1]['acertos']} acertos)")
            print(f"  {AVISO} Assunto com mais erros: {pior_assunto[0]} ({pior_assunto[1]['erros']} erros)")
        else:
            print(f"\n  {CINZA}Nenhum dado de desempenho ainda. Complete um simulado para gerar estatísticas.{RESET}")
        
        pausar()