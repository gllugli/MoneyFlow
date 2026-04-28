# Frontend e assets

O frontend do MoneyFlow é server-rendered com Django Templates e usa Tailwind CSS como base de estilos.

## Estrutura de frontend

Os principais arquivos atuais são:

- `apps/core/templates/base.html`
- `apps/core/templates/core/dashboard.html`
- `apps/movements/templates/movements/movement_list.html`
- `apps/movements/templates/movements/movement_form.html`
- `assets/css/app.css`
- `static/css/app.css`
- `tailwind.config.js`

## Template-base

`apps/core/templates/base.html` define:

- estrutura HTML principal
- idioma da página como `pt-BR`
- carregamento do CSS compilado com `{% static 'css/app.css' %}`
- navegação global
- pilha de mensagens do Django
- blocos de conteúdo e JavaScript adicional

## Páginas principais

### Dashboard

`apps/core/templates/core/dashboard.html` renderiza:

- banner do mês
- cards de KPI
- gráfico comparativo de seis meses
- pulso do resultado
- lista de movimentações recentes

### Histórico

`apps/movements/templates/movements/movement_list.html` renderiza:

- resumo de totais
- tabela com movimentações
- ações de edição e exclusão
- modal de confirmação para remoção

### Formulário

`apps/movements/templates/movements/movement_form.html` renderiza:

- campos do `MovementForm`
- mensagens de erro por campo
- CTA de salvar
- painel lateral com registros recentes

## Interações em JavaScript

O projeto não usa framework frontend. As interações atuais são pequenas e embutidas nos próprios templates.

### Máscara monetária

No formulário de movimentação, o JavaScript:

- captura o campo com `data-currency-input`
- formata o valor com `Intl.NumberFormat('pt-BR', { currency: 'BRL' })`
- mantém a experiência visual em moeda brasileira

### Modal de exclusão

Na listagem, o JavaScript:

- abre o modal ao clicar em excluir
- fecha por botão de cancelar, clique no backdrop ou tecla `Escape`
- devolve foco ao botão original quando o modal é fechado

## Pipeline de CSS

### Fonte

- `assets/css/app.css`

### Saída compilada

- `static/css/app.css`

### Scripts disponíveis

```bash
npm run build:css
npm run watch:css
```

## Como o Tailwind encontra classes

Em `tailwind.config.js`, os caminhos monitorados são:

- `./apps/**/*.html`
- `./apps/**/*.py`
- `./config/**/*.py`

## Paleta e identidade visual observadas

O tema atual usa tons quentes e neutros com destaque em verde, incluindo cores como:

- `shell`
- `ink`
- `accent`
- `income`
- `expense`
- `wheat`

Também há extensões para:

- sombras customizadas
- raios de borda específicos
- famílias tipográficas serifadas e sans-serif

## Cuidados ao alterar a interface

- sempre reconstrua o CSS após alterar classes ou templates
- lembre que a suíte de testes valida alguns textos visíveis
- preserve a consistência entre o contexto da view e o template renderizado

## Leituras relacionadas

- [`overview.md`](overview.md)
- [`../reference/configuration.md`](../reference/configuration.md)
- [`../getting-started/development-workflow.md`](../getting-started/development-workflow.md)
