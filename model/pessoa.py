from abc import ABC, abstractmethod
from datetime import date


class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, cpf: str, celular: str, data_nascimento: date):
        if not isinstance(cpf, str) or len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("O CPF deve ter 11 dígitos.")
        self.__cpf = cpf
        self.nome = nome
        self.celular = celular
        self.data_nascimento = data_nascimento

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome não pode ser vazio.")
        self.__nome = nome.strip()

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str):
        if not isinstance(celular, str) or not celular.strip():
            raise ValueError("O celular não pode ser vazio.")
        self.__celular = celular.strip()

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date):
        if not isinstance(data_nascimento, date):
            raise TypeError("A data de nascimento deve ser uma data.")
        if data_nascimento > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")
        self.__data_nascimento = data_nascimento

    def idade(self) -> int:
        hoje = date.today()
        anos = hoje.year - self.__data_nascimento.year
        if (hoje.month, hoje.day) < (self.__data_nascimento.month, self.__data_nascimento.day):
            anos -= 1
        return anos

    @abstractmethod
    def exibir_dados(self) -> str:
        return (f"Nome: {self.__nome} | CPF: {self.__cpf} | Celular: {self.__celular} | "
                f"Nascimento: {self.__data_nascimento.strftime('%d/%m/%Y')} ({self.idade()} anos)")
