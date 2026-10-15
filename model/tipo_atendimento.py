class TipoAtendimento:
    def __init__(self, nome: str, descricao: str):
        self.nome = nome
        self.descricao = descricao

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome do tipo de atendimento não pode ser vazio.")
        self.__nome = nome.strip()

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser um texto.")
        self.__descricao = descricao.strip()
