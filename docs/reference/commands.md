# Comandos de referência

Esta página reúne os comandos mais úteis para trabalhar com o projeto.

## Execução local

```bash
python manage.py runserver
```

Inicia o servidor de desenvolvimento do Django.

## Migrações

### Aplicar migrações

```bash
python manage.py migrate
```

### Gerar migrações

```bash
python manage.py makemigrations
```

## Verificações do Django

```bash
python manage.py check
```

## Shell do projeto

```bash
python manage.py shell
```

## Criar superusuário

```bash
python manage.py createsuperuser
```

## Testes

### Suíte completa

```bash
python manage.py test
```

### Apenas o app `core`

```bash
python manage.py test apps.core.tests
```

### Apenas o app `movements`

```bash
python manage.py test apps.movements.tests
```

### Uma classe específica

```bash
python manage.py test apps.movements.tests.MovementListViewTests
```

### Um método específico

```bash
python manage.py test apps.movements.tests.MovementListViewTests.test_movement_list_page_returns_success
```

### Filtrar por nome

```bash
python manage.py test apps.movements.tests -k create
```

### Parar na primeira falha

```bash
python manage.py test --failfast
```

### Reutilizar o banco de testes

```bash
python manage.py test --keepdb
```

### Mais detalhes na saída

```bash
python manage.py test --verbosity 2
```

## Frontend

### Instalar dependências de frontend

```bash
npm install
```

### Gerar CSS uma vez

```bash
npm run build:css
```

### Rodar watcher do Tailwind

```bash
npm run watch:css
```

## Comandos úteis para produção manual

```bash
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
npm run build:css
```

## Atalhos úteis no Windows

Sem ativar a virtualenv:

```powershell
.venv\Scripts\python.exe manage.py runserver
.venv\Scripts\python.exe manage.py test
```

## Leituras relacionadas

- [`configuration.md`](configuration.md)
- [`testing.md`](testing.md)
- [`../getting-started/local-setup.md`](../getting-started/local-setup.md)
