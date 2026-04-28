# Configuração atual

Este documento registra a configuração observada no projeto e o que ela implica para desenvolvimento e operação.

## Base tecnológica

- Python 3.11
- Django 5.2.13
- SQLite
- Tailwind CSS 3.4.17

## Settings relevantes

Em `config/settings.py`, o projeto usa hoje:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `LANGUAGE_CODE = "pt-br"`
- `TIME_ZONE = "UTC"`
- `USE_I18N = True`
- `USE_TZ = True`
- `STATIC_URL = "static/"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`
- `STATIC_ROOT = BASE_DIR / "staticfiles"`

## Apps instalados

Atualmente, o projeto instala:

- apps nativos do Django para admin, auth, sessions, messages e staticfiles
- `apps.core`
- `apps.movements`

## Templates

A configuração de templates usa:

- `DIRS = []`
- `APP_DIRS = True`

Isso significa que a aplicação depende da estrutura de templates dentro de cada app.

## Banco de dados

O banco padrão é SQLite, configurado como:

- `BASE_DIR / "db.sqlite3"`

Implicações:

- ótimo para desenvolvimento local
- simples de configurar
- inadequado como estratégia final de produção sem outras decisões de arquitetura

## Internacionalização

Configuração atual:

- idioma da interface: português do Brasil
- fuso horário: UTC

Isso significa que a interface foi escrita em português, mas o tratamento temporal do projeto segue a configuração UTC do Django.

## Arquivos estáticos

Há três conceitos importantes:

- `assets/` — fonte dos estilos
- `static/` — arquivos estáticos usados em runtime local
- `staticfiles/` — saída esperada de `collectstatic`

## Dependências Python

Hoje o repositório não possui um manifesto Python versionado. Ausências observadas:

- `requirements.txt`
- `pyproject.toml`

Consequência prática:

- a reprodução do ambiente depende da documentação e da versão manual do Django

## Segurança e produção

A configuração atual é apropriada para contexto local ou acadêmico, mas não para produção, porque:

- a `SECRET_KEY` está fixa em `settings.py`
- `DEBUG` está ativado
- `ALLOWED_HOSTS` está vazio
- não há separação formal por ambiente

## Leituras relacionadas

- [`commands.md`](commands.md)
- [`routes.md`](routes.md)
- [`../operations/deployment.md`](../operations/deployment.md)
