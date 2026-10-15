from view.tela_abstrata import TelaAbstrata


class TelaTipoAtendimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("TIPOS DE ATENDIMENTO", {
            1: "Incluir tipo",
            2: "Alterar tipo",
            3: "Excluir tipo",
            4: "Listar tipos",
            0: "Voltar",
        })

    def pega_dados_tipo(self) -> dict:
        print("\n-------- DADOS DO TIPO DE ATENDIMENTO --------")
        return {
            "nome": self.le_texto("Nome (ex.: Consulta, Exame, Retorno): "),
            "descricao": self.le_texto("Descrição: ", obrigatorio=False),
        }

    def seleciona_tipo(self) -> str:
        return self.le_texto("Nome do tipo de atendimento: ")

    def mostra_tipo(self, dados: dict):
        print(f"Tipo: {dados['nome']} | Descrição: {dados['descricao'] or '-'}")
