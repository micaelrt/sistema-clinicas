from view.tela_abstrata import TelaAbstrata


class TelaProfissional(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("PROFISSIONAIS DE SAÚDE", {
            1: "Incluir profissional",
            2: "Alterar profissional",
            3: "Excluir profissional",
            4: "Listar profissionais",
            0: "Voltar",
        })

    def pega_dados_profissional(self, incluir_cpf: bool = True) -> dict:
        print("\n-------- DADOS DO PROFISSIONAL --------")
        dados = {}
        if incluir_cpf:
            dados["cpf"] = self.le_cpf("CPF: ")
        dados["nome"] = self.le_texto("Nome: ")
        dados["celular"] = self.le_texto("Celular: ")
        dados["data_nascimento"] = self.le_data("Data de nascimento (DD/MM/AAAA): ")
        dados["especialidade"] = self.le_texto("Especialidade: ")
        dados["registro_profissional"] = self.le_texto("Registro profissional (CRM, COREN etc.): ")
        return dados

    def seleciona_profissional(self) -> str:
        return self.le_cpf("CPF do profissional: ")

    def mostra_profissional(self, dados: str):
        print(dados)
