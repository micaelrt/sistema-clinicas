from view.tela_abstrata import TelaAbstrata


class TelaRelatorio(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._mostra_menu("RELATÓRIOS", {
            1: "Clínicas com maior número de atendimentos",
            2: "Atendimentos mais caros e mais baratos",
            3: "Procedimentos mais realizados",
            4: "Procedimentos mais caros e mais baratos",
            0: "Voltar",
        })

    def mostra_relatorio(self, titulo: str, linhas: list):
        print(f"\n======== {titulo} ========")
        for linha in linhas:
            print(linha)
