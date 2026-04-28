# MoneyFlow

Aplicação web de controle financeiro pessoal desenvolvida com Django para a disciplina de Inteligência Artificial do Centro Universitário de Brasília. O projeto permite registrar entradas e saídas, acompanhar saldo e consultar um painel com métricas mensais, histórico recente e comparativos visuais.

## Principais funcionalidades

- Cadastro de movimentações financeiras com descrição, tipo, valor e data
- Dashboard inicial com saldo atual, entradas, saídas, ticket médio e comparativos mensais
- Histórico completo de movimentações com ordenação cronológica
- Edição e exclusão de registros com confirmação em modal
- Interface em português com máscara monetária em BRL
- Área administrativa do Django para gerenciar registros

## Sumário

- [Visão geral](#visão-geral)
- [Tech stack](#tech-stack)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como a aplicação funciona](#como-a-aplicação-funciona)
- [Modelo de dados](#modelo-de-dados)
- [Pré-requisitos](#pré-requisitos)
- [Como executar localmente](#como-executar-localmente)
- [Comandos úteis](#comandos-úteis)
- [Testes](#testes)
- [Frontend e CSS](#frontend-e-css)
- [Configuração atual](#configuração-atual)
- [Deploy](#deploy)
- [Limitações conhecidas](#limitações-conhecidas)
- [Licença](#licença)

## Visão geral

O MoneyFlow é uma aplicação Django pequena e objetiva, voltada para o registro manual de movimentações financeiras pessoais. A experiência principal hoje se divide em dois fluxos:

1. Registrar entradas e saídas
2. Ler os dados em um painel executivo e em uma lista histórica

As telas atuais disponíveis são:

- `/` - dashboard principal
- `/movements/` - histórico e resumo das movimentações
- `/movements/nova/` - cadastro de nova movimentação
- `/movements/<id>/editar/` - edição de uma movimentação existente
- `/movements/<id>/excluir/` - exclusão via `POST`
- `/admin/` - painel administrativo padrão do Django

## Tech stack

- **Linguagem**: Python 3.11
- **Framework backend**: Django 5.2.13
- **Banco de dados**: SQLite
- **Frontend**: Django Templates + HTML + JavaScript embutido
- **Estilos**: Tailwind CSS 3.4.17
- **Build de assets**: `npm`
- **Idioma da interface**: Português do Brasil (`pt-BR`)

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
|     `- views.py
|  
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

- `config/`: configuração global do Django, URLs raiz e entrypoints ASGI/WSGI
- `apps/core/`: dashboard principal
- `apps/movements/`: modelo principal, formulário, CRUD e testes da área financeira
- `assets/css/app.css`: arquivo-fonte do Tailwind
- `static/css/app.css`: CSS gerado para uso em runtime

## Como a aplicação funciona

### 1. Dashboard

A página inicial usa `DashboardView` em `apps/core/views.py` para calcular e renderizar:

- saldo total acumulado
- entradas e saídas totais
- recorte do mês atual
- comparação com o mês anterior
- série resumida dos últimos 6 meses
- maiores entradas e saídas do mês
- atividade por dia da semana
- lista de movimentações recentes

Essas leituras são montadas a partir de agregações do ORM do Django sobre o modelo `Movement`.

### 2. Histórico de movimentações

A tela `apps/movements/templates/movements/movement_list.html` mostra:

- tabela com todas as movimentações
- totais de entradas e saídas
- quantidade total de registros
- saldo final agregado
- ações de editar e excluir

Os registros são ordenados por data decrescente e, em caso de empate, por identificador decrescente.

### 3. Cadastro e edição

O formulário em `apps/movements/forms.py` aplica algumas regras importantes:

- o valor é informado como texto para permitir máscara monetária
- entradas e saídas são definidas por `movement_type`
- apenas valores positivos são aceitos
- o campo aceita formatos como `1500.00` e `R$ 1.234,56`
- a data recebe o dia atual por padrão quando apropriado

### 4. Exclusão

A exclusão é feita por `POST`, usando `MovementDeleteView`, com um modal de confirmação no frontend. Requisições `GET` para a rota de exclusão não são permitidas.

### 5. Admin Django

O modelo `Movement` está registrado no admin com:

- listagem por descrição, tipo, valor e data
- filtros por tipo e data
- busca por descrição

## Modelo de dados

Hoje o projeto possui um modelo de domínio efetivamente utilizado.

### `Movement`

Arquivo: `apps/movements/models.py`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `description` | `CharField(255)` | Nome da movimentação |
| `movement_type` | `CharField` | Tipo da movimentação: `credit` ou `debit` |
| `value` | `DecimalField(12, 2)` | Valor monetário positivo |
| `date` | `DateField` | Data da movimentação |

### Regras de negócio observadas

- `credit` representa entrada
- `debit` representa saída
- o saldo é calculado como `total_credit - total_debit`
- os registros mais recentes aparecem primeiro

## Pré-requisitos

Antes de iniciar, tenha instalado:

- Python 3.11 ou superior
- `pip`
- Node.js 18 ou superior
- `npm`

Observação importante: o repositório **não possui hoje** `requirements.txt` nem `pyproject.toml`. Portanto, a instalação Python abaixo usa a versão do Django observada no ambiente atual do projeto.

## Como executar localmente

### 1. Clonar o repositório

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

### 3. Instalar dependências Python

```bash
pip install "Django==5.2.13"
```

Se quiser confirmar a instalação:

```bash
python -m django --version
```

### 4. Instalar dependências de frontend

```bash
npm install
```

### 5. Aplicar migrações

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

A aplicação ficará disponível em `http://127.0.0.1:8000/`.

### 8. Opcional: criar usuário administrador

```bash
python manage.py createsuperuser
```

Depois disso, acesse `http://127.0.0.1:8000/admin/`.

## Comandos úteis

| Comando | Descrição |
| --- | --- |
| `python manage.py runserver` | Inicia o servidor local |
| `python manage.py migrate` | Aplica migrações pendentes |
| `python manage.py makemigrations` | Gera novas migrações a partir de alterações nos modelos |
| `python manage.py check` | Executa verificações do Django |
| `python manage.py shell` | Abre shell com o contexto do projeto |
| `python manage.py createsuperuser` | Cria usuário para acesso ao admin |
| `python manage.py test` | Executa toda a suíte de testes |
| `npm run build:css` | Gera o CSS compilado do Tailwind |
| `npm run watch:css` | Reconstrói o CSS continuamente durante o desenvolvimento |

Se você estiver no Windows e preferir usar diretamente o Python do ambiente virtual sem ativação:

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

### Rodar apenas os testes de movimentações

```bash
python manage.py test apps.movements.tests
```

### Rodar um caso específico

```bash
python manage.py test apps.movements.tests.MovementListViewTests
python manage.py test apps.movements.tests.MovementListViewTests.test_movement_list_page_returns_success
```

### O que a suíte cobre hoje

- renderização das páginas principais
- links da navegação
- criação, edição e exclusão de movimentações
- ordenação do histórico
- cálculo de totais, saldo e métricas do dashboard
- suporte a entrada monetária mascarada

## Frontend e CSS

O projeto usa Tailwind CSS com configuração em `tailwind.config.js`.

### Fluxo atual

- fonte de estilos: `assets/css/app.css`
- saída compilada: `static/css/app.css`
- templates carregam o CSS compilado com `{% static 'css/app.css' %}`

### Scripts disponíveis

```bash
npm run build:css
npm run watch:css
```

### Onde o Tailwind procura classes

- `apps/**/*.html`
- `apps/**/*.py`
- `config/**/*.py`

Sempre que alterar classes utilitárias, templates ou estilos-base, gere novamente o CSS antes de subir a aplicação.

## Configuração atual

O estado atual do projeto é orientado a desenvolvimento local.

### Banco de dados

- o backend usa SQLite
- o arquivo local esperado é `db.sqlite3`
- esse arquivo está ignorado no Git

### Settings relevantes

Em `config/settings.py`, hoje temos:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `LANGUAGE_CODE = 'pt-br'`
- `TIME_ZONE = 'UTC'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`

### Variáveis de ambiente

O projeto não usa, por enquanto, um arquivo `.env` nem um módulo dedicado para configuração por ambiente. A `SECRET_KEY` está definida diretamente em `config/settings.py`, o que é aceitável para um projeto acadêmico/local, mas não é recomendado para produção.

## Deploy

O repositório **não possui hoje** configuração pronta de deploy, como:

- `Dockerfile`
- `docker-compose.yml`
- `Procfile`
- pipeline de CI/CD
- separação formal entre configurações de desenvolvimento e produção

### O que seria necessário antes de publicar em produção

1. Externalizar `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS`
2. Criar um manifesto de dependências Python (`requirements.txt` ou `pyproject.toml`)
3. Definir estratégia de banco de dados para produção
4. Configurar `collectstatic` e servir arquivos estáticos corretamente
5. Adicionar verificações de segurança e uma rotina de deploy repetível

### Exemplo mínimo de checklist manual

```bash
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
npm run build:css
```

## Limitações conhecidas

- não há autenticação de usuário final na interface principal
- não existe manifesto versionado de dependências Python
- não há configuração de deploy automatizado
- o banco padrão é SQLite, adequado para desenvolvimento e demonstração local

## Licença

Este projeto está sob a licença MIT. Consulte `LICENSE` para os detalhes completos.
