from view.tela_abstrata import TelaAbstrata


class TelaPaciente(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("PACIENTES", {
            1: "Incluir paciente",
            2: "Alterar paciente",
            3: "Excluir paciente",
            4: "Listar pacientes",
            0: "Voltar",
        })

    def pega_dados_paciente(self, incluir_cpf: bool = True) -> dict:
        print("\n-------- DADOS DO PACIENTE --------")
        dados = {}
        if incluir_cpf:
            dados["cpf"] = self.le_cpf("CPF: ")
        dados["nome"] = self.le_texto("Nome: ")
        dados["celular"] = self.le_texto("Celular: ")
        dados["data_nascimento"] = self.le_data("Data de nascimento (DD/MM/AAAA): ")
        return dados

    def seleciona_paciente(self) -> str:
        return self.le_cpf("CPF do paciente: ")

    def seleciona_responsavel(self) -> str:
        return self.le_cpf("Paciente menor de idade. CPF do responsável (paciente adulto já cadastrado): ")

    def mostra_paciente(self, dados: str):
        print(dados)
