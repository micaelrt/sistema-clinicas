from view.tela_relatorio import TelaRelatorio


class ControladorRelatorios:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_relatorio = TelaRelatorio()

    def clinicas_com_mais_atendimentos(self):
        clinicas = self.__controlador_sistema.controlador_clinicas.clinicas
        if not clinicas:
            self.__tela_relatorio.mostra_mensagem("Nenhuma clínica cadastrada.")
            return
        atendimentos = self.__atendimentos()
        contagem = [(clinica, sum(1 for atendimento in atendimentos if atendimento.clinica is clinica))
                    for clinica in clinicas]
        contagem.sort(key=lambda item: item[1], reverse=True)
        linhas = [f"{posicao}º {clinica.nome} ({clinica.cidade}): {quantidade} atendimento(s)"
                  for posicao, (clinica, quantidade) in enumerate(contagem, start=1)]
        self.__tela_relatorio.mostra_relatorio("CLÍNICAS COM MAIS ATENDIMENTOS", linhas)

    def atendimentos_mais_caros_e_baratos(self):
        atendimentos = self.__atendimentos()
        if not atendimentos:
            self.__tela_relatorio.mostra_mensagem("Nenhum atendimento cadastrado.")
            return
        maior = max(atendimento.valor_total() for atendimento in atendimentos)
        menor = min(atendimento.valor_total() for atendimento in atendimentos)
        linhas = [f"Mais caro(s): R$ {maior:.2f}"]
        linhas += [f"  {self.__descreve_atendimento(atendimento)}" for atendimento in atendimentos
                   if atendimento.valor_total() == maior]
        linhas.append(f"Mais barato(s): R$ {menor:.2f}")
        linhas += [f"  {self.__descreve_atendimento(atendimento)}" for atendimento in atendimentos
                   if atendimento.valor_total() == menor]
        linhas.append("Todos, do mais caro ao mais barato:")
        linhas += [f"  R$ {atendimento.valor_total():.2f} | {self.__descreve_atendimento(atendimento)}"
                   for atendimento in sorted(atendimentos, key=lambda a: a.valor_total(), reverse=True)]
        self.__tela_relatorio.mostra_relatorio("ATENDIMENTOS MAIS CAROS E MAIS BARATOS", linhas)

    def procedimentos_mais_realizados(self):
        procedimentos = self.__procedimentos()
        if not procedimentos:
            self.__tela_relatorio.mostra_mensagem("Nenhum procedimento registrado.")
            return
        # Agrupa pela descrição, sem diferenciar maiúsculas de minúsculas.
        contagem = {}
        for _, procedimento in procedimentos:
            chave = procedimento.descricao.casefold()
            nome, quantidade = contagem.get(chave, (procedimento.descricao, 0))
            contagem[chave] = (nome, quantidade + 1)
        ranking = sorted(contagem.values(), key=lambda item: item[1], reverse=True)
        linhas = [f"{posicao}º {nome}: realizado {quantidade} vez(es)"
                  for posicao, (nome, quantidade) in enumerate(ranking, start=1)]
        self.__tela_relatorio.mostra_relatorio("PROCEDIMENTOS MAIS REALIZADOS", linhas)

    def procedimentos_mais_caros_e_baratos(self):
        procedimentos = self.__procedimentos()
        if not procedimentos:
            self.__tela_relatorio.mostra_mensagem("Nenhum procedimento registrado.")
            return
        maior = max(procedimento.custo for _, procedimento in procedimentos)
        menor = min(procedimento.custo for _, procedimento in procedimentos)
        linhas = [f"Mais caro(s): R$ {maior:.2f}"]
        linhas += [f"  {procedimento.descricao} (atendimento #{atendimento.codigo}, {procedimento.profissional.nome})"
                   for atendimento, procedimento in procedimentos if procedimento.custo == maior]
        linhas.append(f"Mais barato(s): R$ {menor:.2f}")
        linhas += [f"  {procedimento.descricao} (atendimento #{atendimento.codigo}, {procedimento.profissional.nome})"
                   for atendimento, procedimento in procedimentos if procedimento.custo == menor]
        self.__tela_relatorio.mostra_relatorio("PROCEDIMENTOS MAIS CAROS E MAIS BARATOS", linhas)

    def abre_tela(self):
        opcoes = {
            1: self.clinicas_com_mais_atendimentos,
            2: self.atendimentos_mais_caros_e_baratos,
            3: self.procedimentos_mais_realizados,
            4: self.procedimentos_mais_caros_e_baratos,
        }
        while True:
            opcao = self.__tela_relatorio.tela_opcoes()
            if opcao == 0:
                return
            opcoes[opcao]()

    def __atendimentos(self) -> list:
        return self.__controlador_sistema.controlador_atendimentos.atendimentos

    def __procedimentos(self) -> list:
        return [(atendimento, procedimento) for atendimento in self.__atendimentos()
                for procedimento in atendimento.procedimentos]

    def __descreve_atendimento(self, atendimento) -> str:
        return (f"#{atendimento.codigo} {atendimento.tipo.nome} | {atendimento.paciente.nome} | "
                f"{atendimento.clinica.nome} | {atendimento.data.strftime('%d/%m/%Y')}")
