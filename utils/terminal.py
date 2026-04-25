import os
import sys
from utils.emojis import(
    AVISO,CHECK,INFO,LIVRO,
)

# ── Códigos de cor ANSI ──────────────────────────────────────────────────────
# Esses são códigos especiais que mudam a cor do texto no terminal.

AMARELO  = "\033[93m"   # Amarelo claro
VERDE    = "\033[92m"   # Verde claro
VERMELHO = "\033[91m"   # Vermelho claro
AZUL     = "\033[94m"   # Azul claro
CINZA    = "\033[90m"   # Cinza
BRANCO   = "\033[97m"   # Branco claro
RESET    = "\033[0m"    # Volta ao padrão
NEGRITO  = "\033[1m"    # Negrito


def limpar_tela():
    """
    Limpa o terminal.
    'cls' funciona no Windows; 'clear' no Linux/Mac.
    os.name retorna 'nt' no Windows e 'posix' no Linux/Mac.
    """
    os.system("cls" if os.name == "nt" else "clear")


def linha(caractere="─", largura=55):
    """
    Imprime uma linha horizontal.
    """
    print(CINZA + caractere * largura + RESET)


def titulo(texto):
    """
    Imprime um bloco de título formatado.
    Exemplo:
      ───────────────────────────────────────────────────────
        MONITOR AÊ
      ───────────────────────────────────────────────────────
    """
    linha()
    print(f"{AMARELO}{NEGRITO}  {texto}{RESET}")
    linha()


def subtitulo(texto):
    """
    Imprime um subtítulo menor, com linha abaixo.
    """
    print(f"\n{AMARELO}{NEGRITO}  {texto}{RESET}")
    print(CINZA + "  " + "─" * 45 + RESET)


def sucesso(mensagem):
    """
    Imprime uma mensagem de sucesso em verde.
    """
    print(f"\n{VERDE}  {CHECK} {mensagem}{RESET}")


def erro(mensagem):
    """
    Imprime uma mensagem de erro em vermelho.
    """
    print(f"\n{VERMELHO}  {AVISO}  {mensagem}{RESET}")


def info(mensagem):
    """
    Imprime uma mensagem informativa em azul.
    """
    print(f"{AZUL}  {INFO}  {mensagem}{RESET}")


def imprimir_menu(opcoes):
    """
    Recebe uma lista de strings e imprime como opções numeradas.
    Também aceita uma string especial "---" para imprimir uma linha separadora.
    """
    numero = 1
    for opcao in opcoes:
        if opcao == "---":
            print(CINZA + "  " + "─" * 30 + RESET)
        else:
            print(f"  {AMARELO}[{numero}]{RESET} {opcao}")
            numero += 1


def pedir_opcao(total, prompt="  Escolha uma opção: "):
    """
    Pede que o usuário digite uma opção numérica entre 1 e total.
    Fica repetindo até receber uma entrada válida.
    Retorna o número escolhido.
    """
    while True:
        try:
            entrada = input(f"\n{AMARELO}{prompt}{RESET}")
            numero = int(entrada)
            if 1 <= numero <= total:
                return numero
            else:
                erro(f"Digite um número entre 1 e {total}.")
        except ValueError:
            # ValueError acontece quando o usuário digita texto em vez de número
            erro("Digite apenas números.")


def pedir_texto(prompt, obrigatorio=True, senha=False):
    """
    Pede que o usuário digite um texto.
    Se 'obrigatorio=True', não aceita entrada vazia.
    Se 'senha=True', mascara cada caractere digitado com '*'.
    Retorna a string digitada.
    """
    if senha:
        while True:
            valor = _ler_senha_com_mascara(f"  {prompt}: ")
            if not obrigatorio or valor.strip():
                return valor
            erro("Este campo não pode estar vazio.")
    else:
        while True:
            valor = input(f"  {prompt}: ")
            if not obrigatorio or valor.strip():
                return valor
            erro("Este campo não pode estar vazio.")


def _ler_senha_com_mascara(prompt):
    """
    Lê a senha no terminal exibindo '*' para cada caractere digitado.
    No Windows usa msvcrt; nos demais sistemas faz fallback para getpass.
    """
    if os.name != "nt":
        import getpass

        return getpass.getpass(prompt)

    import msvcrt

    print(prompt, end="", flush=True)
    caracteres = []

    while True:
        tecla = msvcrt.getwch()

        if tecla in ("\r", "\n"):
            print()
            return "".join(caracteres)

        if tecla == "\003":
            raise KeyboardInterrupt

        if tecla == "\b":
            if caracteres:
                caracteres.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue

        if tecla in ("\x00", "\xe0"):
            msvcrt.getwch()
            continue

        caracteres.append(tecla)
        sys.stdout.write("*")
        sys.stdout.flush()


def escolher_da_lista(titulo_lista, opcoes):
    """
    Mostra uma lista numerada de opções e pede que o usuário escolha uma.
    Retorna a opção escolhida (string) ou None se o usuário cancelar.
    Exemplo:
        escola = escolher_da_lista("Escola:", ["Escola A", "Escola B"])
    """
    print(f"\n  {AMARELO}{titulo_lista}{RESET}")
    for i, opcao in enumerate(opcoes, start=1):
        print(f"  {AMARELO}[{i}]{RESET} {opcao}")
    print(f"  {AMARELO}[0]{RESET} Cancelar / Voltar")
    
    while True:
        try:
            entrada = input(f"\n{AMARELO}  Escolha: {RESET}")
            numero = int(entrada)
            if numero == 0:
                return None  # Usuário quer voltar
            if 1 <= numero <= len(opcoes):
                return opcoes[numero - 1]
            else:
                erro(f"Digite um número entre 0 e {len(opcoes)}.")
        except ValueError:
            erro("Digite apenas números.")


def pausar(mensagem="  Pressione ENTER para continuar..."):
    """
    Pausa a execução e espera o usuário pressionar ENTER.
    """
    input(f"\n{CINZA}{mensagem}{RESET}")


def confirmar(pergunta):
    """
    Faz uma pergunta de Sim/Não e retorna True ou False.
    Exemplo:
        if confirmar("Deseja excluir sua conta?"):
            ...
    """
    while True:
        resposta = input(f"\n  {AMARELO}{pergunta} (s/n): {RESET}").strip().lower()
        if resposta in ("s", "sim"):
            return True
        elif resposta in ("n", "não", "nao"):
            return False
        else:
            erro("Digite 's' para sim ou 'n' para não.")


def cabecalho_app():
    """
    Imprime o cabeçalho padrão do aplicativo.
    """
    limpar_tela()
    print()
    linha("═")
    print(f"{AMARELO}{NEGRITO}{LIVRO}  MONITORAÊ — Plataforma Educacional{RESET}")
    linha("═")
    print()
