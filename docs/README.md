# KIX Store — Documentation

This is the full documentation index for the KIX Store (Supermercado KIX) project.
Primary language is English; every page has a Portuguese (pt-BR) counterpart.

## Index

| Topic | English | Português |
|-------|---------|-----------|
| Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) | [ARQUITETURA.md](pt-BR/ARQUITETURA.md) |
| Setup & configuration | [SETUP.md](SETUP.md) | [CONFIGURACAO.md](pt-BR/CONFIGURACAO.md) |
| Prerequisites (Git & Docker) | [PREREQUISITES.md](PREREQUISITES.md) | [PREREQUISITOS.md](pt-BR/PREREQUISITOS.md) |
| Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) | [IMPLANTACAO.md](pt-BR/IMPLANTACAO.md) |
| API reference | [API.md](API.md) | [API.md](pt-BR/API.md) |
| Data model | [DATA_MODEL.md](DATA_MODEL.md) | [MODELO_DE_DADOS.md](pt-BR/MODELO_DE_DADOS.md) |
| KIX protocol context | [KIX_PROTOCOL.md](KIX_PROTOCOL.md) | [PROTOCOLO_KIX.md](pt-BR/PROTOCOLO_KIX.md) |

## Suggested reading order

1. **Architecture** — get the mental model of how the pieces fit together.
2. **Setup & configuration** — run it locally and understand every setting.
3. **Data model** — learn the Django models and the admin singletons.
4. **API reference** — see every route and what it returns.
5. **Prerequisites** — install Git and Docker before deploying.
6. **Deployment** — ship it with Docker or bare-metal.
7. **KIX protocol context** — map the store onto the PRISMA layers.

## Maintenance

Known quirks and deferred fixes are tracked in
[`future_improvements.txt`](../future_improvements.txt) at the repository root.
