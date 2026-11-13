# Configuração

> 🇺🇸 [English](../SETUP.md)

Como rodar a KIX Store localmente e configurar cada ajuste. Este documento é voltado a
um desenvolvedor com alguma familiaridade com Django.

## 1. Pré-requisitos

- Python **3.11** (a imagem Docker usa `python:3.11-slim`)
- `pip` e um ambiente virtual
- (opcional) Docker + Docker Compose para o fluxo containerizado
- Credenciais dos serviços externos que deseja usar (LNbits, Telegram)

## 2. Desenvolvimento local

```bash
# 1. crie e ative um virtualenv
python3 -m venv venv
source venv/bin/activate

# 2. instale as dependências
pip install -r requirements.txt

# 3. crie o .env a partir do modelo abaixo
cp .env.example .env   # ou crie o .env manualmente

# 4. aplique as migrações
python manage.py migrate

# 5. crie um usuário admin
python manage.py createsuperuser

# 6. colete os estáticos (opcional em dev; necessário com DEBUG=False)
python manage.py collectstatic --noinput

# 7. rode
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. O admin fica em `/admin/`.

## 3. Variáveis de ambiente

As configurações são carregadas de `.env` com `python-dotenv` (veja `core/settings.py`).
Todas as chaves abaixo são strings; `DEBUG` e booleanos aceitam `true/1/t`
(case-insensitive).

| Variável | Obrigatória | Padrão | Finalidade |
|----------|-------------|--------|------------|
| `SECRET_KEY` | sim (prod) | fallback inseguro | chave secreta do Django |
| `DEBUG` | — | `False` | ativa o modo debug do Django |
| `ALLOWED_HOSTS` | — | `*` | hosts permitidos separados por vírgula |
| `LNBITS_URL` | p/ Lightning | `https://seu-lnbits.exemplo.com/api/v1/payments` | endpoint de pagamentos LNbits |
| `LNBITS_API_KEY` | p/ Lightning | `""` | chave de API LNbits (`X-Api-Key`) |
| `TELEGRAM_BOT_TOKEN` | p/ formulário de contato | `""` | token do bot do @BotFather |
| `TELEGRAM_CHAT_ID` | p/ formulário de contato | `""` | chat ID que recebe as mensagens |
| `WHATSAPP_ATIVO` | — | `""` | toggle fallback do botão flutuante |
| `WHATSAPP_NUMERO` | — | `""` | telefone fallback (só dígitos, DDI+DDD+número) |
| `WHATSAPP_MENSAGEM_PADRAO` | — | `Olá` | mensagem padrão fallback |

Exemplo de `.env`:

```dotenv
SECRET_KEY=troque-por-uma-string-longa-e-aleatoria
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com
LNBITS_URL=https://seu-lnbits/api/v1/payments
LNBITS_API_KEY=sua-chave-lnbits
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=123456789
WHATSAPP_ATIVO=true
WHATSAPP_NUMERO=5531999999999
WHATSAPP_MENSAGEM_PADRAO=Olá
```

### 3.1. Criando o bot no Telegram (BotFather)

O formulário de contato precisa de um token de bot e do chat ID que receberá as
mensagens. Para criá-los:

1. Abra o Telegram e converse com o **@BotFather** (o bot oficial).
2. Envie `/newbot` e siga as instruções para escolher um nome de exibição e um
   username (o username precisa terminar em `bot`).
3. O BotFather responde com um token no formato `123456789:AAF...` — copie-o para
   `TELEGRAM_BOT_TOKEN`.
4. Para obter o `TELEGRAM_CHAT_ID`:
   - mande uma mensagem para o **@userinfobot** (ou envie `/start` ao seu novo bot), ou
   - envie qualquer mensagem ao seu bot e abra
     `https://api.telegram.org/bot<TOKEN>/getUpdates` para copiar o campo `chat.id`.
   Cole esse número em `TELEGRAM_CHAT_ID`.

## 4. Precedência de credenciais (env vs. admin)

