from datetime import time

from model.profissional_saude import ProfissionalSaude
from exceptions.cadastro_duplicado_exception import CadastroDuplicadoException
from exceptions.profissional_nao_vinculado_exception import ProfissionalNaoVinculadoException


class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str,
                 hora_abertura: time, hora_fechamento: time):
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao
        self.alterar_horario(hora_abertura, hora_fechamento)
        # Agregação: os profissionais existem fora da clínica e são apenas vinculados a ela.
        self.__profissionais = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome da clínica não pode ser vazio.")
        self.__nome = nome.strip()

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str):
        if not isinstance(cidade, str) or not cidade.strip():
            raise ValueError("A cidade não pode ser vazia.")
        self.__cidade = cidade.strip()

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser um texto.")
        self.__descricao = descricao.strip()

    @property
    def hora_abertura(self) -> time:
        return self.__hora_abertura

    @property
    def hora_fechamento(self) -> time:
        return self.__hora_fechamento

    @property
    def profissionais(self) -> list:
        return list(self.__profissionais)

    def alterar_horario(self, hora_abertura: time, hora_fechamento: time):
        if not isinstance(hora_abertura, time) or not isinstance(hora_fechamento, time):
            raise TypeError("Os horários devem ser do tipo hora.")
        if hora_abertura >= hora_fechamento:
            raise ValueError("A hora de abertura deve ser anterior à hora de fechamento.")
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento

    def adicionar_profissional(self, profissional: ProfissionalSaude):
        if not isinstance(profissional, ProfissionalSaude):
            raise TypeError("Só é possível vincular profissionais de saúde.")
        if self.possui_profissional(profissional):
            raise CadastroDuplicadoException(
                f"{profissional.nome} já está vinculado(a) à clínica {self.__nome}.")
        self.__profissionais.append(profissional)

    def remover_profissional(self, profissional: ProfissionalSaude):
        if not self.possui_profissional(profissional):
            raise ProfissionalNaoVinculadoException()
        self.__profissionais.remove(profissional)

    def possui_profissional(self, profissional: ProfissionalSaude) -> bool:
        return profissional in self.__profissionais

    def esta_aberta(self, inicio: time, fim: time) -> bool:
        return self.__hora_abertura <= inicio < fim <= self.__hora_fechamento
