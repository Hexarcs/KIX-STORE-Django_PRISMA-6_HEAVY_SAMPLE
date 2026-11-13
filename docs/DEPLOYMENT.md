# Deployment

> 🇧🇷 [Português](pt-BR/IMPLANTACAO.md)

The KIX Store supports two deployment styles: **Docker** (recommended) and
**bare-metal** (venv + Gunicorn/systemd). This page covers both and ends with a
security checklist.

> ⚙️ **Before you start** — make sure **Git** and **Docker** are installed and that you
> have cloned this repository. See **[Prerequisites](PREREQUISITES.md)** for a
> step-by-step guide (Git, Docker Engine + Compose, and cloning/building the image).

## 1. Docker

### 1.1 The image

`Dockerfile` builds a `python:3.11-slim` image that installs system deps (`gcc`,
`libpq-dev`), installs `requirements.txt`, copies the project, and starts
`runserver 0.0.0.0:8000` by default.

```bash
docker build -t your-name/kix-store:latest .
```

### 1.2 Docker Compose

The repo's `docker-compose.yml` builds from source and maps host port **8003** to
container port **8000**, mounting the project directory as a volume:

```bash
docker compose up -d --build
```

`data/` and `media/` are the state you must persist; the current compose mounts the
whole project (`.:/app`), which includes them.

### 1.3 The `deploy.sh` script

`deploy.sh` is a one-shot bootstrap that generates three files and starts the stack:

```
deploy.sh
 ├── .env            (placeholder credentials)
 ├── entrypoint.sh   (in-container bootstrap)
 └── docker-compose.yml (image-based, host port 8006)
```

It then runs `docker compose down -v` and `docker compose up -d`. The generated
`entrypoint.sh`:

1. appends django-allauth/proxy/CSRF settings to `settings.py` (idempotent, guarded by
   a `SOCIALACCOUNT_ONLY` check);
2. runs `makemigrations` + `migrate`;
3. runs `collectstatic --noinput`;
4. ensures a superuser exists (defaults `admin` / `SUA_SENHA_SEGURA_AQUI` — **change these**);
5. starts `runserver 0.0.0.0:8000`.

> ⚠️ `deploy.sh` regenerates `.env`, `entrypoint.sh`, and `docker-compose.yml` from
> scratch on every run — any manual edits to those files are overwritten. It also
> writes a hardcoded default admin password into the compose file, which is acceptable
> only for a private/learning environment.

## 2. Bare-metal (Gunicorn + systemd)

The repo references this flow in `comandos_python.txt` and `docker_comandos.txt`. The
outline:

```bash
source venv/bin/activate
pip install -r requirements.txt          # includes gunicorn

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# run under gunicorn (reverse proxy / systemd in front)
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

A reverse proxy (Nginx/Caddy) should terminate HTTPS, forward to Gunicorn, and serve
`/static/` (from `staticfiles/`) and `/media/`. Because the app sits behind a proxy,
`settings.py`/`entrypoint.sh` enable `USE_X_FORWARDED_HOST` and
`SECURE_PROXY_SSL_HEADER`.

## 3. Accessing the store

- **Locally** — open `http://localhost:8006` in your browser. `8006` is the host port
  used by the `deploy.sh` flow (the repo's own `docker-compose.yml` maps `8003`).
- **Public web** — run the store on a **VPS** and put a reverse proxy (**Nginx** or
  **Apache**) in front of it. The proxy terminates HTTPS and forwards requests to the
  local port (`8006`).
- **Tor** — same idea: configure a Tor hidden service whose target points at the local
  port (`8006`), and the store is reachable through its `.onion` address.

## 4. Database & media persistence

- SQLite lives at `data/db.sqlite3` (see `DATABASES` in `core/settings.py`).
- Uploaded media lives in `media/`.
- To copy a store to another instance, copy `data/db.sqlite3` and the `media/` tree
  (see `copydatabase.txt` for a worked example).
- `requirements.txt` includes `psycopg2-binary` although the current settings use
  SQLite — switching to PostgreSQL only requires editing `DATABASES`.

## 5. Security checklist

The shipped defaults favor a fast first run over security. Before any public
exposure:

- [ ] Set a strong, random `SECRET_KEY` (never the `django-insecure-...` fallback).
- [ ] Set `DEBUG=False`.
- [ ] Replace `ALLOWED_HOSTS=*` with your exact domains.
- [ ] Replace permissive `CSRF_TRUSTED_ORIGINS = ['https://*', 'http://*']` with your
      explicit origins (e.g. `https://your-domain.com`).
- [ ] Decide `CSRF_COOKIE_SECURE` / `CSRF_COOKIE_HTTPONLY` for your frontend
      architecture (set `CSRF_COOKIE_SECURE=True` on pure HTTPS).
- [ ] Change or remove the default admin password (`SUA_SENHA_SEGURA_AQUI`) written by
      `deploy.sh`; prefer environment secrets over hardcoded compose values.
- [ ] Never commit real `.env` values or the Google `client_secret_*.json`.
- [ ] Put a real secret store (Docker secrets, Vault, env in the orchestrator) in front
      of `LNBITS_API_KEY`, `TELEGRAM_BOT_TOKEN`, etc.
- [ ] Keep the LNbits node behind authentication; the store's API key grants invoice
      creation/read access.

## 6. Common operations

```bash
docker compose logs -f            # follow logs
docker compose ps                 # status
docker compose restart            # restart without rebuild
docker compose down               # stop (keeps bind-mounted data/media)
docker compose up -d --build      # rebuild and start
```

Re-run `./deploy.sh` whenever you want the bootstrap to regenerate its three files and
recreate the container.
