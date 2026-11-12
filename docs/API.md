# API Reference

> 🇧🇷 [Português](pt-BR/API.md)

All routes defined in `core/urls.py`. The storefront is server-rendered; the JSON
endpoints below are consumed by `core/static/js/script.js`. All mutating endpoints
require the Django CSRF token (the page exposes it as `window.csrfToken`, and the JS
sends it in the `X-CSRFToken` header).

Legend: 🔐 = login required, 🛒 = cart, 💬 = contact, ⚡ = payment.

## Page routes

| Method | Path | View | Notes |
|--------|------|------|-------|
| GET | `/` | `views.home` | Home: hero, macro categories, quick offers, BTC quote |
| GET | `/categoria/<nome>/` | `views.categoria_detalhe` | Category products (filters by `categoria__slug`) |
| GET | `/categoria/<slug>/` | `views.detalhe_categoria` | Unreachable in practice (see Architecture §9) |
| GET | `/produto/<sku>/` | `views.produto_detalhe` | Product detail |
| GET/POST | `/perfil/editar/` 🔐 | `views.editar_perfil` | Edit delivery profile |
| GET | `/accounts/…` | django-allauth | Login/signup/social |
| GET | `/admin/` | Django admin | — |

## Cart endpoints 🛒

### `POST /cart/add/`

Adds one unit of a product by SKU. Price/name are re-read from the DB (client values
ignored).

**Body** (form-encoded): `product_id` (SKU)

**Response** `200`:

```json
{"total_items": 3, "total_sats": 45000}
```

Errors: `400` missing product, `404` unknown SKU.

### `POST /cart/remove/`

Removes one unit (the active `KixCart.remove` deletes the item entirely when quantity
reaches zero).

**Body**: `product_id`

**Response** `200`: `{"total_items": …, "total_sats": …}`

### `POST /cart/clear/`

Empties the cart.

**Response** `200`: `{"total_items": 0, "total_sats": 0, "message": "…"}`

### `GET /cart/status/`

Current cart state.

**Response** `200`:

```json
{"total_items": 2, "total_sats": 45000, "items": {"<sku>": {"name": "…", "price_sats": 22500, "quantity": 2}}}
```

### `GET /cart/summary/`

Structured summary (used for modal item lists).

**Response** `200`:

```json
{"items": [{"product_id": "<sku>", "name": "…", "price_sats": 22500, "quantity": 2, "subtotal_sats": 45000}], "total_items": 2, "total_sats": 45000}
```

## Payment endpoints ⚡

### `POST /cart/checkout/`

Creates a Lightning invoice via LNbits.

**Response** `200`:

```json
{"payment_request": "lnbc…", "payment_hash": "…"}
```

Errors: `400` empty cart, `500` LNbits error, `503` connection error.

### `POST /cart/check-payment/`

Checks invoice settlement status.

**Body** (JSON): `{"payment_hash": "…"}`

**Response** `200`:

```json
{"paid": true, "status": "complete"}
```

Errors: `400` invalid/missing hash, `503` connection error. Non-200 LNbits responses
echo the upstream status.

## Profile endpoints

### `GET /api/user-profile/` 🔐

Returns the logged-in user's delivery data.

**Response** `200`:

```json
{"telefone": "…", "endereco": "…"}
```

Missing fields resolve to `"Não informado"`.

## Contact endpoints 💬

### `POST /send_telegram`

Footer contact form → Telegram notification to the store owner.

**Body** (form-encoded): `name`, `email`, `telegram` (optional), `message`

**Response** `200`: `{"status": "success", "message": "…"}`

Errors: `400` missing fields / invalid e-mail. The Telegram send is best-effort: a
failure is logged and still returns success to the visitor.

### `POST /servico/interesse/`

Service card interest contact.

**Body** (JSON or form-encoded): `servico_id`, `mensagem`, `canal` (`whatsapp` | `telegram`)

**Response** (WhatsApp) `200`:

```json
{"status": "success", "canal": "whatsapp", "url": "https://api.whatsapp.com/send?phone=…&text=…"}
```

**Response** (Telegram) `200`:

```json
{"status": "success", "canal": "telegram", "message": "…"}
```

Errors: `400` missing/invalid input or channel disabled, `404` unknown service,
`502` Telegram send failure.
