from model.atendimento import Atendimento
from model.procedimento import Procedimento
from view.tela_atendimento import TelaAtendimento
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.paciente_menor_sem_responsavel_exception import PacienteMenorSemResponsavelException
from exceptions.horario_fora_do_funcionamento_exception import HorarioForaDoFuncionamentoException
from exceptions.profissional_nao_vinculado_exception import ProfissionalNaoVinculadoException
from exceptions.pagamento_fora_do_prazo_exception import PagamentoForaDoPrazoException
from exceptions.valor_excedente_exception import ValorExcedenteException


class ControladorAtendimentos:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__atendimentos = []
        self.__proximo_codigo = 1
        self.__tela_atendimento = TelaAtendimento()

    @property
    def atendimentos(self) -> list:
        return list(self.__atendimentos)

    def pega_atendimento_por_codigo(self, codigo: int) -> Atendimento:
        for atendimento in self.__atendimentos:
            if atendimento.codigo == codigo:
                return atendimento
        raise NaoEncontradoException(f"Nenhum atendimento com o código {codigo}.")

    def possui_referencia(self, objeto) -> bool:
        for atendimento in self.__atendimentos:
            if objeto in (atendimento.clinica, atendimento.paciente,
                          atendimento.profissional, atendimento.tipo):
                return True
            if any(procedimento.profissional is objeto for procedimento in atendimento.procedimentos):
                return True
        return False

    def incluir_atendimento(self):
        dados = self.__tela_atendimento.pega_dados_atendimento()
        clinica, paciente, profissional, tipo = self.__busca_relacionados(dados)
        atendimento = Atendimento(self.__proximo_codigo, clinica, paciente, profissional, tipo,
                                  dados["data"], dados["hora_inicio"], dados["hora_fim"], dados["valor"])
        self.__atendimentos.append(atendimento)
        self.__proximo_codigo += 1
        self.__tela_atendimento.mostra_mensagem(
            f"Atendimento cadastrado com sucesso. Código: {atendimento.codigo}")

    def alterar_atendimento(self):
        atendimento = self.pega_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())
        self.__tela_atendimento.mostra_atendimento(self.__dados_atendimento(atendimento))
        dados = self.__tela_atendimento.pega_dados_atendimento()
        clinica, paciente, profissional, tipo = self.__busca_relacionados(dados)
        atendimento.alterar_dados(clinica, paciente, profissional, tipo, dados["data"],
                                  dados["hora_inicio"], dados["hora_fim"], dados["valor"])
        self.__tela_atendimento.mostra_mensagem("Atendimento alterado com sucesso.")

    def excluir_atendimento(self):
        atendimento = self.pega_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())
        # Composição: os procedimentos e pagamentos são excluídos junto com o atendimento.
        self.__atendimentos.remove(atendimento)
        self.__tela_atendimento.mostra_mensagem(
            "Atendimento excluído com sucesso (procedimentos e pagamentos dele também foram excluídos).")

    def listar_atendimentos(self):
        if not self.__atendimentos:
            self.__tela_atendimento.mostra_mensagem("Nenhum atendimento cadastrado.")
            return
        for atendimento in self.__atendimentos:
            self.__tela_atendimento.mostra_atendimento(self.__dados_atendimento(atendimento))

    def incluir_procedimento(self):
        atendimento = self.pega_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())
        dados = self.__tela_atendimento.pega_dados_procedimento()
        profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(
            dados["cpf_profissional"])
        atendimento.incluir_procedimento(dados["descricao"], dados["custo"], profissional)
        self.__tela_atendimento.mostra_mensagem("Procedimento incluído com sucesso.")

    def alterar_procedimento(self):
        atendimento = self.pega_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())
        procedimento = self.__seleciona_procedimento(atendimento)
        dados = self.__tela_atendimento.pega_dados_procedimento()
        profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(
            dados["cpf_profissional"])
        atendimento.alterar_procedimento(procedimento, dados["descricao"], dados["custo"], profissional)
        self.__tela_atendimento.mostra_mensagem("Procedimento alterado com sucesso.")

    def excluir_procedimento(self):
        atendimento = self.pega_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())
        procedimento = self.__seleciona_procedimento(atendimento)
        atendimento.excluir_procedimento(procedimento)
        self.__tela_atendimento.mostra_mensagem("Procedimento excluído com sucesso.")

    def listar_procedimentos(self):
        atendimento = self.pega_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())
        if not atendimento.procedimentos:
            self.__tela_atendimento.mostra_mensagem("Esse atendimento não possui procedimentos.")
            return
        self.__tela_atendimento.mostra_procedimentos(self.__dados_procedimentos(atendimento))

    def abre_tela(self):
        opcoes = {
            1: self.incluir_atendimento,
            2: self.alterar_atendimento,
            3: self.excluir_atendimento,
            4: self.listar_atendimentos,
            5: self.incluir_procedimento,
            6: self.alterar_procedimento,
            7: self.excluir_procedimento,
            8: self.listar_procedimentos,
        }
        while True:
            opcao = self.__tela_atendimento.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (NaoEncontradoException, PacienteMenorSemResponsavelException,
                    HorarioForaDoFuncionamentoException, ProfissionalNaoVinculadoException,
                    PagamentoForaDoPrazoException, ValorExcedenteException,
                    ValueError, TypeError) as erro:
                self.__tela_atendimento.mostra_mensagem(f"Erro: {erro}")

    def __busca_relacionados(self, dados: dict) -> tuple:
        sistema = self.__controlador_sistema
        clinica = sistema.controlador_clinicas.pega_clinica_por_nome(dados["nome_clinica"])
        paciente = sistema.controlador_pacientes.pega_paciente_por_cpf(dados["cpf_paciente"])
        profissional = sistema.controlador_profissionais.pega_profissional_por_cpf(dados["cpf_profissional"])
        tipo = sistema.controlador_tipos_atendimento.pega_tipo_por_nome(dados["nome_tipo"])
        return clinica, paciente, profissional, tipo

    def __seleciona_procedimento(self, atendimento: Atendimento) -> Procedimento:
        procedimentos = atendimento.procedimentos
        if not procedimentos:
            raise NaoEncontradoException("Esse atendimento não possui procedimentos.")
        self.__tela_atendimento.mostra_procedimentos(self.__dados_procedimentos(atendimento))
        return procedimentos[self.__tela_atendimento.seleciona_procedimento(len(procedimentos))]

    def __dados_procedimentos(self, atendimento: Atendimento) -> list:
        return [{"descricao": procedimento.descricao,
                 "custo": procedimento.custo,
                 "profissional": procedimento.profissional.nome}
                for procedimento in atendimento.procedimentos]

    def __dados_atendimento(self, atendimento: Atendimento) -> dict:
        return {
            "codigo": atendimento.codigo,
            "tipo": atendimento.tipo.nome,
            "data": atendimento.data,
            "hora_inicio": atendimento.hora_inicio,
            "hora_fim": atendimento.hora_fim,
            "clinica": atendimento.clinica.nome,
            "paciente": atendimento.paciente.nome,
            "profissional": atendimento.profissional.nome,
            "valor": atendimento.valor,
            "qtd_procedimentos": len(atendimento.procedimentos),
            "valor_total": atendimento.valor_total(),
            "valor_pago": atendimento.valor_pago(),
            "valor_restante": atendimento.valor_restante(),
        }
