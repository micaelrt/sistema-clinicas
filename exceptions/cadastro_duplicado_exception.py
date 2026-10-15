class CadastroDuplicadoException(Exception):
    def __init__(self, mensagem: str = "Já existe um cadastro com esse identificador."):
        super().__init__(mensagem)
