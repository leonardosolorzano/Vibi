# Deploy & Deployment

Guía completa para desplegar la API en producción.

## Índice

1. [Servidor Virtual (VPS)](#servidor-virtual-vps)
2. [Docker](#docker)
3. [Cloud Platforms](#cloud-platforms)
4. [Monitoreo & Logs](#monitoreo--logs)
5. [SSL/HTTPS](#sslhttps)
6. [Backups](#backups)
7. [Checklist Pre-Producción](#checklist-pre-producción)

---

## Servidor Virtual (VPS)

### Opción 1: Ubuntu + Nginx + Gunicorn

#### 1. Preparar servidor

```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx

# Iniciar servicios
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 2. Crear usuario y clonar proyecto

```bash
# Crear usuario app
sudo useradd -m -s /bin/bash vibi
sudo su - vibi

# Clonar repositorio
git clone https://github.com/tu-usuario/vibi-backend.git
cd vibi-backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 3. Crear base de datos

```bash
sudo -u postgres psql

postgres=# CREATE DATABASE vibi_db;
postgres=# CREATE USER vibi_user WITH PASSWORD 'secure_password_here';
postgres=# ALTER ROLE vibi_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE vibi_user SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE vibi_user SET default_transaction_deferrable TO on;
postgres=# ALTER ROLE vibi_user SET default_transaction_deferrable TO off;
postgres=# ALTER ROLE vibi_user SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE vibi_db TO vibi_user;
postgres=# \q
```

#### 4. Configurar variables de entorno

```bash
# Copiar .env.example y editar
cp .env.example .env

# Editar con valores de producción
nano .env

# Contenido recomendado:
# DEBUG=False
# DATABASE_URL=postgresql://vibi_user:password@localhost:5432/vibi_db
# SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
# ALLOWED_HOSTS=tu-dominio.com
```

#### 5. Crear servicio Systemd

**archivo: /etc/systemd/system/vibi.service**

```ini
[Unit]
Description=Vibi API
After=network.target postgresql.service

[Service]
Type=notify
User=vibi
WorkingDirectory=/home/vibi/vibi-backend
Environment="PATH=/home/vibi/vibi-backend/venv/bin"
ExecStart=/home/vibi/vibi-backend/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    app.main:app

[Install]
WantedBy=multi-user.target
```

#### 6. Instalar y configurar Gunicorn

```bash
pip install gunicorn

# Activar servicio
sudo systemctl daemon-reload
sudo systemctl enable vibi
sudo systemctl start vibi
sudo systemctl status vibi
```

#### 7. Configurar Nginx

**archivo: /etc/nginx/sites-available/vibi**

```nginx
upstream vibi_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Limitar tamaño de upload
    client_max_body_size 10M;

    location / {
        proxy_pass http://vibi_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /var/www/vibi/static/;
        expires 30d;
    }

    # Bloquear acceso a archivos sensibles
    location ~ /\. {
        deny all;
    }
}
```

#### 8. Activar sitio y SSL

```bash
# Crear enlace simbólico
sudo ln -s /etc/nginx/sites-available/vibi /etc/nginx/sites-enabled/

# Probar configuración
sudo nginx -t

# Reiniciar
sudo systemctl restart nginx
```

---

## Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: vibi_db
      POSTGRES_USER: vibi_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vibi_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://vibi_user:${DB_PASSWORD}@db:5432/vibi_db
      DEBUG: "False"
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### Ejecutar con Docker Compose

```bash
# Crear archivo .env
echo "DB_PASSWORD=your_secure_password" > .env
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" >> .env

# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener
docker-compose down
```

---

## Cloud Platforms

### Heroku

```bash
# Instalar Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login
heroku login

# Crear app
heroku create nombre-app

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

### Railway

1. Conectar repo de GitHub
2. Seleccionar `Add Service` → PostgreSQL
3. Agregar variables:
   ```
   DATABASE_URL (auto)
   SECRET_KEY
   DEBUG=False
   ```
4. Deploy automático al hacer push

### Render

1. Crear PostgreSQL database
2. Crear Web Service
3. Conectar GitHub repo
4. Configurar environment variables
5. Deploy

### DigitalOcean App Platform

1. Conectar GitHub
2. Seleccionar `vibi-backend`
3. Crear database PostgreSQL
4. Configurar environment variables
5. Deploy

---

## Monitoreo & Logs

### Logging a Archivos

```python
# app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("vibi")
handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10000000,  # 10 MB
    backupCount=5
)
logger.addHandler(handler)
```

### Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/123456",
    traces_sample_rate=0.1,
    environment="production"
)
```

### Prometheus (Métricas)

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## SSL/HTTPS

### Let's Encrypt + Certbot

```bash
# Instalar
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot certonly --nginx -d tu-dominio.com

# Renovar automáticamente
sudo certbot renew --dry-run
```

### Nginx con SSL

```nginx
server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Configuración SSL moderna
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:8000;
        # ... resto de configuración
    }
}

# Redirigir HTTP a HTTPS
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Backups

### PostgreSQL Automático

**script: /home/vibi/backup.sh**

```bash
#!/bin/bash

BACKUP_DIR="/home/vibi/backups"
DB_NAME="vibi_db"
DB_USER="vibi_user"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Guardar últimos 7 días
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completado: db_backup_$DATE.sql.gz"
```

**Cron job (ejecutar diariamente):**

```bash
# Editar crontab
crontab -e

# Agregar línea
0 2 * * * /home/vibi/backup.sh >> /var/log/vibi_backup.log 2>&1
```

---

## Checklist Pre-Producción

```ini
[ ] DEBUG = False en .env
[ ] SECRET_KEY válido y secreto
[ ] DATABASE_URL correcta
[ ] CORS configurado a dominios específicos
[ ] ALLOWED_HOSTS actualizado
[ ] SSL/HTTPS configurado
[ ] Backups automatizados
[ ] Monitoreo habilitado (Sentry)
[ ] Logs configurados
[ ] Rate limiting implementado
[ ] Health checks funcionando
[ ] Base de datos optimizada (índices)
[ ] CDN para archivos estáticos
[ ] Autenticación JWT implementada
[ ] CSRF protection habilitado
[ ] Headers de seguridad configurados
[ ] Tests pasando (100% cobertura)
[ ] Documentación actualizada
[ ] Plan de disaster recovery
[ ] Alertas configuradas
[ ] Load balancer configurado (si aplica)
```

---

## Performance Optimization

### Caching Headers

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

@router.get("/properties")
async def get_properties(...):
    return Response(
        content=...,
        headers={
            "Cache-Control": "public, max-age=3600"  # 1 hora
        }
    )
```

### GZIP Compression

```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### Database Connection Pooling

```python
# Ya configurado en app/core/database.py
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,           # Máximo de conexiones
    max_overflow=10,        # Conexiones extra
    pool_pre_ping=True,     # Verificar conexiones
)
```

---

## Comandos Útiles en Producción

```bash
# Ver estado del servicio
sudo systemctl status vibi

# Reiniciar servicio
sudo systemctl restart vibi

# Ver logs
sudo journalctl -u vibi -f

# Acceder a la BD
psql -U vibi_user -d vibi_db

# Hacer backup
pg_dump -U vibi_user vibi_db > backup.sql

# Restaurar desde backup
psql -U vibi_user vibi_db < backup.sql
```

---

## Monitoreo de Recursos

### CPU, Memoria, Disk

```bash
# Ver uso de recursos
htop

# Ver espacio en disco
df -h

# Ver conexiones activas
netstat -an | grep ESTABLISHED | wc -l
```

### Alertas en Producción

```python
# Simplemail para alertas
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message):
    # Enviar email de alerta cuando hay error
    pass
```

---

## Conclusión

La implementación recomendada para **producción mínima** es:

1. ✅ Ubuntu + Nginx + Gunicorn
2. ✅ PostgreSQL externo (gestionado)
3. ✅ SSL con Let's Encrypt
4. ✅ Backups diarios
5. ✅ Monitoreo básico

Para **alta disponibilidad**:

1. Load Balancer
2. Múltiples instancias de API
3. PostgreSQL replicada
4. CDN para assets
5. Monitoreo avanzado (Prometheus + Grafana)
