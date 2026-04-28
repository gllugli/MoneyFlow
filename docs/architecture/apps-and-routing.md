# Apps e roteamento

Este documento descreve como o projeto organiza seus apps e como as rotas são distribuídas.

## Apps instalados

No estado atual, `config/settings.py` instala apenas:

- `apps.core.apps.CoreConfig`
- `apps.movements.apps.MovementsConfig`

Isso significa que a aplicação funcional disponível para navegação se concentra nessas duas áreas.

## Roteamento raiz

O arquivo `config/urls.py` expõe três entradas principais:

- `/admin/` — administração padrão do Django
- `/movements/` — módulo de movimentações
- `/` — dashboard principal

## App `core`

### Objetivo

`apps.core` concentra a home do sistema e o template-base compartilhado.

### Rota do app

Em `apps/core/urls.py`:

- `""` -> `DashboardView` -> nome `core:dashboard`

### Fluxo funcional

Ao acessar `/`, a `DashboardView`:

1. consulta todas as movimentações
2. calcula saldo total
3. separa o mês atual e o mês anterior
4. monta a série dos últimos seis meses
5. calcula tickets, maiores valores e indicadores do período
6. renderiza `core/dashboard.html`

## App `movements`

### Objetivo

`apps.movements` reúne o domínio financeiro principal do projeto.

### Rotas do app

Em `apps/movements/urls.py`:

- `""` -> `MovementListView` -> nome `movements:movement_list`
- `"nova/"` -> `MovementCreateView` -> nome `movements:movement_create`
- `"<int:pk>/editar/"` -> `MovementUpdateView` -> nome `movements:movement_update`
- `"<int:pk>/excluir/"` -> `MovementDeleteView` -> nome `movements:movement_delete`

### Fluxo de listagem

`MovementListView`:

- carrega as movimentações em ordem decrescente de data e id
- calcula total de entradas
- calcula total de saídas
- calcula saldo final
- exibe ações de edição e exclusão

### Fluxo de criação

`MovementCreateView`:

- renderiza o formulário `MovementForm`
- injeta textos de apoio e últimos registros
- salva a movimentação válida
- adiciona mensagem de sucesso
- redireciona para a listagem

### Fluxo de edição

`MovementUpdateView`:

- reutiliza o mesmo template do formulário
- pré-carrega os dados existentes
- reaplica a formatação monetária na exibição
- salva as alterações
- adiciona mensagem de sucesso

### Fluxo de exclusão

`MovementDeleteView`:

- aceita apenas `POST`
- remove o registro selecionado
- mostra mensagem de sucesso
- bloqueia requisições `GET`

## Navegação compartilhada

O template `apps/core/templates/base.html` mantém a navegação principal entre:

- dashboard
- histórico de movimentações
- criação de nova movimentação

## Considerações de arquitetura

- o projeto usa namespaces de URL (`core:` e `movements:`)
- a aplicação depende de descoberta de templates por app, já que `TEMPLATES['DIRS']` está vazio
- não há uma camada separada de API; a navegação é toda server-rendered

## Leituras relacionadas

- [`overview.md`](overview.md)
- [`../reference/routes.md`](../reference/routes.md)
- [`../product/feature-overview.md`](../product/feature-overview.md)
