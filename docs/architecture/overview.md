# Visão arquitetural

O MoneyFlow é uma aplicação Django pequena, server-rendered e orientada a desenvolvimento local. A arquitetura atual segue convenções padrão do Django, com pouca abstração extra e uma separação clara entre configuração global, app de apresentação e app de domínio.

## Estrutura principal

```text
MoneyFlow/
|- apps/
|  |- core/
|  `- movements/
|- assets/
|- config/
|- static/
|- manage.py
|- package.json
`- tailwind.config.js
```

## Responsabilidades por área

### `config/`

Centraliza a configuração global do projeto Django:

- `settings.py` — apps instalados, banco, templates, internacionalização e arquivos estáticos
- `urls.py` — roteamento raiz
- `asgi.py` e `wsgi.py` — entrypoints padrão do Django

### `apps/core/`

Responsável pela experiência inicial do usuário:

- dashboard principal
- agregações e métricas exibidas na home
- template-base compartilhado entre as páginas

### `apps/movements/`

Concentra o núcleo funcional do sistema:

- modelo `Movement`
- formulário de criação e edição
- listagem e CRUD das movimentações
- registro do modelo no Django Admin
- testes da área financeira

### `assets/`

Contém os arquivos-fonte de frontend usados no build, especialmente:

- `assets/css/app.css`

### `static/`

Contém ativos prontos para uso em runtime, especialmente:

- `static/css/app.css`

## Arquitetura de execução

O ciclo principal da aplicação hoje é:

1. o usuário acessa uma rota Django
2. a view consulta o banco SQLite com ORM
3. a view monta o contexto do template
4. o template renderiza HTML no servidor
5. pequenos comportamentos interativos são tratados com JavaScript embutido

## Padrões adotados

- class-based views do Django
- `ModelForm` para validação de entrada
- templates por app
- uso de agregações ORM para métricas do dashboard
- CSS utilitário compilado com Tailwind

## O que existe hoje de domínio

O domínio ativo é simples e gira em torno de uma entidade principal:

- `Movement`

Não há, no estado atual:

- autenticação de usuário final na experiência principal
- multiusuário por proprietário de movimentação
- API REST pública
- serviços de integração externa

## Pontos fortes da arquitetura atual

- baixa complexidade
- aderência às convenções do Django
- fácil leitura para contexto acadêmico e evoluções iniciais
- separação razoável entre apresentação, formulário e persistência

## Limites atuais

- toda a lógica gira em torno de um único modelo
- o projeto está configurado para desenvolvimento, não para produção
- não há manifesto Python versionado
- parte das métricas calculadas no dashboard ainda não é exibida na interface

## Leituras relacionadas

- [`apps-and-routing.md`](apps-and-routing.md)
- [`data-model.md`](data-model.md)
- [`frontend-and-assets.md`](frontend-and-assets.md)
