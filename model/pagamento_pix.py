from datetime import date

from model.pagamento import Pagamento


class PagamentoPix(Pagamento):
    def __init__(self, data: date, valor_pago: float, atendimento, cpf_pagador: str):
        super().__init__(data, valor_pago, atendimento)
        self.cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        if not isinstance(cpf_pagador, str) or len(cpf_pagador) != 11 or not cpf_pagador.isdigit():
            raise ValueError("O CPF do pagador deve ter 11 dígitos.")
        self.__cpf_pagador = cpf_pagador

    def modalidade(self) -> str:
        return f"PIX (CPF do pagador: {self.__cpf_pagador})"
