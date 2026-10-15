from abc import ABC, abstractmethod
from datetime import date, time, datetime


class TelaAbstrata(ABC):
    @abstractmethod
    def tela_opcoes(self) -> int:
        pass

    def le_num_inteiro(self, mensagem: str, opcoes_validas: list = None) -> int:
        while True:
            valor_lido = input(mensagem)
            try:
                numero = int(valor_lido)
                if opcoes_validas is not None and numero not in opcoes_validas:
                    raise ValueError
                return numero
            except ValueError:
                if opcoes_validas is not None:
                    print(f"Valor inválido. Opções válidas: {', '.join(map(str, opcoes_validas))}")
                else:
                    print("Valor inválido. Digite um número inteiro.")

    def le_texto(self, mensagem: str, obrigatorio: bool = True) -> str:
        while True:
            texto = input(mensagem).strip()
            if texto or not obrigatorio:
                return texto
            print("Este campo é obrigatório.")

    def le_cpf(self, mensagem: str) -> str:
        while True:
            cpf = "".join(caractere for caractere in input(mensagem) if caractere.isdigit())
            if len(cpf) == 11:
                return cpf
            print("CPF inválido. Digite os 11 dígitos (pontos e traço são opcionais).")

    def le_data(self, mensagem: str) -> date:
        while True:
            try:
                return datetime.strptime(input(mensagem).strip(), "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida. Use o formato DD/MM/AAAA.")

    def le_hora(self, mensagem: str) -> time:
        while True:
            try:
                return datetime.strptime(input(mensagem).strip(), "%H:%M").time()
            except ValueError:
                print("Hora inválida. Use o formato HH:MM.")

    def le_valor(self, mensagem: str) -> float:
        while True:
            try:
                valor = float(input(mensagem).strip().replace(",", "."))
                if valor < 0:
                    raise ValueError
                return valor
            except ValueError:
                print("Valor inválido. Digite um número maior ou igual a zero (ex.: 150,00).")

    def mostra_mensagem(self, mensagem: str):
        print(mensagem)

    def _mostra_menu(self, titulo: str, opcoes: dict) -> int:
        print(f"\n-------- {titulo} --------")
        for numero, descricao in opcoes.items():
            print(f"{numero} - {descricao}")
        return self.le_num_inteiro("Escolha a opção: ", list(opcoes.keys()))
