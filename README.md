# MoneyFlow

Aplicação web de controle financeiro pessoal desenvolvida com Django. O projeto permite registrar entradas e saídas, acompanhar saldo, consultar métricas mensais e visualizar o histórico das movimentações em uma interface em português.

## Visão rápida

- backend em Django 5.2.13
- banco local SQLite
- frontend com Django Templates e Tailwind CSS
- foco atual em desenvolvimento local e contexto acadêmico

## Funcionalidades principais

- cadastro de movimentações financeiras com descrição, tipo, valor e data
- dashboard com saldo atual, entradas, saídas, ticket médio e comparativos mensais
- histórico completo de movimentações
- edição e exclusão de registros com confirmação
- área administrativa do Django para manutenção dos dados

## Rotas principais

- `/` — dashboard principal
- `/movements/` — histórico das movimentações
- `/movements/nova/` — nova movimentação
- `/movements/<id>/editar/` — edição de movimentação
- `/movements/<id>/excluir/` — exclusão via `POST`
- `/admin/` — administração do Django

## Início rápido

### 1. Instale as dependências principais

```bash
pip install "Django==5.2.13"
npm install
```

### 2. Aplique migrações e gere o CSS

```bash
python manage.py migrate
npm run build:css
```

### 3. Suba o servidor

```bash
python manage.py runserver
```

Aplicação disponível em `http://127.0.0.1:8000/`.

## Documentação

Além deste arquivo de entrada, a documentação detalhada está organizada na pasta `docs/`.

### Mapa da documentação

- [`docs/getting-started/local-setup.md`](docs/getting-started/local-setup.md)
- [`docs/getting-started/development-workflow.md`](docs/getting-started/development-workflow.md)
- [`docs/getting-started/troubleshooting.md`](docs/getting-started/troubleshooting.md)
- [`docs/architecture/overview.md`](docs/architecture/overview.md)
- [`docs/architecture/apps-and-routing.md`](docs/architecture/apps-and-routing.md)
- [`docs/architecture/data-model.md`](docs/architecture/data-model.md)
- [`docs/architecture/frontend-and-assets.md`](docs/architecture/frontend-and-assets.md)
- [`docs/product/feature-overview.md`](docs/product/feature-overview.md)
- [`docs/reference/commands.md`](docs/reference/commands.md)
- [`docs/reference/configuration.md`](docs/reference/configuration.md)
- [`docs/reference/routes.md`](docs/reference/routes.md)
- [`docs/reference/testing.md`](docs/reference/testing.md)
- [`docs/operations/deployment.md`](docs/operations/deployment.md)
- [`docs/contributing/contributor-guide.md`](docs/contributing/contributor-guide.md)

### Leitura recomendada

- Para configurar o projeto pela primeira vez: [`docs/getting-started/local-setup.md`](docs/getting-started/local-setup.md)
- Para entender a arquitetura: [`docs/architecture/overview.md`](docs/architecture/overview.md)
- Para conhecer as funcionalidades: [`docs/product/feature-overview.md`](docs/product/feature-overview.md)
- Para consultar comandos rápidos: [`docs/reference/commands.md`](docs/reference/commands.md)

## Comandos úteis

```bash
python manage.py runserver
python manage.py migrate
python manage.py test
npm run build:css
npm run watch:css
```

## Estado atual

- o projeto está preparado para desenvolvimento local
- não há manifesto Python versionado no repositório neste momento
- não existe configuração pronta de deploy para produção

## Licença

Este projeto está sob a licença MIT. Consulte [`LICENSE`](LICENSE).
