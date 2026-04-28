# Visão funcional

Este documento descreve as funcionalidades implementadas no MoneyFlow e como elas se comportam do ponto de vista do usuário.

## Objetivo do produto

O sistema permite registrar manualmente movimentações financeiras pessoais e acompanhar o efeito dessas movimentações em um painel com leituras consolidadas.

## Funcionalidades disponíveis

### 1. Dashboard principal

Rota:

- `/`

O dashboard mostra:

- saldo atual acumulado
- entradas do mês
- saídas do mês
- ticket médio do mês
- resultado líquido atual
- comparação com o mês anterior
- dias ativos com movimentações
- data do último registro
- gráfico de entradas e saídas dos últimos seis meses
- lista de movimentações recentes

## 2. Histórico de movimentações

Rota:

- `/movements/`

A tela de histórico oferece:

- tabela com todos os lançamentos
- total de entradas
- total de saídas
- quantidade de registros
- saldo final agregado
- ação de editar
- ação de excluir com confirmação

## 3. Cadastro de movimentação

Rota:

- `/movements/nova/`

O formulário permite informar:

- descrição
- tipo da movimentação
- valor
- data

Comportamentos relevantes:

- o valor usa máscara monetária em BRL
- o valor precisa ser positivo
- o tipo define se o valor entra ou sai do saldo
- a data pode vir preenchida com o dia atual

## 4. Edição de movimentação

Rota:

- `/movements/<id>/editar/`

O fluxo de edição reutiliza o mesmo formulário de cadastro, mas:

- carrega os dados já existentes
- formata o valor para exibição monetária
- apresenta textos específicos de edição

## 5. Exclusão de movimentação

Rota:

- `/movements/<id>/excluir/`

Comportamento:

- só aceita `POST`
- exige confirmação pela interface
- remove o registro do histórico
- atualiza a listagem após sucesso

## 6. Administração do Django

Rota:

- `/admin/`

O admin permite:

- listar movimentações
- filtrar por tipo e data
- buscar por descrição
- visualizar e manter registros diretamente pelo painel administrativo

## Fluxo principal do usuário

Hoje a jornada principal é:

1. registrar uma entrada ou saída
2. voltar para o histórico e conferir o lançamento
3. acompanhar o impacto no dashboard
4. editar ou excluir lançamentos quando necessário

## Limitações funcionais atuais

- não há autenticação de usuário final na interface principal
- não existe separação de dados por usuário
- não há categorias de movimentação
- não existe importação automática de extrato
- não há integração bancária

## Leituras relacionadas

- [`../architecture/data-model.md`](../architecture/data-model.md)
- [`../reference/routes.md`](../reference/routes.md)
- [`../reference/testing.md`](../reference/testing.md)
