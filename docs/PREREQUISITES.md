# Prerequisites

> 🇧🇷 [Português](pt-BR/PREREQUISITOS.md)

Everything you need installed on your machine **before** deploying the KIX Store with
Docker. After this guide, continue with [Deployment](DEPLOYMENT.md).

The store is a Django application distributed as a Git repository and shipped as a
Docker image, so you need two tools on the host:

1. **Git** — to clone the source code.
2. **Docker Engine + Docker Compose** — to build and run the container.

> ℹ️ "GitHub" is the hosting service; **Git** is the command-line tool you actually
> install. A GitHub account is optional (useful to fork/star the repository), but not
> required to run the store.

## 1. Install Git

Follow the official guide for your operating system:

- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install -y git`
- **All platforms:** [git-scm.com/downloads](https://git-scm.com/downloads)
- **Quick start:** [GitHub — Set up Git](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git)

Verify:

```bash
git --version
```

## 2. Install Docker Engine + Compose

### 2.1 Debian (official repository)

Add the official Docker GPG key and the Debian repository, then install the packages:

```bash
# 1. Install packages required for apt over HTTPS
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# 2. Create the keyring directory
sudo install -m 0755 -d /etc/apt/keyrings

# 3. Add the official Docker GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Add the Debian repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Install Docker Engine, CLI, containerd and the Compose plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

> 💡 **Other distributions** (Ubuntu, Fedora, RHEL, etc.) — follow the official
> [Docker Engine install guide](https://docs.docker.com/engine/install/) and select
> your platform.

### 2.2 Add your user to the `docker` group (recommended)

This lets you run `docker` without `sudo`. The group name is lowercase `docker`.

```bash
sudo usermod -aG docker "$USER"
newgrp docker
```

> ⚠️ If `newgrp docker` has no effect (or you skip it), **log out and log back in** for
> the group change to take effect.

Verify:

```bash
docker --version
docker compose version
```

## 3. Clone the repository

```bash
git clone https://github.com/Hexarcs/KIX-STORE-Django_PRISMA-6_HEAVY_SAMPLE.git
cd KIX-STORE-Django_PRISMA-6_HEAVY_SAMPLE
```

> 💡 Run `ls` and confirm a `Dockerfile` is listed at the repository root — that means
> you are in the right place.

## 4. Build the image (optional smoke test)

The `.` at the end tells Docker to look for a `Dockerfile` in the current directory.

```bash
docker build -t your-name/kix-store:latest .
```

Replace `your-name` with your Docker Hub username (or any tag you prefer).

## Next step

Continue with [Deployment](DEPLOYMENT.md) to run the store with Docker Compose
(`docker compose up -d --build`) or bare-metal.
