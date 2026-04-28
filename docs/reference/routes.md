# Rotas disponíveis

Esta página resume as rotas públicas observadas no projeto.

## Rotas principais

| Método | Rota | Nome | Responsabilidade |
| --- | --- | --- | --- |
| `GET` | `/` | `core:dashboard` | Exibe o dashboard principal |
| `GET` | `/movements/` | `movements:movement_list` | Lista as movimentações e seus totais |
| `GET`, `POST` | `/movements/nova/` | `movements:movement_create` | Cria uma nova movimentação |
| `GET`, `POST` | `/movements/<id>/editar/` | `movements:movement_update` | Edita uma movimentação existente |
| `POST` | `/movements/<id>/excluir/` | `movements:movement_delete` | Exclui uma movimentação |
| `GET`, `POST` | `/admin/` | admin do Django | Administração padrão do framework |

## Observações importantes

### Dashboard

- usa `DashboardView`
- depende do modelo `Movement` para todas as métricas exibidas

### Listagem de movimentações

- usa `MovementListView`
- agrega total de entradas, total de saídas, quantidade de registros e saldo final

### Criação e edição

- reutilizam o mesmo template de formulário
- usam `MovementForm` para validação e normalização de valor monetário

### Exclusão

- usa `MovementDeleteView`
- aceita apenas `POST`
- responde com `405 Method Not Allowed` para `GET`

## Namespaces de URL

O projeto usa namespaces para evitar colisões e facilitar reversão de URL:

- `core`
- `movements`

## Leituras relacionadas

- [`configuration.md`](configuration.md)
- [`testing.md`](testing.md)
- [`../architecture/apps-and-routing.md`](../architecture/apps-and-routing.md)
