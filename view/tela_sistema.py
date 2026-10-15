from view.tela_abstrata import TelaAbstrata


class TelaSistema(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("SISTEMA DE CLÍNICAS", {
            1: "Pacientes",
            2: "Profissionais de saúde",
            3: "Clínicas",
            4: "Tipos de atendimento",
            5: "Atendimentos e procedimentos",
            6: "Pagamentos",
            7: "Relatórios",
            0: "Sair",
        })
