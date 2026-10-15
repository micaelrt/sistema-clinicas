from model.atendimento import Atendimento
from model.pagamento import Pagamento
from model.pagamento_dinheiro import PagamentoDinheiro
from model.pagamento_pix import PagamentoPix
from model.pagamento_cartao import PagamentoCartao
from view.tela_pagamento import TelaPagamento
from exceptions.nao_encontrado_exception import NaoEncontradoException
from exceptions.pagamento_fora_do_prazo_exception import PagamentoForaDoPrazoException
from exceptions.valor_excedente_exception import ValorExcedenteException


class ControladorPagamentos:
    def __init__(self, controlador_sistema):
        # Não guarda lista própria: os pagamentos ficam dentro de cada Atendimento (composição).
        self.__controlador_sistema = controlador_sistema
        self.__tela_pagamento = TelaPagamento()

    def incluir_pagamento(self):
        atendimento = self.__seleciona_atendimento()
        self.__tela_pagamento.mostra_resumo_atendimento(self.__resumo(atendimento))
        if atendimento.valor_restante() <= 0:
            self.__tela_pagamento.mostra_mensagem("Esse atendimento já está quitado.")
            return
        modalidade = self.__tela_pagamento.seleciona_modalidade()
        dados = self.__tela_pagamento.pega_dados_pagamento()
        if modalidade == 1:
            pagamento = PagamentoDinheiro(dados["data"], dados["valor_pago"], atendimento)
        elif modalidade == 2:
            pagamento = PagamentoPix(dados["data"], dados["valor_pago"], atendimento,
                                     self.__tela_pagamento.pega_cpf_pagador())
        else:
            cartao = self.__tela_pagamento.pega_dados_cartao()
            pagamento = PagamentoCartao(dados["data"], dados["valor_pago"], atendimento,
                                        cartao["numero_cartao"], cartao["bandeira"])
        atendimento.incluir_pagamento(pagamento)
        self.__tela_pagamento.mostra_mensagem(
            f"Pagamento registrado. Valor restante: R$ {atendimento.valor_restante():.2f}")

    def alterar_pagamento(self):
        atendimento = self.__seleciona_atendimento()
        pagamento = self.__seleciona_pagamento(atendimento)
        dados = self.__tela_pagamento.pega_dados_pagamento()
        atendimento.alterar_pagamento(pagamento, dados["data"], dados["valor_pago"])
        self.__tela_pagamento.mostra_mensagem(
            f"Pagamento alterado. Valor restante: R$ {atendimento.valor_restante():.2f}")

    def excluir_pagamento(self):
        atendimento = self.__seleciona_atendimento()
        pagamento = self.__seleciona_pagamento(atendimento)
        atendimento.excluir_pagamento(pagamento)
        self.__tela_pagamento.mostra_mensagem(
            f"Pagamento excluído. Valor restante: R$ {atendimento.valor_restante():.2f}")

    def listar_pagamentos(self):
        atendimentos = self.__controlador_sistema.controlador_atendimentos.atendimentos
        if not atendimentos:
            self.__tela_pagamento.mostra_mensagem("Nenhum atendimento cadastrado.")
            return
        for atendimento in atendimentos:
            self.__tela_pagamento.mostra_resumo_atendimento(self.__resumo(atendimento))
            self.__tela_pagamento.mostra_pagamentos(self.__dados_pagamentos(atendimento))

    def abre_tela(self):
        opcoes = {
            1: self.incluir_pagamento,
            2: self.alterar_pagamento,
            3: self.excluir_pagamento,
            4: self.listar_pagamentos,
        }
        while True:
            opcao = self.__tela_pagamento.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (NaoEncontradoException, PagamentoForaDoPrazoException,
                    ValorExcedenteException, ValueError, TypeError) as erro:
                self.__tela_pagamento.mostra_mensagem(f"Erro: {erro}")

    def __seleciona_atendimento(self) -> Atendimento:
        codigo = self.__tela_pagamento.seleciona_atendimento()
        return self.__controlador_sistema.controlador_atendimentos.pega_atendimento_por_codigo(codigo)

    def __seleciona_pagamento(self, atendimento: Atendimento) -> Pagamento:
        pagamentos = atendimento.pagamentos
        if not pagamentos:
            raise NaoEncontradoException("Esse atendimento não possui pagamentos.")
        self.__tela_pagamento.mostra_pagamentos(self.__dados_pagamentos(atendimento))
        return pagamentos[self.__tela_pagamento.seleciona_pagamento(len(pagamentos))]

    def __resumo(self, atendimento: Atendimento) -> dict:
        return {
            "codigo": atendimento.codigo,
            "paciente": atendimento.paciente.nome,
            "data": atendimento.data,
            "valor_total": atendimento.valor_total(),
            "valor_pago": atendimento.valor_pago(),
            "valor_restante": atendimento.valor_restante(),
        }

    def __dados_pagamentos(self, atendimento: Atendimento) -> list:
        return [{"data": pagamento.data,
                 "valor_pago": pagamento.valor_pago,
                 "modalidade": pagamento.modalidade(),
                 "paciente": pagamento.paciente().nome}
                for pagamento in atendimento.pagamentos]
