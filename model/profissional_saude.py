from datetime import date

from model.pessoa import Pessoa


class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, cpf: str, celular: str, data_nascimento: date,
                 especialidade: str, registro_profissional: str):
        super().__init__(nome, cpf, celular, data_nascimento)
        self.especialidade = especialidade
        self.registro_profissional = registro_profissional

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str):
        if not isinstance(especialidade, str) or not especialidade.strip():
            raise ValueError("A especialidade não pode ser vazia.")
        self.__especialidade = especialidade.strip()

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional

    @registro_profissional.setter
    def registro_profissional(self, registro_profissional: str):
        if not isinstance(registro_profissional, str) or not registro_profissional.strip():
            raise ValueError("O registro profissional não pode ser vazio.")
        self.__registro_profissional = registro_profissional.strip()

    def exibir_dados(self) -> str:
        return (super().exibir_dados() +
                f" | Especialidade: {self.__especialidade} | Registro: {self.__registro_profissional}")
