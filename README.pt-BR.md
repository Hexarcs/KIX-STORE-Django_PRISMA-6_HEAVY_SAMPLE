# KIX Store — Supermercado KIX

Uma loja virtual Django que precifica produtos em **satoshis** e aceita dois meios de
pagamento lado a lado: **Lightning Network** nativa (via LNbits) e **PIX** (moeda
fiduciária, com uma "taxa de processamento estatal" configurável). A loja é a camada
de comerciante (PDV) do ecossistema do [Protocolo KIX](https://github.com/Hexarcs/KIX-PROTOCOL).

> 🇺🇸 **English:** [README.md](README.md)

---

## O que é

A KIX Store é uma aplicação Django autocontida (app `core`) que permite a um lojista
catalogar produtos, precificá-los em sats e receber pagamentos de duas formas:

- **⚡ Checkout KIX nativo** — uma invoice BOLT 11 é gerada por meio de um endpoint
  LNbits e o cliente paga via Lightning. Esse é o caminho *padrão*.
- **🏛️ PIX estatal** — alternativa em moeda fiduciária, precificada pela cotação
  Bitcoin/BRL acrescida de uma taxa percentual configurável (padrão `+10%`), o que
  incentiva o uso do caminho Lightning.

Tudo o que aparece na vitrine — logo, nome, cores, banner, textos, chave PIX, canais
de contato — é editável pelo Django admin, sem alterar código.

## Principais recursos

- Produtos precificados em sats com cotação Bitcoin/BRL ao vivo (ticker Binance, cache de 24 h)
- Carrinho baseado em sessão (`KixCart`) com adicionar/remover/limpar via AJAX
- Checkout Lightning: invoice LNbits + QR code + consulta de confirmação de pagamento
- Checkout PIX: conversão fiduciária no cliente com taxa configurável
- Autenticação via **django-allauth** (local usuário/e-mail + Google OAuth)
- Formulário de contato no rodapé → notificação por **Telegram**
- Cards de "Serviços" (assessoria/concierge) com contato via **Telegram** ou **WhatsApp**
- Botão flutuante de WhatsApp (click-to-chat)
- Configuração do site em singleton, totalmente pelo Django admin
- Docker + `deploy.sh` para implantações repetíveis; WhiteNoise para estáticos

## Stack técnica

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.11 |
| Framework web | Django 5.x |
| Auth | django-allauth (local + Google) |
| Banco de dados | SQLite (`data/db.sqlite3`) |
| Arquivos estáticos | WhiteNoise |
| Cliente HTTP | `requests` (Binance, LNbits, Telegram) |
| Implantação | Docker / Docker Compose, pronto para Gunicorn |

## Documentação

- [Arquitetura](docs/pt-BR/ARQUITETURA.md) — componentes, fluxo de dados, pagamentos, mapeamento KIX
- [Configuração](docs/pt-BR/CONFIGURACAO.md) — desenvolvimento local e todas as variáveis
- [Implantação](docs/pt-BR/IMPLANTACAO.md) — Docker, `deploy.sh`, bare-metal
- [Referência da API](docs/pt-BR/API.md) — todas as rotas/endpoints
- [Modelo de dados](docs/pt-BR/MODELO_DE_DADOS.md) — todos os models e singletons do admin
- [Contexto do Protocolo KIX](docs/pt-BR/PROTOCOLO_KIX.md) — como a loja se encaixa no PRISMA
- [Índice da documentação](docs/README.md)

## Início rápido

### Local (venv)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# copie o .env e preencha os placeholders (veja docs/pt-BR/CONFIGURACAO.md)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Docker

```bash
docker compose up -d --build
```

A aplicação fica disponível em `http://localhost:8003` (porta mapeada no `docker-compose.yml`).

> **Nota de produção:** o repositório entrega padrões permissivos (`ALLOWED_HOSTS=*`,
> `CSRF_TRUSTED_ORIGINS=['https://*', ...]`, segredos fracos de exemplo) para facilitar
> o início. Aperte-os antes de expor a loja publicamente — veja
> [Implantação → Checklist de segurança](docs/pt-BR/IMPLANTACAO.md#checklist-de-seguranca).

## Variáveis de ambiente

A aplicação lê a configuração de `.env` (via `python-dotenv`). Veja a referência
completa em [Configuração](docs/pt-BR/CONFIGURACAO.md#variaveis-de-ambiente).

| Variável | Finalidade |
|----------|-----------|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | `True`/`False` |
| `ALLOWED_HOSTS` | hosts separados por vírgula |
| `LNBITS_URL` | endpoint de pagamentos do LNbits |
| `LNBITS_API_KEY` | chave de API do LNbits |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | notificações de contato via Telegram |
| `WHATSAPP_ATIVO` / `WHATSAPP_NUMERO` / `WHATSAPP_MENSAGEM_PADRAO` | fallback do botão flutuante |

---

Licenciado sob os termos existentes do projeto. Construído sobre o
[Protocolo KIX](https://github.com/Hexarcs/KIX-PROTOCOL).
