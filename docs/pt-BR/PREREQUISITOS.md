# Pré-requisitos

> 🇺🇸 [English](../PREREQUISITES.md)

Tudo o que você precisa instalar na sua máquina **antes** de implantar a KIX Store com
Docker. Depois deste guia, continue em [Implantação](IMPLANTACAO.md).

A loja é uma aplicação Django distribuída como repositório Git e entregue como imagem
Docker, então você precisa de duas ferramentas no host:

1. **Git** — para clonar o código-fonte.
2. **Docker Engine + Docker Compose** — para construir e executar o container.

> ℹ️ "GitHub" é o serviço de hospedagem; **Git** é a ferramenta de linha de comando que
> você realmente instala. Uma conta no GitHub é opcional (útil para dar fork/star no
> repositório), mas não é necessária para rodar a loja.

## 1. Instalar o Git

Siga o guia oficial para o seu sistema:

- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install -y git`
- **Todas as plataformas:** [git-scm.com/downloads](https://git-scm.com/downloads)
- **Guia rápido:** [GitHub — Configurar o Git](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git)

Verifique:

```bash
git --version
```

## 2. Instalar o Docker Engine + Compose

### 2.1 Debian (repositório oficial)

Adicione a chave GPG oficial do Docker e o repositório para Debian; depois instale os
pacotes:

```bash
# 1. Instale os pacotes necessários para apt sobre HTTPS
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# 2. Crie o diretório de keyrings
sudo install -m 0755 -d /etc/apt/keyrings

# 3. Adicione a chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/debian/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Configure o repositório para o Debian
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instale o Docker Engine, CLI, containerd e o plugin Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

> 💡 **Outras distribuições** (Ubuntu, Fedora, RHEL etc.) — siga o
> [guia oficial de instalação do Docker Engine](https://docs.docker.com/engine/install/)
> e selecione a sua plataforma.

### 2.2 Adicione seu usuário ao grupo `docker` (recomendado)

Isso permite rodar `docker` sem `sudo`. O nome do grupo é `docker`, em minúsculas.

```bash
sudo usermod -aG docker "$USER"
newgrp docker
```

> ⚠️ Se o `newgrp docker` não surtir efeito (ou se você pular essa etapa), **saia e
> entre novamente** na sessão para a mudança de grupo valer.

Verifique:

```bash
docker --version
docker compose version
```

## 3. Clonar o repositório

```bash
git clone https://github.com/Hexarcs/KIX-STORE-Django_PRISMA-6_HEAVY_SAMPLE.git
cd KIX-STORE-Django_PRISMA-6_HEAVY_SAMPLE
```

> 💡 Use `ls` e confirme que existe um arquivo `Dockerfile` na raiz do repositório —
> isso garante que você está no lugar certo.

## 4. Construir a imagem (teste opcional)

O `.` no final do comando diz ao Docker para procurar um arquivo chamado `Dockerfile`
na pasta onde você está no momento.

```bash
docker build -t seu-nome/kix-store:latest .
```

Substitua `seu-nome` pelo seu nome de usuário do Docker Hub (ou qualquer tag que
preferir).

## Próximo passo

Continue em [Implantação](IMPLANTACAO.md) para executar a loja com Docker Compose
(`docker compose up -d --build`) ou bare-metal.
