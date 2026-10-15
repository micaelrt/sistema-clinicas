class NaoEncontradoException(Exception):
    def __init__(self, mensagem: str = "Registro não encontrado."):
        super().__init__(mensagem)
