from model.tipo_atendimento import TipoAtendimento
from view.tela_tipo_atendimento import TelaTipoAtendimento
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.cadastro_duplicado_exception import CadastroDuplicadoException


class ControladorTiposAtendimento:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tipos = []
        self.__tela_tipo_atendimento = TelaTipoAtendimento()

    @property
    def tipos(self) -> list:
        return list(self.__tipos)

    def pega_tipo_por_nome(self, nome: str) -> TipoAtendimento:
        for tipo in self.__tipos:
            if tipo.nome.casefold() == nome.strip().casefold():
                return tipo
        raise NaoEncontradoException(f"Nenhum tipo de atendimento cadastrado com o nome {nome}.")

    def incluir_tipo(self):
        dados = self.__tela_tipo_atendimento.pega_dados_tipo()
        self.__verifica_nome_disponivel(dados["nome"])
        self.__tipos.append(TipoAtendimento(dados["nome"], dados["descricao"]))
        self.__tela_tipo_atendimento.mostra_mensagem("Tipo de atendimento cadastrado com sucesso.")

    def alterar_tipo(self):
        tipo = self.pega_tipo_por_nome(self.__tela_tipo_atendimento.seleciona_tipo())
        dados = self.__tela_tipo_atendimento.pega_dados_tipo()
        self.__verifica_nome_disponivel(dados["nome"], ignorar=tipo)
        tipo.nome = dados["nome"]
        tipo.descricao = dados["descricao"]
        self.__tela_tipo_atendimento.mostra_mensagem("Tipo de atendimento alterado com sucesso.")

    def excluir_tipo(self):
        tipo = self.pega_tipo_por_nome(self.__tela_tipo_atendimento.seleciona_tipo())
        if self.__controlador_sistema.controlador_atendimentos.possui_referencia(tipo):
            self.__tela_tipo_atendimento.mostra_mensagem(
                "Não é possível excluir: existem atendimentos desse tipo.")
            return
        self.__tipos.remove(tipo)
        self.__tela_tipo_atendimento.mostra_mensagem("Tipo de atendimento excluído com sucesso.")

    def listar_tipos(self):
        if not self.__tipos:
            self.__tela_tipo_atendimento.mostra_mensagem("Nenhum tipo de atendimento cadastrado.")
            return
        for tipo in self.__tipos:
            self.__tela_tipo_atendimento.mostra_tipo({"nome": tipo.nome, "descricao": tipo.descricao})

    def abre_tela(self):
        opcoes = {
            1: self.incluir_tipo,
            2: self.alterar_tipo,
            3: self.excluir_tipo,
            4: self.listar_tipos,
        }
        while True:
            opcao = self.__tela_tipo_atendimento.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (NaoEncontradoException, CadastroDuplicadoException, ValueError, TypeError) as erro:
                self.__tela_tipo_atendimento.mostra_mensagem(f"Erro: {erro}")

    def __verifica_nome_disponivel(self, nome: str, ignorar: TipoAtendimento = None):
        for tipo in self.__tipos:
            if tipo is not ignorar and tipo.nome.casefold() == nome.strip().casefold():
                raise CadastroDuplicadoException(f"Já existe um tipo de atendimento com o nome {nome}.")
