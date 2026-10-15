class ProfissionalNaoVinculadoException(Exception):
    def __init__(self, mensagem: str = "O profissional não está vinculado a essa clínica."):
        super().__init__(mensagem)
