# Instalação local

Este guia mostra como preparar o MoneyFlow para desenvolvimento local.

## Pré-requisitos

Antes de começar, tenha instalado:

- Python 3.11 ou superior
- `pip`
- Node.js 18 ou superior
- `npm`

## Observação importante sobre dependências Python

O repositório não possui, no estado atual, um arquivo versionado como `requirements.txt` ou `pyproject.toml`. Por isso, a instalação Python precisa seguir a versão observada no projeto.

Versão atualmente usada:

- Django 5.2.13

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd MoneyFlow
```

## 2. Criar o ambiente virtual

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS e Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar dependências Python

```bash
pip install "Django==5.2.13"
```

Para conferir a instalação:

```bash
python -m django --version
```

## 4. Instalar dependências de frontend

```bash
npm install
```

No momento, o repositório usa `tailwindcss` como dependência de desenvolvimento do pipeline de estilos.

## 5. Aplicar migrações

```bash
python manage.py migrate
```

Esse passo cria o banco local `db.sqlite3` e aplica a estrutura do app `apps.movements`.

## 6. Gerar o CSS compilado

```bash
npm run build:css
```

O arquivo-fonte fica em `assets/css/app.css` e o CSS gerado é salvo em `static/css/app.css`.

## 7. Iniciar o servidor

```bash
python manage.py runserver
```

Depois disso, a aplicação estará disponível em:

- `http://127.0.0.1:8000/`

## 8. Opcional: criar usuário administrador

```bash
python manage.py createsuperuser
```

O painel administrativo ficará disponível em:

- `http://127.0.0.1:8000/admin/`

## Sequência rápida

Se você só quer subir o projeto rapidamente, a sequência mínima é:

```bash
pip install "Django==5.2.13"
npm install
python manage.py migrate
npm run build:css
python manage.py runserver
```

## Próximas leituras

- [`development-workflow.md`](development-workflow.md)
- [`../reference/commands.md`](../reference/commands.md)
- [`../reference/configuration.md`](../reference/configuration.md)
