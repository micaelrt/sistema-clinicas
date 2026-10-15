class ValorExcedenteException(Exception):
    def __init__(self, mensagem: str = "O valor pago não pode ultrapassar o valor restante do atendimento."):
        super().__init__(mensagem)
