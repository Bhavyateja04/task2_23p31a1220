FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app
ENV PYTHONPATH="/app"

# Install cron + timezone + procps for debugging (pgrep/ps)
RUN apt-get update && apt-get install -y cron tzdata procps && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo UTC > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy Python deps from builder
COPY --from=builder /install /usr/local

# Copy app code
COPY app app
COPY scripts scripts
COPY cron/2fa-cron cron/2fa-cron

# Copy keys
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Permissions for cron file & install it
RUN chmod 0644 /app/cron/2fa-cron && \
    crontab /app/cron/2fa-cron

# Create persistent directories
RUN mkdir -p /data /cron

EXPOSE 8080

# Run cron in foreground + start FastAPI
CMD ["sh", "-c", "cron -f & uvicorn app.main:app --host 0.0.0.0 --port 8080"]
