# Testes

O projeto usa o test runner nativo do Django.

## Base atual da suíte

Os testes ficam principalmente em:

- `apps/core/tests.py`
- `apps/movements/tests.py`

## Como executar

### Todos os testes

```bash
python manage.py test
```

### Apenas os testes do dashboard

```bash
python manage.py test apps.core.tests
```

### Apenas os testes de movimentações

```bash
python manage.py test apps.movements.tests
```

### Uma classe específica

```bash
python manage.py test apps.core.tests.DashboardViewTests
```

### Um método específico

```bash
python manage.py test apps.movements.tests.MovementListViewTests.test_movement_list_page_returns_success
```

## O que a suíte cobre hoje

### `apps.core.tests`

Valida, entre outros pontos:

- resposta `200` do dashboard
- uso do template correto
- presença de links de navegação
- renderização de métricas financeiras
- cálculo de dados mensais e séries usadas pela interface

### `apps.movements.tests`

Valida, entre outros pontos:

- renderização da listagem
- ordenação por data mais recente
- estado vazio da tabela
- totais e saldo final
- criação de movimentação
- aceitação de valor mascarado em BRL
- edição de movimentação
- exclusão por `POST`
- bloqueio de exclusão por `GET`

## Estilo de teste observado

O padrão atual usa fortemente:

- `django.test.TestCase`
- `self.client`
- `reverse`
- `assertContains`
- `assertTemplateUsed`
- `assertRedirects`
- inspeção de `response.context`

## Cuidados ao alterar comportamento

Se você mudar:

- textos da interface
- nomes de links ou botões
- valores exibidos nas páginas
- estrutura das views

é provável que precise ajustar testes existentes.

## Observação de manutenção

Há indícios de descompasso pontual entre parte dos textos esperados nos testes do dashboard e a interface renderizada no template atual. Em caso de falha, revise tanto a expectativa do teste quanto o texto real da página antes de decidir a correção.

## Leituras relacionadas

- [`commands.md`](commands.md)
- [`routes.md`](routes.md)
- [`../getting-started/development-workflow.md`](../getting-started/development-workflow.md)
