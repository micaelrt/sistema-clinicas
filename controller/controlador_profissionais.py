from model.profissional_saude import ProfissionalSaude
from view.tela_profissional import TelaProfissional
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.cadastro_duplicado_exception import CadastroDuplicadoException


class ControladorProfissionais:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__profissionais = []
        self.__tela_profissional = TelaProfissional()

    @property
    def profissionais(self) -> list:
        return list(self.__profissionais)

    def pega_profissional_por_cpf(self, cpf: str) -> ProfissionalSaude:
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        raise NaoEncontradoException(f"Nenhum profissional cadastrado com o CPF {cpf}.")

    def incluir_profissional(self):
        dados = self.__tela_profissional.pega_dados_profissional()
        if any(profissional.cpf == dados["cpf"] for profissional in self.__profissionais):
            raise CadastroDuplicadoException(f"Já existe um profissional com o CPF {dados['cpf']}.")
        profissional = ProfissionalSaude(dados["nome"], dados["cpf"], dados["celular"],
                                         dados["data_nascimento"], dados["especialidade"],
                                         dados["registro_profissional"])
        self.__profissionais.append(profissional)
        self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso.")

    def alterar_profissional(self):
        profissional = self.pega_profissional_por_cpf(self.__tela_profissional.seleciona_profissional())
        self.__tela_profissional.mostra_profissional(profissional.exibir_dados())
        dados = self.__tela_profissional.pega_dados_profissional(incluir_cpf=False)
        # Valida todos os dados antes de alterar o objeto real.
        ProfissionalSaude(dados["nome"], profissional.cpf, dados["celular"], dados["data_nascimento"],
                          dados["especialidade"], dados["registro_profissional"])
        profissional.nome = dados["nome"]
        profissional.celular = dados["celular"]
        profissional.data_nascimento = dados["data_nascimento"]
        profissional.especialidade = dados["especialidade"]
        profissional.registro_profissional = dados["registro_profissional"]
        self.__tela_profissional.mostra_mensagem("Profissional alterado com sucesso.")

    def excluir_profissional(self):
        profissional = self.pega_profissional_por_cpf(self.__tela_profissional.seleciona_profissional())
        if self.__controlador_sistema.controlador_atendimentos.possui_referencia(profissional):
            self.__tela_profissional.mostra_mensagem(
                "Não é possível excluir: o profissional possui atendimentos ou procedimentos.")
            return
        clinicas = [clinica.nome for clinica in self.__controlador_sistema.controlador_clinicas.clinicas
                    if clinica.possui_profissional(profissional)]
        if clinicas:
            self.__tela_profissional.mostra_mensagem(
                f"Não é possível excluir: desvincule o profissional das clínicas {', '.join(clinicas)}.")
            return
        self.__profissionais.remove(profissional)
        self.__tela_profissional.mostra_mensagem("Profissional excluído com sucesso.")

    def listar_profissionais(self):
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado.")
            return
        for profissional in self.__profissionais:
            self.__tela_profissional.mostra_profissional(profissional.exibir_dados())

    def abre_tela(self):
        opcoes = {
            1: self.incluir_profissional,
            2: self.alterar_profissional,
            3: self.excluir_profissional,
            4: self.listar_profissionais,
        }
        while True:
            opcao = self.__tela_profissional.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (NaoEncontradoException, CadastroDuplicadoException, ValueError, TypeError) as erro:
                self.__tela_profissional.mostra_mensagem(f"Erro: {erro}")
