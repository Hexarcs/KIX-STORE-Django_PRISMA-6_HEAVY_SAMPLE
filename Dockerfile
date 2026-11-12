# Usa uma imagem oficial e leve do Python (perfeita para o seu Debian)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as bibliotecas do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia o projeto
COPY . /app/

EXPOSE 8000

# Inicia o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
