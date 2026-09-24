#  builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# final
FROM python:3.12-slim

WORKDIR /app

# Utilisateur non-root (sécurité)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copie uniquement les dépendances installées depuis le builder
COPY --from=builder /install /usr/local

# Copie le code source
COPY app/ app/

# Copie les fichiers nécessaires au démarrage
COPY alembic/ alembic/
COPY alembic.ini .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
