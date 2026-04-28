# Solução de problemas

Esta página reúne os problemas mais prováveis ao rodar ou evoluir o projeto localmente.

## O comando `python` não usa o ambiente virtual

No Windows, use diretamente o executável da virtualenv:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

Se preferir, ative o ambiente antes:

```powershell
.venv\Scripts\Activate.ps1
```

## O PowerShell bloqueia a ativação da virtualenv

Se a política de execução impedir o script de ativação, você pode:

- abrir um terminal já configurado para Python
- usar diretamente `.venv\Scripts\python.exe`

## `ModuleNotFoundError: No module named 'django'`

Isso indica que o Django ainda não foi instalado no ambiente atual.

Instale com:

```bash
pip install "Django==5.2.13"
```

## O estilo da interface não aparece corretamente

Verifique os pontos abaixo:

1. se `npm install` foi executado
2. se `npm run build:css` gerou `static/css/app.css`
3. se o template base continua carregando `{% static 'css/app.css' %}`
4. se você salvou as alterações nos arquivos monitorados pelo Tailwind

Para acompanhar mudanças de interface em tempo real:

```bash
npm run watch:css
```

## Fiz mudanças no template, mas o CSS não refletiu

O Tailwind examina os seguintes caminhos:

- `apps/**/*.html`
- `apps/**/*.py`
- `config/**/*.py`

Se você criar arquivos fora desses caminhos, as classes podem não entrar no build. Nesse caso, atualize `tailwind.config.js` se a mudança fizer sentido para o projeto.

## Erro ao acessar o banco SQLite

Geralmente isso acontece quando as migrações ainda não foram aplicadas.

Execute:

```bash
python manage.py migrate
```

## O admin não aceita login

O painel do Django precisa de um superusuário criado manualmente.

Execute:

```bash
python manage.py createsuperuser
```

## Os testes falham após mudança de layout

A suíte atual valida bastante conteúdo textual nas páginas. Se você mudou títulos, rótulos ou textos visíveis, talvez seja necessário atualizar os testes correspondentes.

Arquivos mais sensíveis a esse tipo de mudança:

- `apps/core/tests.py`
- `apps/movements/tests.py`

## Há menções a `apps.accounts`, mas essa pasta não existe ou não está ativa

O estado real do projeto hoje considera apenas os apps instalados em `config/settings.py`:

- `apps.core`
- `apps.movements`

Se alguma documentação antiga mencionar outra app, considere o código real como fonte principal.

## Leituras relacionadas

- [`local-setup.md`](local-setup.md)
- [`../architecture/frontend-and-assets.md`](../architecture/frontend-and-assets.md)
- [`../reference/commands.md`](../reference/commands.md)
