from abc import ABC, abstractmethod
from datetime import date


class Pagamento(ABC):
    @abstractmethod
    def __init__(self, data: date, valor_pago: float, atendimento):
        self.data = data
        self.valor_pago = valor_pago
        self.__atendimento = atendimento

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        if not isinstance(data, date):
            raise TypeError("A data do pagamento deve ser uma data.")
        self.__data = data

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float):
        if not isinstance(valor_pago, (int, float)) or valor_pago <= 0:
            raise ValueError("O valor pago deve ser maior que zero.")
        self.__valor_pago = float(valor_pago)

    @property
    def atendimento(self):
        return self.__atendimento

    def paciente(self):
        return self.__atendimento.paciente

    @abstractmethod
    def modalidade(self) -> str:
        pass
