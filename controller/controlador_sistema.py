import sys

from controller.controlador_pacientes import ControladorPacientes
from controller.controlador_profissionais import ControladorProfissionais
from controller.controlador_clinicas import ControladorClinicas
from controller.controlador_tipos_atendimento import ControladorTiposAtendimento
from controller.controlador_atendimentos import ControladorAtendimentos
from controller.controlador_pagamentos import ControladorPagamentos
from controller.controlador_relatorios import ControladorRelatorios
from view.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_profissionais = ControladorProfissionais(self)
        self.__controlador_clinicas = ControladorClinicas(self)
        self.__controlador_tipos_atendimento = ControladorTiposAtendimento(self)
        self.__controlador_atendimentos = ControladorAtendimentos(self)
        self.__controlador_pagamentos = ControladorPagamentos(self)
        self.__controlador_relatorios = ControladorRelatorios(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_pacientes(self) -> ControladorPacientes:
        return self.__controlador_pacientes

    @property
    def controlador_profissionais(self) -> ControladorProfissionais:
        return self.__controlador_profissionais

    @property
    def controlador_clinicas(self) -> ControladorClinicas:
        return self.__controlador_clinicas

    @property
    def controlador_tipos_atendimento(self) -> ControladorTiposAtendimento:
        return self.__controlador_tipos_atendimento

    @property
    def controlador_atendimentos(self) -> ControladorAtendimentos:
        return self.__controlador_atendimentos

    @property
    def controlador_pagamentos(self) -> ControladorPagamentos:
        return self.__controlador_pagamentos

    @property
    def controlador_relatorios(self) -> ControladorRelatorios:
        return self.__controlador_relatorios

    def inicializa_sistema(self):
        self.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.__controlador_pacientes.abre_tela,
            2: self.__controlador_profissionais.abre_tela,
            3: self.__controlador_clinicas.abre_tela,
            4: self.__controlador_tipos_atendimento.abre_tela,
            5: self.__controlador_atendimentos.abre_tela,
            6: self.__controlador_pagamentos.abre_tela,
            7: self.__controlador_relatorios.abre_tela,
            0: self.encerra_sistema,
        }
        while True:
            opcoes[self.__tela_sistema.tela_opcoes()]()

    def encerra_sistema(self):
        self.__tela_sistema.mostra_mensagem("Sistema encerrado.")
        sys.exit(0)
