# Referência da API

> 🇺🇸 [English](../API.md)

Todas as rotas definidas em `core/urls.py`. A vitrine é renderizada no servidor; os
endpoints JSON abaixo são consumidos por `core/static/js/script.js`. Todos os
endpoints de mutação exigem o token CSRF do Django (a página o expõe como
`window.csrfToken`, e o JS o envia no header `X-CSRFToken`).

Legenda: 🔐 = requer login, 🛒 = carrinho, 💬 = contato, ⚡ = pagamento.

## Rotas de página

| Método | Caminho | View | Notas |
|--------|---------|------|-------|
| GET | `/` | `views.home` | Home: hero, macro categorias, ofertas rápidas, cotação BTC |
| GET | `/categoria/<nome>/` | `views.categoria_detalhe` | Produtos da categoria (filtra por `categoria__slug`) |
| GET | `/categoria/<slug>/` | `views.detalhe_categoria` | Inalcançável na prática (veja Arquitetura §9) |
| GET | `/produto/<sku>/` | `views.produto_detalhe` | Detalhe do produto |
| GET/POST | `/perfil/editar/` 🔐 | `views.editar_perfil` | Edita perfil de entrega |
| GET | `/accounts/…` | django-allauth | Login/cadastro/social |
| GET | `/admin/` | Django admin | — |

## Endpoints de carrinho 🛒

### `POST /cart/add/`

Adiciona uma unidade de um produto pelo SKU. Preço/nome são relidos do banco (valores
do cliente são ignorados).

**Body** (form-encoded): `product_id` (SKU)

**Resposta** `200`:

```json
{"total_items": 3, "total_sats": 45000}
```

Erros: `400` produto ausente, `404` SKU desconhecido.

### `POST /cart/remove/`

Remove uma unidade (o `KixCart.remove` ativo apaga o item quando a quantidade chega a
zero).

**Body**: `product_id`

**Resposta** `200`: `{"total_items": …, "total_sats": …}`

### `POST /cart/clear/`

Esvazia o carrinho.

**Resposta** `200`: `{"total_items": 0, "total_sats": 0, "message": "…"}`

### `GET /cart/status/`

Estado atual do carrinho.

**Resposta** `200`:

```json
{"total_items": 2, "total_sats": 45000, "items": {"<sku>": {"name": "…", "price_sats": 22500, "quantity": 2}}}
```

### `GET /cart/summary/`

Resumo estruturado (usado nas listas de itens do modal).

**Resposta** `200`:

```json
{"items": [{"product_id": "<sku>", "name": "…", "price_sats": 22500, "quantity": 2, "subtotal_sats": 45000}], "total_items": 2, "total_sats": 45000}
```

## Endpoints de pagamento ⚡

### `POST /cart/checkout/`

Cria uma invoice Lightning via LNbits.

**Resposta** `200`:

```json
{"payment_request": "lnbc…", "payment_hash": "…"}
```

Erros: `400` carrinho vazio, `500` erro do LNbits, `503` erro de conexão.

### `POST /cart/check-payment/`

Consulta o status de liquidação da invoice.

**Body** (JSON): `{"payment_hash": "…"}`

**Resposta** `200`:

```json
{"paid": true, "status": "complete"}
```

Erros: `400` hash inválido/ausente, `503` erro de conexão. Respostas não-200 do LNbits
ecoam o status upstream.

## Endpoints de perfil

### `GET /api/user-profile/` 🔐

Retorna os dados de entrega do usuário logado.

**Resposta** `200`:

```json
{"telefone": "…", "endereco": "…"}
```

Campos ausentes resolvem para `"Não informado"`.

## Endpoints de contato 💬

### `POST /send_telegram`

Formulário de contato do rodapé → notificação Telegram ao dono da loja.

**Body** (form-encoded): `name`, `email`, `telegram` (opcional), `message`

**Resposta** `200`: `{"status": "success", "message": "…"}`

Erros: `400` campos ausentes / e-mail inválido. O envio Telegram é best-effort: uma
falha é logada e ainda assim retorna sucesso ao visitante.

### `POST /servico/interesse/`

Contato de interesse em um card de serviço.

**Body** (JSON ou form-encoded): `servico_id`, `mensagem`, `canal` (`whatsapp` | `telegram`)

**Resposta** (WhatsApp) `200`:

```json
{"status": "success", "canal": "whatsapp", "url": "https://api.whatsapp.com/send?phone=…&text=…"}
```

**Resposta** (Telegram) `200`:

```json
{"status": "success", "canal": "telegram", "message": "…"}
```

Erros: `400` entrada ausente/inválida ou canal desabilitado, `404` serviço
desconhecido, `502` falha no envio Telegram.
