class Router:
    """
    Controlador de navegação entre telas.
    
    Atributos:
      tela_atual → string com o nome da tela ativa agora
      usuario    → dicionário com os dados do usuário logado (ou None)
    """
    
    def __init__(self):
        self.tela_atual = "inicio"
        self.usuario    = None        # Ninguém está logado ainda
    
    def ir_para(self, destino, usuario=None):
        """
        Registra o destino e, se um usuário for passado, o salva.
        
        Parâmetro 'usuario': é passado quando o login é bem-sucedido.
        """
        self.tela_atual = destino
        
        if usuario is not None:
            self.usuario = usuario
        
        # Se for para o início (logout), limpa o usuário
        if destino == "inicio":
            self.usuario = None