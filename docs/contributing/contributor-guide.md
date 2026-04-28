# Guia de contribuição

Este guia é voltado para pessoas desenvolvedoras que queiram evoluir o projeto com consistência.

## Princípios do repositório

- prefira soluções simples e idiomáticas do Django
- mantenha a arquitetura enxuta
- evite abstrações desnecessárias
- preserve a separação entre configuração global, domínio e templates
- faça mudanças pequenas e fáceis de revisar

## Estrutura que importa conhecer

- `config/` — settings e URLs globais
- `apps/core/` — dashboard e base da interface
- `apps/movements/` — domínio principal e CRUD financeiro
- `assets/css/` — fonte de estilos
- `static/css/` — CSS compilado usado em runtime

## Convenções observadas

### Python

- 4 espaços de indentação
- imports no topo do arquivo
- preferência por convenções padrão do Django
- uso moderado de type hints

### Django

- class-based views quando fizer sentido
- `ModelForm` para validação e apresentação de entrada
- testes com `django.test.TestCase`
- templates por app em vez de uma pasta global de templates

### Frontend

- Tailwind CSS como base visual
- interface em português do Brasil
- JavaScript pequeno e embutido quando a interação é local à página

## Como contribuir com segurança

### Ao mexer em views, forms ou modelos

- rode os testes relacionados
- valide o impacto no dashboard e no histórico
- preserve as regras atuais de saldo e tipos de movimentação

### Ao mexer em templates ou estilos

- reconstrua o CSS
- revise os textos renderizados
- confirme se os testes que validam conteúdo textual continuam coerentes

### Ao mexer em modelos

- gere migração com `python manage.py makemigrations`
- revise a migração antes de seguir
- aplique com `python manage.py migrate`

## Documentação e código precisam andar juntos

Se você alterar comportamento funcional, comandos, setup ou arquitetura, atualize também a documentação correspondente em `/docs`.

## Sobre `AGENTS.md`

O arquivo `AGENTS.md` contém instruções operacionais para agentes de código. Ele é útil como referência interna, mas este guia e a árvore `/docs` devem ser tratados como a documentação principal para contribuidores humanos.

## Checklist curto antes de entregar mudanças

1. código revisado
2. testes relevantes executados
3. CSS recompilado se necessário
4. documentação atualizada se o comportamento mudou

## Leituras relacionadas

- [`../architecture/overview.md`](../architecture/overview.md)
- [`../reference/testing.md`](../reference/testing.md)
- [`../reference/commands.md`](../reference/commands.md)
