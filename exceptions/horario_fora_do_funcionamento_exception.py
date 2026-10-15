class HorarioForaDoFuncionamentoException(Exception):
    def __init__(self, mensagem: str = "O atendimento deve ocorrer dentro do horário de funcionamento da clínica."):
        super().__init__(mensagem)
