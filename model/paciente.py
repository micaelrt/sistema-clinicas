from datetime import date

from model.pessoa import Pessoa
from exceptions.paciente_menor_sem_responsavel_exception import PacienteMenorSemResponsavelException


class Paciente(Pessoa):
    def __init__(self, nome: str, cpf: str, celular: str, data_nascimento: date,
                 responsavel: "Paciente" = None):
        super().__init__(nome, cpf, celular, data_nascimento)
        self.responsavel = responsavel

    @property
    def responsavel(self) -> "Paciente":
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel: "Paciente"):
        if self.maior_de_idade():
            # Paciente maior de idade realiza atendimentos de forma independente.
            self.__responsavel = None
            return
        if responsavel is None:
            raise PacienteMenorSemResponsavelException()
        if not isinstance(responsavel, Paciente):
            raise TypeError("O responsável deve ser um paciente cadastrado.")
        if responsavel is self:
            raise ValueError("O paciente não pode ser responsável por si mesmo.")
        if not responsavel.maior_de_idade():
            raise PacienteMenorSemResponsavelException("O responsável precisa ser maior de idade.")
        self.__responsavel = responsavel

    def maior_de_idade(self) -> bool:
        return self.idade() >= 18

    def exibir_dados(self) -> str:
        dados = super().exibir_dados()
        if self.__responsavel is not None:
            dados += f" | Responsável: {self.__responsavel.nome} (CPF {self.__responsavel.cpf})"
        return dados
