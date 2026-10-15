from view.tela_abstrata import TelaAbstrata


class TelaAtendimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("ATENDIMENTOS E PROCEDIMENTOS", {
            1: "Incluir atendimento",
            2: "Alterar atendimento",
            3: "Excluir atendimento",
            4: "Listar atendimentos",
            5: "Incluir procedimento em um atendimento",
            6: "Alterar procedimento",
            7: "Excluir procedimento",
            8: "Listar procedimentos de um atendimento",
            0: "Voltar",
        })

    def pega_dados_atendimento(self) -> dict:
        print("\n-------- DADOS DO ATENDIMENTO --------")
        return {
            "nome_clinica": self.le_texto("Nome da clínica: "),
            "cpf_paciente": self.le_cpf("CPF do paciente: "),
            "cpf_profissional": self.le_cpf("CPF do profissional: "),
            "nome_tipo": self.le_texto("Tipo de atendimento: "),
            "data": self.le_data("Data (DD/MM/AAAA): "),
            "hora_inicio": self.le_hora("Hora de início (HH:MM): "),
            "hora_fim": self.le_hora("Hora de fim (HH:MM): "),
            "valor": self.le_valor("Valor do atendimento (R$): "),
        }

    def seleciona_atendimento(self) -> int:
        return self.le_num_inteiro("Código do atendimento: ")

    def mostra_atendimento(self, dados: dict):
        print(f"\nAtendimento #{dados['codigo']} | {dados['tipo']} | "
              f"{dados['data'].strftime('%d/%m/%Y')} das {dados['hora_inicio'].strftime('%H:%M')} "
              f"às {dados['hora_fim'].strftime('%H:%M')}")
        print(f"Clínica: {dados['clinica']} | Paciente: {dados['paciente']} | "
              f"Profissional: {dados['profissional']}")
        print(f"Valor: R$ {dados['valor']:.2f} | Procedimentos: {dados['qtd_procedimentos']} | "
              f"Total: R$ {dados['valor_total']:.2f} | Pago: R$ {dados['valor_pago']:.2f} | "
              f"Restante: R$ {dados['valor_restante']:.2f}")

    def pega_dados_procedimento(self) -> dict:
        print("\n-------- DADOS DO PROCEDIMENTO --------")
        return {
            "descricao": self.le_texto("Descrição: "),
            "custo": self.le_valor("Custo (R$): "),
            "cpf_profissional": self.le_cpf("CPF do profissional responsável: "),
        }

    def seleciona_procedimento(self, quantidade: int) -> int:
        numero = self.le_num_inteiro("Número do procedimento: ", list(range(1, quantidade + 1)))
        return numero - 1

    def mostra_procedimentos(self, procedimentos: list):
        print("\n-------- PROCEDIMENTOS --------")
        for numero, dados in enumerate(procedimentos, start=1):
            print(f"{numero} - {dados['descricao']} | Custo: R$ {dados['custo']:.2f} | "
                  f"Responsável: {dados['profissional']}")
