from view.tela_abstrata import TelaAbstrata


class TelaClinica(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("CLÍNICAS", {
            1: "Incluir clínica",
            2: "Alterar clínica",
            3: "Excluir clínica",
            4: "Listar clínicas",
            5: "Vincular profissional à clínica",
            6: "Desvincular profissional da clínica",
            0: "Voltar",
        })

    def pega_dados_clinica(self) -> dict:
        print("\n-------- DADOS DA CLÍNICA --------")
        return {
            "nome": self.le_texto("Nome: "),
            "cidade": self.le_texto("Cidade: "),
            "descricao": self.le_texto("Descrição: ", obrigatorio=False),
            "hora_abertura": self.le_hora("Hora de abertura (HH:MM): "),
            "hora_fechamento": self.le_hora("Hora de fechamento (HH:MM): "),
        }

    def seleciona_clinica(self) -> str:
        return self.le_texto("Nome da clínica: ")

    def seleciona_profissional(self) -> str:
        return self.le_cpf("CPF do profissional: ")

    def mostra_clinica(self, dados: dict):
        print(f"\nClínica: {dados['nome']} | Cidade: {dados['cidade']}")
        print(f"Descrição: {dados['descricao'] or '-'}")
        print(f"Funcionamento: {dados['hora_abertura'].strftime('%H:%M')} às "
              f"{dados['hora_fechamento'].strftime('%H:%M')}")
        if dados["profissionais"]:
            print("Profissionais: " + "; ".join(dados["profissionais"]))
        else:
            print("Profissionais: nenhum vinculado")
