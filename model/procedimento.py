from model.profissional_saude import ProfissionalSaude


class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional: ProfissionalSaude):
        self.descricao = descricao
        self.custo = custo
        self.profissional = profissional

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        if not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("A descrição do procedimento não pode ser vazia.")
        self.__descricao = descricao.strip()

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float):
        if not isinstance(custo, (int, float)) or custo < 0:
            raise ValueError("O custo deve ser um número maior ou igual a zero.")
        self.__custo = float(custo)

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        if not isinstance(profissional, ProfissionalSaude):
            raise TypeError("O responsável pelo procedimento deve ser um profissional de saúde.")
        self.__profissional = profissional