Algumas configurações podem ser definidas no `.env` **ou** no Django admin. As regras:

- **Telegram** — o `.env` (`TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`) vence quando os
  dois estão definidos; caso contrário, usa-se `ConfiguracaoTelegram` (admin). Veja
  `core/services/executor.py:_resolve_credentials`.
- **Botão flutuante do WhatsApp** — o admin `ConfiguracaoWhatsApp` vence por campo;
  quando um campo está vazio no banco, usa-se o valor do `.env` como fallback. Veja
  `core/context_processors.py:whatsapp_config_processor`.

## 5. Configuração pelo Django admin

Após `createsuperuser`, entre em `/admin/` e configure os singletons. Eles controlam a
vitrine sem mudanças de código:

| Seção do admin | O que você controla |
|----------------|---------------------|
| **Configurações do Site** (`SiteConfig`) | nome da loja, logo, `<title>`, badge KIX, cores/textos do header/banner/botões |
| **Configuração do PIX** (`ConfiguracaoPix`) | chave PIX, nome do recebedor, rótulo da taxa, % da taxa, instrução do modal |
| **Configuração do Telegram** | credenciais fallback + textos do formulário de contato e on/off |
| **Configuração do Rodapé** | descrição da empresa, telefones, e-mail, endereço, URLs sociais |
| **Configuração do WhatsApp** | botão flutuante (ativo, número, mensagem) |

Outras seções do admin gerenciam dados de catálogo:

- **Categorias** (`Categoria`) — categorias de produto (o slug guia as páginas de categoria)
- **Macro Categorias** (`MacroCategoria`) — seções da vitrine (definidas, mas não
  renderizadas por `index.html`)
- **Categoria Cards** (`CategoriaCard`) — os tiles de categoria da home
- **Produtos** (`Produto`) — SKU, nome, descrição, categoria, emoji, preço em sats,
  imagem, flag "Ofertas Rápidas"
- **Serviços** (`Servico`) — cards de assessoria/concierge com contato Telegram/WhatsApp
- **Cotação Bitcoin** (`CotacaoBitcoin`) — cotação BTC/BRL em cache (gerenciada automaticamente)
- **Configurações do Hero** (`HomeConfig`) — título/subtítulo/imagem do hero

## 6. Arquivos estáticos e de mídia

- **Estáticos** (`/static/`) — origem em `core/static/`; coletados para `staticfiles/`
  pelo `collectstatic`. Servidos pelo **WhiteNoise** em produção (`DEBUG=False`).
- **Mídia** (`/media/`) — imagens enviadas (`media/`). Sempre servidas pelo Django via
  `core/urls.py`, pois o WhiteNoise não cobre mídia. Isso é intencional para
  implantações pequenas; para escala, coloque a mídia em object storage/CDN.

## 7. Opcional: login social do Google

O login do Google já vem habilitado via `allauth.socialaccount.providers.google`, mas
você precisa de credenciais OAuth do Google para usá-lo. Abra o
[Google Cloud Console](https://console.cloud.google.com/) e:

1. Crie (ou selecione) um projeto.
2. Configure a **tela de consentimento OAuth** (APIs e serviços → Tela de consentimento OAuth).
3. Vá em **APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth**.
4. Escolha **Aplicativo da Web** e adicione o URI de redirecionamento autorizado
   `https://<seu-dominio>/accounts/google/login/callback/`.
5. Baixe o `client_secret_*.json` e coloque na raiz do projeto.

Depois habilite no Django:

6. Em `/admin/`, em **Social Applications**, adicione o provedor "Google" com seu
   client ID/secret e anexe-o ao site (`SITE_ID=1`).
7. O arquivo `client_secret_*.json` no repositório é um exemplo e é ignorado pelo git.

O login local por usuário/e-mail funciona de imediato
(`ACCOUNT_ALLOW_REGISTRATION=True`, `ACCOUNT_EMAIL_VERIFICATION='none'`).
