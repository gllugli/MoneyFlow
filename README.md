# MoneyFlow

Aplicacao web de controle financeiro pessoal desenvolvida com Django para a disciplina de Inteligencia Artificial do Centro Universitario de Brasilia. O projeto permite registrar entradas e saidas, acompanhar saldo e consultar um painel com metricas mensais, historico recente e comparativos visuais.

## Principais funcionalidades

- Cadastro de movimentacoes financeiras com descricao, tipo, valor e data
- Dashboard inicial com saldo atual, entradas, saidas, ticket medio e comparativos mensais
- Historico completo de movimentacoes com ordenacao cronologica
- Edicao e exclusao de registros com confirmacao em modal
- Interface em portugues com mascara monetaria em BRL
- Area administrativa do Django para gerenciar registros

## Sumario

- [Visao geral](#visao-geral)
- [Tech stack](#tech-stack)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como a aplicacao funciona](#como-a-aplicacao-funciona)
- [Modelo de dados](#modelo-de-dados)
- [Pre-requisitos](#pre-requisitos)
- [Como executar localmente](#como-executar-localmente)
- [Comandos uteis](#comandos-uteis)
- [Testes](#testes)
- [Frontend e CSS](#frontend-e-css)
- [Configuracao atual](#configuracao-atual)
- [Deploy](#deploy)
- [Limitacoes conhecidas](#limitacoes-conhecidas)
- [Licenca](#licenca)

## Visao geral

O MoneyFlow e uma aplicacao Django pequena e objetiva, voltada para o registro manual de movimentacoes financeiras pessoais. A experiencia principal hoje se divide em dois fluxos:

1. Registrar entradas e saidas
2. Ler os dados em um painel executivo e em uma lista historica

As telas atuais disponiveis sao:

- `/` - dashboard principal
- `/movements/` - historico e resumo das movimentacoes
- `/movements/nova/` - cadastro de nova movimentacao
- `/movements/<id>/editar/` - edicao de uma movimentacao existente
- `/movements/<id>/excluir/` - exclusao via `POST`
- `/admin/` - painel administrativo padrao do Django

## Tech stack

- **Linguagem**: Python 3.11
- **Framework backend**: Django 5.2.13
- **Banco de dados**: SQLite
- **Frontend**: Django Templates + HTML + JavaScript embutido
- **Estilos**: Tailwind CSS 3.4.17
- **Build de assets**: `npm`
- **Idioma da interface**: Portugues do Brasil (`pt-BR`)

## Estrutura do projeto

```text
MoneyFlow/
|- apps/
|  |- core/
|  |  |- templates/core/
|  |  |- tests.py
|  |  |- urls.py
|  |  `- views.py
|  |- movements/
|  |  |- migrations/
|  |  |- templates/movements/
|  |  |- admin.py
|  |  |- forms.py
|  |  |- models.py
|  |  |- tests.py
|  |  |- urls.py
|  |  `- views.py
|  `- accounts/
|- assets/
|  `- css/app.css
|- config/
|  |- settings.py
|  |- urls.py
|  |- asgi.py
|  `- wsgi.py
|- static/
|  `- css/app.css
|- manage.py
|- package.json
`- tailwind.config.js
```

### Responsabilidade de cada parte

- `config/`: configuracao global do Django, URLs raiz e entrypoints ASGI/WSGI
- `apps/core/`: dashboard principal
- `apps/movements/`: modelo principal, formulario, CRUD e testes da area financeira
- `apps/accounts/`: app ainda nao conectado ao projeto
- `assets/css/app.css`: arquivo fonte do Tailwind
- `static/css/app.css`: CSS gerado para uso em runtime

## Como a aplicacao funciona

### 1. Dashboard

A pagina inicial usa `DashboardView` em `apps/core/views.py` para calcular e renderizar:

- saldo total acumulado
- entradas e saidas totais
- recorte do mes atual
- comparacao com o mes anterior
- serie resumida dos ultimos 6 meses
- maiores entradas e saidas do mes
- atividade por dia da semana
- lista de movimentacoes recentes

Essas leituras sao montadas a partir de agregacoes do ORM do Django sobre o modelo `Movement`.

### 2. Historico de movimentacoes

A tela `apps/movements/templates/movements/movement_list.html` mostra:

- tabela com todas as movimentacoes
- totais de entradas e saidas
- quantidade total de registros
- saldo final agregado
- acoes de editar e excluir

Os registros sao ordenados por data decrescente e, em caso de empate, por identificador decrescente.

### 3. Cadastro e edicao

O formulario em `apps/movements/forms.py` aplica algumas regras importantes:

- o valor e informado como texto para permitir mascara monetaria
- entradas e saidas sao definidas por `movement_type`
- apenas valores positivos sao aceitos
- o campo aceita formatos como `1500.00` e `R$ 1.234,56`
- a data recebe o dia atual por padrao quando apropriado

### 4. Exclusao

A exclusao e feita por `POST`, usando `MovementDeleteView`, com um modal de confirmacao no frontend. Requisicoes `GET` para a rota de exclusao nao sao permitidas.

### 5. Admin Django

O modelo `Movement` esta registrado no admin com:

- listagem por descricao, tipo, valor e data
- filtros por tipo e data
- busca por descricao

## Modelo de dados

Hoje o projeto possui um modelo de dominio efetivamente utilizado.

### `Movement`

Arquivo: `apps/movements/models.py`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `description` | `CharField(255)` | Nome da movimentacao |
| `movement_type` | `CharField` | Tipo da movimentacao: `credit` ou `debit` |
| `value` | `DecimalField(12, 2)` | Valor monetario positivo |
| `date` | `DateField` | Data da movimentacao |

### Regras de negocio observadas

- `credit` representa entrada
- `debit` representa saida
- o saldo e calculado como `total_credit - total_debit`
- os registros mais recentes aparecem primeiro

## Pre-requisitos

Antes de iniciar, tenha instalado:

- Python 3.11 ou superior
- `pip`
- Node.js 18 ou superior
- `npm`

Observacao importante: o repositorio **nao possui hoje** `requirements.txt` nem `pyproject.toml`. Portanto, a instalacao Python abaixo usa a versao do Django observada no ambiente atual do projeto.

## Como executar localmente

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd MoneyFlow
```

### 2. Criar um ambiente virtual Python

No Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

No macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias Python

```bash
pip install "Django==5.2.13"
```

Se quiser confirmar a instalacao:

```bash
python -m django --version
```

### 4. Instalar dependencias de frontend

```bash
npm install
```

### 5. Aplicar migracoes

```bash
python manage.py migrate
```

Isso cria o banco SQLite local e aplica a estrutura atual do app `movements`.

### 6. Gerar o CSS do projeto

```bash
npm run build:css
```

### 7. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

A aplicacao ficara disponivel em `http://127.0.0.1:8000/`.

### 8. Opcional: criar usuario administrador

```bash
python manage.py createsuperuser
```

Depois disso, acesse `http://127.0.0.1:8000/admin/`.

## Comandos uteis

| Comando | Descricao |
| --- | --- |
| `python manage.py runserver` | Inicia o servidor local |
| `python manage.py migrate` | Aplica migracoes pendentes |
| `python manage.py makemigrations` | Gera novas migracoes a partir de alteracoes nos modelos |
| `python manage.py check` | Executa verificacoes do Django |
| `python manage.py shell` | Abre shell com o contexto do projeto |
| `python manage.py createsuperuser` | Cria usuario para acesso ao admin |
| `python manage.py test` | Executa toda a suite de testes |
| `npm run build:css` | Gera o CSS compilado do Tailwind |
| `npm run watch:css` | Reconstroi o CSS continuamente durante o desenvolvimento |

Se voce estiver no Windows e preferir usar diretamente o Python do ambiente virtual sem ativacao:

```powershell
.venv\Scripts\python.exe manage.py runserver
.venv\Scripts\python.exe manage.py test
```

## Testes

O projeto usa o test runner nativo do Django.

### Rodar todos os testes

```bash
python manage.py test
```

### Rodar apenas os testes do dashboard

```bash
python manage.py test apps.core.tests
```

### Rodar apenas os testes de movimentacoes

```bash
python manage.py test apps.movements.tests
```

### Rodar um caso especifico

```bash
python manage.py test apps.movements.tests.MovementListViewTests
python manage.py test apps.movements.tests.MovementListViewTests.test_movement_list_page_returns_success
```

### O que a suite cobre hoje

- renderizacao das paginas principais
- links da navegacao
- criacao, edicao e exclusao de movimentacoes
- ordenacao do historico
- calculo de totais, saldo e metricas do dashboard
- suporte a entrada monetaria mascarada

## Frontend e CSS

O projeto usa Tailwind CSS com configuracao em `tailwind.config.js`.

### Fluxo atual

- fonte de estilos: `assets/css/app.css`
- saida compilada: `static/css/app.css`
- templates carregam o CSS compilado com `{% static 'css/app.css' %}`

### Scripts disponiveis

```bash
npm run build:css
npm run watch:css
```

### Onde o Tailwind procura classes

- `apps/**/*.html`
- `apps/**/*.py`
- `config/**/*.py`

Sempre que alterar classes utilitarias, templates ou estilos-base, gere novamente o CSS antes de subir a aplicacao.

## Configuracao atual

O estado atual do projeto e orientado a desenvolvimento local.

### Banco de dados

- o backend usa SQLite
- o arquivo local esperado e `db.sqlite3`
- esse arquivo esta ignorado no Git

### Settings relevantes

Em `config/settings.py`, hoje temos:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `LANGUAGE_CODE = 'pt-br'`
- `TIME_ZONE = 'UTC'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`

### Variaveis de ambiente

O projeto nao usa, por enquanto, um arquivo `.env` nem um modulo dedicado para configuracao por ambiente. A `SECRET_KEY` esta definida diretamente em `config/settings.py`, o que e aceitavel para um projeto academico/local, mas nao e recomendado para producao.

## Deploy

O repositorio **nao possui hoje** configuracao pronta de deploy, como:

- `Dockerfile`
- `docker-compose.yml`
- `Procfile`
- pipeline de CI/CD
- separacao formal entre configuracoes de desenvolvimento e producao

### O que seria necessario antes de publicar em producao

1. Externalizar `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS`
2. Criar um manifesto de dependencias Python (`requirements.txt` ou `pyproject.toml`)
3. Definir estrategia de banco de dados para producao
4. Configurar `collectstatic` e servir arquivos estaticos corretamente
5. Adicionar verificacoes de seguranca e uma rotina de deploy repetivel

### Exemplo minimo de checklist manual

```bash
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
npm run build:css
```

## Limitacoes conhecidas

- nao ha autenticacao de usuario final na interface principal
- o app `apps.accounts` existe, mas ainda nao esta ligado em `INSTALLED_APPS` nem nas rotas
- nao existe manifesto versionado de dependencias Python
- nao ha configuracao de deploy automatizado
- o banco padrao e SQLite, adequado para desenvolvimento e demonstracao local

## Licenca

Este projeto esta sob a licenca MIT. Consulte `LICENSE` para os detalhes completos.
