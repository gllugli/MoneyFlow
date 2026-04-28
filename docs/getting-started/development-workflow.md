# Fluxo de desenvolvimento

Este documento resume o fluxo mais comum para trabalhar no MoneyFlow no dia a dia.

## Rotina recomendada

### 1. Ative o ambiente virtual

No Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Se preferir não ativar o ambiente virtual, use diretamente:

```powershell
.venv\Scripts\python.exe manage.py runserver
.venv\Scripts\python.exe manage.py test
```

### 2. Suba o servidor Django

```bash
python manage.py runserver
```

### 3. Rode o watcher do Tailwind quando estiver alterando a interface

```bash
npm run watch:css
```

Isso é especialmente útil quando você altera:

- templates em `apps/**/*.html`
- classes utilitárias em Python ou templates
- o arquivo `assets/css/app.css`

### 4. Aplique migrações quando o modelo mudar

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Rode os testes mais relevantes para a sua alteração

```bash
python manage.py test
```

Ou execute apenas uma área específica:

```bash
python manage.py test apps.core.tests
python manage.py test apps.movements.tests
```

## Quando reconstruir o CSS

Rode `npm run build:css` ou `npm run watch:css` quando houver mudança em:

- `assets/css/app.css`
- `apps/core/templates/core/dashboard.html`
- `apps/movements/templates/movements/movement_list.html`
- `apps/movements/templates/movements/movement_form.html`
- qualquer arquivo novo dentro dos caminhos monitorados pelo Tailwind

## Fluxo por tipo de alteração

### Alteração de backend simples

Exemplos:

- ajuste em view
- regra no formulário
- mudança de contexto do template

Fluxo comum:

1. editar o código
2. rodar o teste mais próximo
3. validar a tela manualmente

### Alteração de modelo

Exemplos:

- novo campo em `Movement`
- mudança de tipo de dado

Fluxo comum:

1. editar `models.py`
2. rodar `python manage.py makemigrations`
3. revisar a migração gerada
4. rodar `python manage.py migrate`
5. executar testes relacionados

### Alteração de interface

Exemplos:

- novo card no dashboard
- ajuste de layout ou classes CSS
- mudança de formulário

Fluxo comum:

1. editar template ou CSS-fonte
2. rodar `npm run build:css` ou `npm run watch:css`
3. validar a renderização no navegador
4. rodar os testes afetados

## Ferramentas centrais do projeto

- Django para backend, templates, rotas e admin
- SQLite para persistência local
- Tailwind CSS para estilos
- JavaScript embutido nos templates para interações pequenas, como máscara monetária e modal de exclusão

## Leituras relacionadas

- [`local-setup.md`](local-setup.md)
- [`troubleshooting.md`](troubleshooting.md)
- [`../reference/testing.md`](../reference/testing.md)
