# Setup & Configuration

> 🇧🇷 [Português](pt-BR/CONFIGURACAO.md)

How to run the KIX Store locally and configure every setting. This document targets a
developer with some Django familiarity.

## 1. Prerequisites

- Python **3.11** (the Docker image uses `python:3.11-slim`)
- `pip` and a virtual environment
- (optional) Docker + Docker Compose for the containerized flow
- Credentials for the external services you want to use (LNbits, Telegram)

## 2. Local development

```bash
# 1. create and activate a virtualenv
python3 -m venv venv
source venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. create the .env from the template below
cp .env.example .env   # or create .env manually

# 4. apply migrations
python manage.py migrate

# 5. create an admin user
python manage.py createsuperuser

# 6. collect static (optional in dev; required with DEBUG=False)
python manage.py collectstatic --noinput

# 7. run
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The admin is at `/admin/`.

## 3. Environment variables

Settings are loaded from `.env` with `python-dotenv` (see `core/settings.py`). All keys
below are strings; `DEBUG` and booleans accept `true/1/t` (case-insensitive).

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `SECRET_KEY` | yes (prod) | insecure fallback | Django secret key |
| `DEBUG` | — | `False` | enable Django debug mode |
| `ALLOWED_HOSTS` | — | `*` | comma-separated allowed hosts |
| `LNBITS_URL` | for Lightning | `https://seu-lnbits.exemplo.com/api/v1/payments` | LNbits payments endpoint |
| `LNBITS_API_KEY` | for Lightning | `""` | LNbits API key (`X-Api-Key`) |
| `TELEGRAM_BOT_TOKEN` | for contact form | `""` | bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | for contact form | `""` | chat ID that receives messages |
| `WHATSAPP_ATIVO` | — | `""` | fallback toggle for the floating button |
| `WHATSAPP_NUMERO` | — | `""` | fallback phone (digits only, DDI+DDD+number) |
| `WHATSAPP_MENSAGEM_PADRAO` | — | `Olá` | fallback default message |

Example `.env`:

```dotenv
SECRET_KEY=change-me-to-a-long-random-string
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
LNBITS_URL=https://your-lnbits/api/v1/payments
LNBITS_API_KEY=your-lnbits-key
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=123456789
WHATSAPP_ATIVO=true
WHATSAPP_NUMERO=5531999999999
WHATSAPP_MENSAGEM_PADRAO=Olá
```

## 4. Credential precedence (env vs. admin)

Some settings can be configured either in `.env` **or** the Django admin. The rules:

- **Telegram** — `.env` (`TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`) wins when both are
  set; otherwise `ConfiguracaoTelegram` (admin) is used. See
  `core/services/executor.py:_resolve_credentials`.
- **WhatsApp floating button** — the admin `ConfiguracaoWhatsApp` wins per-field; when
  a field is empty in the DB, the `.env` value is used as fallback. See
  `core/context_processors.py:whatsapp_config_processor`.

## 5. Django admin configuration

After `createsuperuser`, log into `/admin/` and configure the singletons. These drive
the storefront without code changes:

| Admin section | What you control |
|---------------|------------------|
| **Configurações do Site** (`SiteConfig`) | store name, logo, `<title>`, KIX badge, header/banner/button colors and texts |
| **Configuração do PIX** (`ConfiguracaoPix`) | PIX key, payee name, fee label, fee %, modal instruction |
| **Configuração do Telegram** | fallback creds + contact form texts and on/off |
| **Configuração do Rodapé** | company description, phones, e-mail, address, social URLs |
| **Configuração do WhatsApp** | floating button (active, number, message) |

Other admin sections manage catalogue data:

- **Categorias** (`Categoria`) — product categories (slug drives category pages)
- **Macro Categorias** (`MacroCategoria`) — storefront sections (currently defined but
  not rendered by `index.html`)
- **Categoria Cards** (`CategoriaCard`) — the category tiles on the home page
- **Produtos** (`Produto`) — SKU, name, description, category, emoji, price in sats,
  image, "Ofertas Rápidas" flag
- **Serviços** (`Servico`) — concierge/advisory cards with Telegram/WhatsApp contact
- **Cotação Bitcoin** (`CotacaoBitcoin`) — cached BTC/BRL (auto-managed)
- **Configurações do Hero** (`HomeConfig`) — hero title/subtitle/image

## 6. Static & media files

- **Static** (`/static/`) — source in `core/static/`; collected to `staticfiles/` by
  `collectstatic`. Served by **WhiteNoise** in production (`DEBUG=False`).
- **Media** (`/media/`) — uploaded images (`media/`). Always served by Django via
  `core/urls.py`, because WhiteNoise does not handle media. This is intentional for
  small deployments; for scale, put media on object storage/CDN.

## 7. Optional: Google OAuth

Google login ships enabled via `allauth.socialaccount.providers.google`. To activate:

1. Create OAuth credentials in Google Cloud Console.
2. In `/admin/`, under **Social Applications**, add a provider "Google" with your
   client ID/secret and attach it to the site (`SITE_ID=1`).
3. The `client_secret_*.json` file in the repo is an example and is git-ignored.

Local username/e-mail login works out of the box (`ACCOUNT_ALLOW_REGISTRATION=True`,
`ACCOUNT_EMAIL_VERIFICATION='none'`).
