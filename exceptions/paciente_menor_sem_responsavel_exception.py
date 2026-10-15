class PacienteMenorSemResponsavelException(Exception):
    def __init__(self, mensagem: str = "Paciente menor de 18 anos precisa de um responsável maior de idade."):
        super().__init__(mensagem)
