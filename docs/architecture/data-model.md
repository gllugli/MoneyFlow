# Modelo de dados

O domínio efetivamente usado pelo sistema gira em torno de um único modelo: `Movement`.

## Entidade principal

### `Movement`

Arquivo:

- `apps/movements/models.py`

Campos atuais:

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `description` | `CharField(255)` | Nome ou identificação da movimentação |
| `movement_type` | `CharField(max_length=6)` | Tipo da movimentação: entrada ou saída |
| `value` | `DecimalField(12, 2)` | Valor monetário positivo |
| `date` | `DateField` | Data da movimentação |

## Tipos de movimentação

O modelo define duas opções por `TextChoices`:

- `credit` — entrada
- `debit` — saída

Na interface, esses valores são exibidos como:

- `Entrada`
- `Saída`

## Regras de negócio observadas

### Regra de sinal

O valor armazenado permanece positivo. O impacto financeiro é determinado por `movement_type`:

- `credit` soma ao saldo
- `debit` reduz o saldo

### Regra de saldo

O saldo consolidado é calculado como:

```text
saldo = total_credit - total_debit
```

### Regra de validação do valor

O formulário impede:

- valores vazios ou inválidos
- valores menores ou iguais a zero

Também aceita formatos como:

- `1500.00`
- `1.234,56`
- `R$ 1.234,56`

### Regra de ordenação

O modelo define ordenação padrão por:

1. `-date`
2. `-id`

Isso garante que os registros mais recentes apareçam primeiro, inclusive em caso de empate na data.

## Ausências importantes no modelo atual

Hoje o projeto não possui campos ou relações para:

- usuário proprietário da movimentação
- categoria financeira
- conta bancária
- centro de custo
- parcelamento
- recorrência
- anexos

## Implicações práticas

- todas as movimentações pertencem, na prática, à instância inteira da aplicação
- o sistema é adequado para demonstração local e uso simples
- uma evolução para multiusuário exigirá mudanças de modelo, views, testes e regras de acesso

## Origem das métricas do dashboard

As métricas exibidas na home são derivadas do modelo `Movement` por meio de agregações ORM, como:

- soma de entradas
- soma de saídas
- média do mês
- maiores valores do período
- agrupamento por mês

## Leituras relacionadas

- [`overview.md`](overview.md)
- [`apps-and-routing.md`](apps-and-routing.md)
- [`../product/feature-overview.md`](../product/feature-overview.md)
