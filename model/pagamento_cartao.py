from datetime import date

from model.pagamento import Pagamento


class PagamentoCartao(Pagamento):
    def __init__(self, data: date, valor_pago: float, atendimento,
                 numero_cartao: str, bandeira: str):
        super().__init__(data, valor_pago, atendimento)
        self.numero_cartao = numero_cartao
        self.bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str):
        if (not isinstance(numero_cartao, str) or not numero_cartao.isdigit()
                or not 13 <= len(numero_cartao) <= 19):
            raise ValueError("O número do cartão deve ter entre 13 e 19 dígitos.")
        self.__numero_cartao = numero_cartao

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        if not isinstance(bandeira, str) or not bandeira.strip():
            raise ValueError("A bandeira do cartão não pode ser vazia.")
        self.__bandeira = bandeira.strip()

    def modalidade(self) -> str:
        return f"Cartão de crédito ({self.__bandeira} final {self.__numero_cartao[-4:]})"
