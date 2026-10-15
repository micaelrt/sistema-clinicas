from datetime import date

from model.pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    def __init__(self, data: date, valor_pago: float, atendimento):
        super().__init__(data, valor_pago, atendimento)

    def modalidade(self) -> str:
        return "Dinheiro"
