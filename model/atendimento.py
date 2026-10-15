from datetime import date, time

from model.clinica import Clinica
from model.paciente import Paciente
from model.profissional_saude import ProfissionalSaude
from model.tipo_atendimento import TipoAtendimento
from model.procedimento import Procedimento
from model.pagamento import Pagamento
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.paciente_menor_sem_responsavel_exception import PacienteMenorSemResponsavelException
from exceptions.horario_fora_do_funcionamento_exception import HorarioForaDoFuncionamentoException
from exceptions.profissional_nao_vinculado_exception import ProfissionalNaoVinculadoException
from exceptions.pagamento_fora_do_prazo_exception import PagamentoForaDoPrazoException
from exceptions.valor_excedente_exception import ValorExcedenteException


class Atendimento:
    def __init__(self, codigo: int, clinica: Clinica, paciente: Paciente,
                 profissional: ProfissionalSaude, tipo: TipoAtendimento, data: date,
                 hora_inicio: time, hora_fim: time, valor: float):
        self.__codigo = codigo
        # Composição: procedimentos e pagamentos só existem dentro do atendimento.
        self.__procedimentos = []
        self.__pagamentos = []
        self.alterar_dados(clinica, paciente, profissional, tipo, data, hora_inicio, hora_fim, valor)

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @property
    def tipo(self) -> TipoAtendimento:
        return self.__tipo

    @property
    def data(self) -> date:
        return self.__data

    @property
    def hora_inicio(self) -> time:
        return self.__hora_inicio

    @property
    def hora_fim(self) -> time:
        return self.__hora_fim

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def procedimentos(self) -> list:
        return list(self.__procedimentos)

    @property
    def pagamentos(self) -> list:
        return list(self.__pagamentos)

    def alterar_dados(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude,
                      tipo: TipoAtendimento, data: date, hora_inicio: time, hora_fim: time,
                      valor: float):
        # Valida tudo antes de alterar, para o objeto nunca ficar em estado inválido.
        if not isinstance(clinica, Clinica):
            raise TypeError("Clínica inválida.")
        if not isinstance(paciente, Paciente):
            raise TypeError("Paciente inválido.")
        if not isinstance(profissional, ProfissionalSaude):
            raise TypeError("Profissional inválido.")
        if not isinstance(tipo, TipoAtendimento):
            raise TypeError("Tipo de atendimento inválido.")
        if not isinstance(data, date):
            raise TypeError("A data do atendimento deve ser uma data.")
        if not isinstance(hora_inicio, time) or not isinstance(hora_fim, time):
            raise TypeError("Os horários devem ser do tipo hora.")
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O valor deve ser um número maior ou igual a zero.")
        if not paciente.maior_de_idade() and paciente.responsavel is None:
            raise PacienteMenorSemResponsavelException()
        if not clinica.possui_profissional(profissional):
            raise ProfissionalNaoVinculadoException(
                f"{profissional.nome} não está vinculado(a) à clínica {clinica.nome}.")
        if hora_inicio >= hora_fim:
            raise ValueError("A hora de início deve ser anterior à hora de fim.")
        if not clinica.esta_aberta(hora_inicio, hora_fim):
            raise HorarioForaDoFuncionamentoException(
                f"A clínica {clinica.nome} funciona das {clinica.hora_abertura.strftime('%H:%M')} "
                f"às {clinica.hora_fechamento.strftime('%H:%M')}.")
        if any(pagamento.data > data for pagamento in self.__pagamentos):
            raise PagamentoForaDoPrazoException(
                "Já existem pagamentos posteriores a essa data de atendimento.")
        if valor + self.__custo_procedimentos() < self.valor_pago():
            raise ValorExcedenteException(
                "O novo valor ficaria menor do que o total já pago.")

        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__tipo = tipo
        self.__data = data
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__valor = float(valor)

    def incluir_procedimento(self, descricao: str, custo: float,
                             profissional: ProfissionalSaude) -> Procedimento:
        if not self.__clinica.possui_profissional(profissional):
            raise ProfissionalNaoVinculadoException(
                f"{profissional.nome} não está vinculado(a) à clínica {self.__clinica.nome}.")
        # O próprio atendimento cria o procedimento (composição).
        procedimento = Procedimento(descricao, custo, profissional)
        self.__procedimentos.append(procedimento)
        return procedimento

    def alterar_procedimento(self, procedimento: Procedimento, descricao: str, custo: float,
                             profissional: ProfissionalSaude):
        self.__verifica_procedimento(procedimento)
        Procedimento(descricao, custo, profissional)  # valida os dados antes de alterar
        if not self.__clinica.possui_profissional(profissional):
            raise ProfissionalNaoVinculadoException(
                f"{profissional.nome} não está vinculado(a) à clínica {self.__clinica.nome}.")
        if self.valor_total() - procedimento.custo + custo < self.valor_pago():
            raise ValorExcedenteException("O novo custo deixaria o total menor do que o já pago.")
        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.profissional = profissional

    def excluir_procedimento(self, procedimento: Procedimento):
        self.__verifica_procedimento(procedimento)
        if self.valor_total() - procedimento.custo < self.valor_pago():
            raise ValorExcedenteException(
                "Excluir esse procedimento deixaria o total menor do que o já pago.")
        self.__procedimentos.remove(procedimento)

    def incluir_pagamento(self, pagamento: Pagamento):
        if not isinstance(pagamento, Pagamento):
            raise TypeError("Pagamento inválido.")
        if pagamento.atendimento is not self:
            raise ValueError("O pagamento pertence a outro atendimento.")
        if pagamento.data > self.__data:
            raise PagamentoForaDoPrazoException()
        if pagamento.valor_pago > self.valor_restante():
            raise ValorExcedenteException(
                f"O valor restante é R$ {self.valor_restante():.2f}.")
        self.__pagamentos.append(pagamento)

    def alterar_pagamento(self, pagamento: Pagamento, data: date, valor_pago: float):
        self.__verifica_pagamento(pagamento)
        if not isinstance(data, date):
            raise TypeError("A data do pagamento deve ser uma data.")
        if data > self.__data:
            raise PagamentoForaDoPrazoException()
        if not isinstance(valor_pago, (int, float)) or valor_pago <= 0:
            raise ValueError("O valor pago deve ser maior que zero.")
        restante_sem_esse = self.valor_restante() + pagamento.valor_pago
        if valor_pago > restante_sem_esse:
            raise ValorExcedenteException(f"O valor máximo para esse pagamento é R$ {restante_sem_esse:.2f}.")
        pagamento.data = data
        pagamento.valor_pago = valor_pago

    def excluir_pagamento(self, pagamento: Pagamento):
        self.__verifica_pagamento(pagamento)
        self.__pagamentos.remove(pagamento)

    def valor_total(self) -> float:
        return round(self.__valor + self.__custo_procedimentos(), 2)

    def valor_pago(self) -> float:
        # Polimorfismo: soma qualquer modalidade de pagamento sem saber qual é.
        return round(sum(pagamento.valor_pago for pagamento in self.__pagamentos), 2)

    def valor_restante(self) -> float:
        return round(self.valor_total() - self.valor_pago(), 2)

    def __custo_procedimentos(self) -> float:
        return sum(procedimento.custo for procedimento in self.__procedimentos)

    def __verifica_procedimento(self, procedimento: Procedimento):
        if procedimento not in self.__procedimentos:
            raise NaoEncontradoException("Procedimento não encontrado nesse atendimento.")

    def __verifica_pagamento(self, pagamento: Pagamento):
        if pagamento not in self.__pagamentos:
            raise NaoEncontradoException("Pagamento não encontrado nesse atendimento.")
