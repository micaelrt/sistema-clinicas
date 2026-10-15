# Sistema de Clínicas

Trabalho 1 de INE5605 (Desenvolvimento de Sistemas Orientados a Objetos I), UFSC 2026.2.

Sistema em Python para gerenciar clínicas, profissionais de saúde, pacientes, atendimentos,
procedimentos e pagamentos. Os dados ficam em memória e a interface é pelo terminal.

## Como executar

```
python main.py
```

Requer Python 3.10 ou superior. Não usa bibliotecas externas.

## Organização (MVC)

- `model/`: entidades e regras de negócio (`Pessoa`, `Paciente`, `ProfissionalSaude`, `Clinica`,
  `TipoAtendimento`, `Atendimento`, `Procedimento`, `Pagamento` e suas modalidades)
- `view/`: telas de terminal (`TelaAbstrata` e uma tela por módulo)
- `controller/`: controladores que ligam as telas ao modelo (`ControladorSistema` e um por módulo)
- `exceptions/`: exceções das regras de negócio
- `docs/diagrama_classes.drawio`: diagrama de classes UML

## Regras implementadas

1. Paciente menor de 18 anos precisa de um responsável maior de idade (`PacienteMenorSemResponsavelException`).
2. O atendimento deve ocorrer dentro do horário de funcionamento da clínica (`HorarioForaDoFuncionamentoException`).
3. O pagamento deve ser feito até a data do atendimento (`PagamentoForaDoPrazoException`).
4. Pagamentos em dinheiro, PIX (com CPF do pagador) ou cartão de crédito (com número e bandeira), com
   pagamento parcial e cálculo do valor restante (`ValorExcedenteException` impede pagar além do devido).

O profissional precisa estar vinculado à clínica para atender nela (`ProfissionalNaoVinculadoException`).
