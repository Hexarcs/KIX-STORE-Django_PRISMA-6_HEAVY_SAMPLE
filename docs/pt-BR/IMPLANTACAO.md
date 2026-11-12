# Implantação

> 🇺🇸 [English](../DEPLOYMENT.md)

A KIX Store suporta dois estilos de implantação: **Docker** (recomendado) e
**bare-metal** (venv + Gunicorn/systemd). Esta página cobre ambos e termina com um
checklist de segurança.

## 1. Docker

### 1.1 A imagem

O `Dockerfile` constrói uma imagem `python:3.11-slim` que instala dependências de
sistema (`gcc`, `libpq-dev`), instala o `requirements.txt`, copia o projeto e inicia
`runserver 0.0.0.0:8000` por padrão.

```bash
docker build -t seu-nome/kix-store:latest .
```

### 1.2 Docker Compose

O `docker-compose.yml` do repositório constrói a partir do código-fonte e mapeia a
porta **8003** do host para a porta **8000** do container, montando o diretório do
projeto como volume:

```bash
docker compose up -d --build
```

`data/` e `media/` são o estado que você deve persistir; o compose atual monta o
projeto inteiro (`.:/app`), que os inclui.

### 1.3 O script `deploy.sh`

`deploy.sh` é um bootstrap one-shot que gera três arquivos e inicia o stack:

```
deploy.sh
 ├── .env            (credenciais placeholder)
 ├── entrypoint.sh   (bootstrap dentro do container)
 └── docker-compose.yml (baseado em imagem, porta 8006)
```

Depois executa `docker compose down -v` e `docker compose up -d`. O `entrypoint.sh`
gerado:

1. anexa as configurações de django-allauth/proxy/CSRF ao `settings.py` (idempotente,
   protegido por uma checagem de `SOCIALACCOUNT_ONLY`);
2. executa `makemigrations` + `migrate`;
3. executa `collectstatic --noinput`;
4. garante a existência de um superusuário (padrões `admin` / `SUA_SENHA_SEGURA_AQUI` —
   **troque-os**);
5. inicia `runserver 0.0.0.0:8000`.

> ⚠️ O `deploy.sh` regenera `.env`, `entrypoint.sh` e `docker-compose.yml` do zero a
> cada execução — qualquer edição manual nesses arquivos é sobrescrita. Ele também
> grava uma senha de admin padrão fixa no compose, aceitável apenas em ambiente
> privado/aprendizado.

## 2. Bare-metal (Gunicorn + systemd)

O repositório referencia esse fluxo em `comandos_python.txt` e `docker_comandos.txt`.
O resumo:

```bash
source venv/bin/activate
pip install -r requirements.txt          # inclui gunicorn

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# rode sob gunicorn (reverse proxy / systemd à frente)
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Um reverse proxy (Nginx/Caddy) deve terminar o HTTPS, encaminhar ao Gunicorn e servir
`/static/` (de `staticfiles/`) e `/media/`. Como a app fica atrás de proxy,
`settings.py`/`entrypoint.sh` habilitam `USE_X_FORWARDED_HOST` e
`SECURE_PROXY_SSL_HEADER`.

## 3. Persistência de banco e mídia

- O SQLite vive em `data/db.sqlite3` (veja `DATABASES` em `core/settings.py`).
- A mídia enviada vive em `media/`.
- Para copiar uma loja para outra instância, copie `data/db.sqlite3` e a árvore
  `media/` (veja `copydatabase.txt` para um exemplo prático).
- O `requirements.txt` inclui `psycopg2-binary` embora as configurações atuais usem
  SQLite — migrar para PostgreSQL exige apenas editar `DATABASES`.

## 4. Checklist de segurança

Os padrões entregues favorecem uma primeira execução rápida em detrimento da
segurança. Antes de qualquer exposição pública:

- [ ] Defina uma `SECRET_KEY` forte e aleatória (nunca o fallback `django-insecure-...`).
- [ ] Defina `DEBUG=False`.
- [ ] Substitua `ALLOWED_HOSTS=*` pelos seus domínios exatos.
- [ ] Substitua `CSRF_TRUSTED_ORIGINS = ['https://*', 'http://*']` permissivo pelas
      suas origens explícitas (ex.: `https://seu-dominio.com`).
- [ ] Decida `CSRF_COOKIE_SECURE` / `CSRF_COOKIE_HTTPONLY` para sua arquitetura de
      frontend (use `CSRF_COOKIE_SECURE=True` em HTTPS puro).
- [ ] Troque ou remova a senha de admin padrão (`SUA_SENHA_SEGURA_AQUI`) gravada pelo
      `deploy.sh`; prefira secrets de ambiente a valores fixos no compose.
- [ ] Nunca faça commit de valores reais do `.env` ou do `client_secret_*.json` do Google.
- [ ] Use um cofre de segredos real (Docker secrets, Vault, env no orquestrador) para
      `LNBITS_API_KEY`, `TELEGRAM_BOT_TOKEN` etc.
- [ ] Mantenha o nó LNbits atrás de autenticação; a chave de API da loja concede
      acesso de criação/leitura de invoices.

## 5. Operações comuns

```bash
docker compose logs -f            # acompanha logs
docker compose ps                 # status
docker compose restart            # reinicia sem rebuild
docker compose down               # para (mantém data/media dos bind mounts)
docker compose up -d --build      # reconstrói e inicia
```

Execute `./deploy.sh` novamente sempre que quiser que o bootstrap regenere seus três
arquivos e recrie o container.
