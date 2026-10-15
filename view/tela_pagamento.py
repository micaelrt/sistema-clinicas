from view.tela_abstrata import TelaAbstrata


class TelaPagamento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("PAGAMENTOS", {
            1: "Incluir pagamento",
            2: "Alterar pagamento",
            3: "Excluir pagamento",
            4: "Listar pagamentos",
            0: "Voltar",
        })

    def seleciona_atendimento(self) -> int:
        return self.le_num_inteiro("Código do atendimento: ")

    def seleciona_modalidade(self) -> int:
        print("\nModalidade: 1 - Dinheiro | 2 - PIX | 3 - Cartão de crédito")
        return self.le_num_inteiro("Escolha a modalidade: ", [1, 2, 3])

    def pega_dados_pagamento(self) -> dict:
        return {
            "data": self.le_data("Data do pagamento (DD/MM/AAAA): "),
            "valor_pago": self.le_valor("Valor pago (R$): "),
        }

    def pega_cpf_pagador(self) -> str:
        return self.le_cpf("CPF do pagador: ")

    def pega_dados_cartao(self) -> dict:
        while True:
            numero = "".join(caractere for caractere in input("Número do cartão: ") if caractere.isdigit())
            if 13 <= len(numero) <= 19:
                break
            print("Número inválido. O cartão deve ter entre 13 e 19 dígitos.")
        return {"numero_cartao": numero, "bandeira": self.le_texto("Bandeira: ")}

    def seleciona_pagamento(self, quantidade: int) -> int:
        numero = self.le_num_inteiro("Número do pagamento: ", list(range(1, quantidade + 1)))
        return numero - 1

    def mostra_resumo_atendimento(self, dados: dict):
        print(f"\nAtendimento #{dados['codigo']} | Paciente: {dados['paciente']} | "
              f"Data: {dados['data'].strftime('%d/%m/%Y')}")
        print(f"Total: R$ {dados['valor_total']:.2f} | Pago: R$ {dados['valor_pago']:.2f} | "
              f"Restante: R$ {dados['valor_restante']:.2f}")

    def mostra_pagamentos(self, pagamentos: list):
        if not pagamentos:
            print("Nenhum pagamento registrado.")
            return
        for numero, dados in enumerate(pagamentos, start=1):
            print(f"  {numero} - {dados['data'].strftime('%d/%m/%Y')} | R$ {dados['valor_pago']:.2f} | "
                  f"{dados['modalidade']} | Paciente: {dados['paciente']}")
