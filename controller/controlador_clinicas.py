from model.clinica import Clinica
from view.tela_clinica import TelaClinica
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.cadastro_duplicado_exception import CadastroDuplicadoException
from exceptions.profissional_nao_vinculado_exception import ProfissionalNaoVinculadoException


class ControladorClinicas:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__clinicas = []
        self.__tela_clinica = TelaClinica()

    @property
    def clinicas(self) -> list:
        return list(self.__clinicas)

    def pega_clinica_por_nome(self, nome: str) -> Clinica:
        for clinica in self.__clinicas:
            if clinica.nome.casefold() == nome.strip().casefold():
                return clinica
        raise NaoEncontradoException(f"Nenhuma clínica cadastrada com o nome {nome}.")

    def incluir_clinica(self):
        dados = self.__tela_clinica.pega_dados_clinica()
        self.__verifica_nome_disponivel(dados["nome"])
        clinica = Clinica(dados["nome"], dados["cidade"], dados["descricao"],
                          dados["hora_abertura"], dados["hora_fechamento"])
        self.__clinicas.append(clinica)
        self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso.")

    def alterar_clinica(self):
        clinica = self.pega_clinica_por_nome(self.__tela_clinica.seleciona_clinica())
        dados = self.__tela_clinica.pega_dados_clinica()
        self.__verifica_nome_disponivel(dados["nome"], ignorar=clinica)
        # Valida todos os dados antes de alterar o objeto real.
        Clinica(dados["nome"], dados["cidade"], dados["descricao"],
                dados["hora_abertura"], dados["hora_fechamento"])
        clinica.nome = dados["nome"]
        clinica.cidade = dados["cidade"]
        clinica.descricao = dados["descricao"]
        clinica.alterar_horario(dados["hora_abertura"], dados["hora_fechamento"])
        self.__tela_clinica.mostra_mensagem("Clínica alterada com sucesso.")

    def excluir_clinica(self):
        clinica = self.pega_clinica_por_nome(self.__tela_clinica.seleciona_clinica())
        if self.__controlador_sistema.controlador_atendimentos.possui_referencia(clinica):
            self.__tela_clinica.mostra_mensagem("Não é possível excluir: a clínica possui atendimentos.")
            return
        # Agregação: excluir a clínica não exclui os profissionais vinculados.
        self.__clinicas.remove(clinica)
        self.__tela_clinica.mostra_mensagem("Clínica excluída com sucesso.")

    def listar_clinicas(self):
        if not self.__clinicas:
            self.__tela_clinica.mostra_mensagem("Nenhuma clínica cadastrada.")
            return
        for clinica in self.__clinicas:
            self.__tela_clinica.mostra_clinica({
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "descricao": clinica.descricao,
                "hora_abertura": clinica.hora_abertura,
                "hora_fechamento": clinica.hora_fechamento,
                "profissionais": [f"{profissional.nome} ({profissional.especialidade})"
                                  for profissional in clinica.profissionais],
            })

    def vincular_profissional(self):
        clinica = self.pega_clinica_por_nome(self.__tela_clinica.seleciona_clinica())
        cpf = self.__tela_clinica.seleciona_profissional()
        profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(cpf)
        clinica.adicionar_profissional(profissional)
        self.__tela_clinica.mostra_mensagem(f"{profissional.nome} vinculado(a) à clínica {clinica.nome}.")

    def desvincular_profissional(self):
        clinica = self.pega_clinica_por_nome(self.__tela_clinica.seleciona_clinica())
        cpf = self.__tela_clinica.seleciona_profissional()
        profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(cpf)
        clinica.remover_profissional(profissional)
        self.__tela_clinica.mostra_mensagem(f"{profissional.nome} desvinculado(a) da clínica {clinica.nome}.")

    def abre_tela(self):
        opcoes = {
            1: self.incluir_clinica,
            2: self.alterar_clinica,
            3: self.excluir_clinica,
            4: self.listar_clinicas,
            5: self.vincular_profissional,
            6: self.desvincular_profissional,
        }
        while True:
            opcao = self.__tela_clinica.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (NaoEncontradoException, CadastroDuplicadoException,
                    ProfissionalNaoVinculadoException, ValueError, TypeError) as erro:
                self.__tela_clinica.mostra_mensagem(f"Erro: {erro}")

    def __verifica_nome_disponivel(self, nome: str, ignorar: Clinica = None):
        for clinica in self.__clinicas:
            if clinica is not ignorar and clinica.nome.casefold() == nome.strip().casefold():
                raise CadastroDuplicadoException(f"Já existe uma clínica com o nome {nome}.")
