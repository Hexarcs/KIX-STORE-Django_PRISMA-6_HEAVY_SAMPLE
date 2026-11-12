# KIX Store — Supermercado KIX

A Django e-commerce storefront that prices products in **satoshis** and accepts two
payment rails side by side: native **Lightning Network** (via LNbits) and **PIX**
(fiat, with a configurable "state processing fee"). The store is the merchant
front-end of the [KIX Protocol](https://github.com/Hexarcs/KIX-PROTOCOL) ecosystem.

> 🇧🇷 **Português:** [README.pt-BR.md](README.pt-BR.md)

---

## What it is

KIX Store is a self-contained Django application (`core` app) that lets a merchant
catalogue products, price them in sats, and let customers pay:

- **⚡ Native KIX checkout** — a BOLT 11 invoice is generated through an LNbits
  endpoint and the customer pays over Lightning. This is the *default* path.
- **🏛️ PIX estatal** — the fiat fallback, priced at the Bitcoin/BRL rate plus a
  configurable percentage fee (default `+10%`), which incentives the Lightning path.

Everything visible in the storefront — logo, name, colors, banner, texts, PIX keys,
contact channels — is editable from the Django admin, no code changes needed.

## Key features

- Products priced in sats with a live Bitcoin/BRL reference (Binance ticker, cached 24 h)
- Session-based cart (`KixCart`) with add/remove/clear over AJAX
- Lightning checkout: LNbits invoice + QR code + polling for payment confirmation
- PIX checkout: client-side fiat conversion with a configurable fee
- Authentication via **django-allauth** (local username/e-mail + Google OAuth)
- Footer contact form → **Telegram** notification
- "Services" cards (concierge/advisory) with interest contact via **Telegram** or **WhatsApp**
- Floating WhatsApp button (click-to-chat)
- Singleton site configuration driven entirely by Django admin
- Docker + `deploy.sh` for repeatable deployments; WhiteNoise for static files

## Tech stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Web framework | Django 5.x |
| Auth | django-allauth (local + Google) |
| Database | SQLite (`data/db.sqlite3`) |
| Static files | WhiteNoise |
| HTTP client | `requests` (Binance, LNbits, Telegram) |
| Deployment | Docker / Docker Compose, Gunicorn-ready |

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — components, data flow, payment flows, KIX mapping
- [Setup & configuration](docs/SETUP.md) — local development and all settings/env vars
- [Deployment](docs/DEPLOYMENT.md) — Docker, `deploy.sh`, bare-metal
- [API reference](docs/API.md) — every URL/endpoint
- [Data model](docs/DATA_MODEL.md) — all Django models and admin singletons
- [KIX protocol context](docs/KIX_PROTOCOL.md) — how the store maps onto PRISMA
- [Docs index](docs/README.md)

## Quick start

### Local (venv)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# copy .env and fill in the placeholders (see docs/SETUP.md)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Docker

```bash
docker compose up -d --build
```

The app is served on `http://localhost:8003` (port mapped in `docker-compose.yml`).

> **Production note:** the repo ships permissive defaults (`ALLOWED_HOSTS=*`,
> `CSRF_TRUSTED_ORIGINS=['https://*', ...]`, weak placeholder secrets) for easy
> onboarding. Tighten them before exposing the store publicly — see
> [Deployment → Security checklist](docs/DEPLOYMENT.md#security-checklist).

## Environment variables

The application reads configuration from `.env` (via `python-dotenv`). See
[Setup & configuration](docs/SETUP.md#environment-variables) for the full reference.

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True`/`False` |
| `ALLOWED_HOSTS` | comma-separated hosts |
| `LNBITS_URL` | LNbits payments endpoint |
| `LNBITS_API_KEY` | LNbits API key |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | Telegram contact notifications |
| `WHATSAPP_ATIVO` / `WHATSAPP_NUMERO` / `WHATSAPP_MENSAGEM_PADRAO` | floating button fallback |

---

Licensed under the project's existing terms. Built on top of the
[KIX Protocol](https://github.com/Hexarcs/KIX-PROTOCOL).
