from model.paciente import Paciente
from view.tela_paciente import TelaPaciente
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.cadastro_duplicado_exception import CadastroDuplicadoException
from exceptions.paciente_menor_sem_responsavel_exception import PacienteMenorSemResponsavelException


class ControladorPacientes:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__pacientes = []
        self.__tela_paciente = TelaPaciente()

    @property
    def pacientes(self) -> list:
        return list(self.__pacientes)

    def pega_paciente_por_cpf(self, cpf: str) -> Paciente:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        raise NaoEncontradoException(f"Nenhum paciente cadastrado com o CPF {cpf}.")

    def incluir_paciente(self):
        dados = self.__tela_paciente.pega_dados_paciente()
        if any(paciente.cpf == dados["cpf"] for paciente in self.__pacientes):
            raise CadastroDuplicadoException(f"Já existe um paciente com o CPF {dados['cpf']}.")
        try:
            paciente = Paciente(dados["nome"], dados["cpf"], dados["celular"], dados["data_nascimento"])
        except PacienteMenorSemResponsavelException:
            # Regra 1: menor de 18 anos só é atendido com um responsável maior de idade.
            responsavel = self.pega_paciente_por_cpf(self.__tela_paciente.seleciona_responsavel())
            paciente = Paciente(dados["nome"], dados["cpf"], dados["celular"],
                                dados["data_nascimento"], responsavel)
        self.__pacientes.append(paciente)
        self.__tela_paciente.mostra_mensagem("Paciente cadastrado com sucesso.")

    def alterar_paciente(self):
        paciente = self.pega_paciente_por_cpf(self.__tela_paciente.seleciona_paciente())
        self.__tela_paciente.mostra_paciente(paciente.exibir_dados())
        dados = self.__tela_paciente.pega_dados_paciente(incluir_cpf=False)
        antigos = (paciente.nome, paciente.celular, paciente.data_nascimento, paciente.responsavel)
        try:
            paciente.nome = dados["nome"]
            paciente.celular = dados["celular"]
            paciente.data_nascimento = dados["data_nascimento"]
            responsavel = None
            if not paciente.maior_de_idade():
                if self.__eh_responsavel(paciente):
                    raise ValueError("Esse paciente é responsável por outro paciente e precisa ser maior de idade.")
                responsavel = self.pega_paciente_por_cpf(self.__tela_paciente.seleciona_responsavel())
            paciente.responsavel = responsavel
        except (ValueError, TypeError, NaoEncontradoException, PacienteMenorSemResponsavelException):
            # Desfaz a alteração para o paciente não ficar com dados inconsistentes.
            paciente.nome, paciente.celular, paciente.data_nascimento = antigos[:3]
            paciente.responsavel = antigos[3]
            raise
        self.__tela_paciente.mostra_mensagem("Paciente alterado com sucesso.")

    def excluir_paciente(self):
        paciente = self.pega_paciente_por_cpf(self.__tela_paciente.seleciona_paciente())
        if self.__controlador_sistema.controlador_atendimentos.possui_referencia(paciente):
            self.__tela_paciente.mostra_mensagem("Não é possível excluir: o paciente possui atendimentos.")
            return
        if self.__eh_responsavel(paciente):
            self.__tela_paciente.mostra_mensagem("Não é possível excluir: o paciente é responsável por outro paciente.")
            return
        self.__pacientes.remove(paciente)
        self.__tela_paciente.mostra_mensagem("Paciente excluído com sucesso.")

    def listar_pacientes(self):
        if not self.__pacientes:
            self.__tela_paciente.mostra_mensagem("Nenhum paciente cadastrado.")
            return
        for paciente in self.__pacientes:
            self.__tela_paciente.mostra_paciente(paciente.exibir_dados())

    def abre_tela(self):
        opcoes = {
            1: self.incluir_paciente,
            2: self.alterar_paciente,
            3: self.excluir_paciente,
            4: self.listar_pacientes,
        }
        while True:
            opcao = self.__tela_paciente.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (NaoEncontradoException, CadastroDuplicadoException,
                    PacienteMenorSemResponsavelException, ValueError, TypeError) as erro:
                self.__tela_paciente.mostra_mensagem(f"Erro: {erro}")

    def __eh_responsavel(self, paciente: Paciente) -> bool:
        return any(outro.responsavel is paciente for outro in self.__pacientes)
