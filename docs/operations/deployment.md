# Deploy e operação

O MoneyFlow, no estado atual do repositório, está preparado para desenvolvimento local. Este documento registra o que existe hoje, o que ainda falta para produção e um checklist mínimo de validação manual.

## O que não existe hoje no repositório

Não foram encontrados, neste momento:

- `Dockerfile`
- `docker-compose.yml`
- `Procfile`
- pipeline de CI/CD
- separação formal entre settings de desenvolvimento e produção
- manifesto Python versionado

## Riscos atuais para produção

- `SECRET_KEY` fixa em `config/settings.py`
- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- banco SQLite como padrão
- ausência de automação de deploy
- estratégia de estáticos ainda manual

## O que precisaria ser feito antes de publicar

### Configuração e segurança

1. externalizar `SECRET_KEY`
2. desligar `DEBUG`
3. definir `ALLOWED_HOSTS`
4. separar configurações por ambiente

### Dependências

1. criar `requirements.txt` ou `pyproject.toml`
2. fixar versões necessárias para reprodução consistente

### Banco de dados

1. definir banco apropriado para produção
2. planejar estratégia de migração e backup

### Arquivos estáticos

1. garantir build do CSS no processo de entrega
2. executar `collectstatic`
3. definir como os arquivos estáticos serão servidos

### Qualidade operacional

1. automatizar testes
2. rodar `check --deploy`
3. documentar procedimento de rollback e atualização

## Checklist mínimo manual

Antes de qualquer tentativa de publicação, pelo menos rode:

```bash
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
npm run build:css
python manage.py test
```

## Situação adequada hoje

O cenário mais compatível com o estado atual do projeto é:

- desenvolvimento local
- demonstração acadêmica
- validação funcional em ambiente simples

## Leituras relacionadas

- [`../reference/configuration.md`](../reference/configuration.md)
- [`../reference/commands.md`](../reference/commands.md)
- [`../architecture/overview.md`](../architecture/overview.md)
