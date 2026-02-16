# -----------------------------------------------------------------------------
# Stage 1: Build Vite frontend (same-origin API in production)
# -----------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /app

ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

COPY frontend/package.json frontend/package-lock.json* ./
ARG CACHE_BUST=1
RUN npm ci

COPY frontend/ .
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 2: Runtime (Python + nginx)
# -----------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS runner
WORKDIR /app

# Install nginx + netcat for startup health-check only (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser

# Python deps: root (full app) then backend extras (asyncpg, psycopg2)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Application code
COPY . .

# Overlay built frontend (no node_modules in image)
COPY --from=frontend-builder /app/dist ./frontend/dist

# Nginx: replace default config and validate
RUN rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
COPY nginx.conf /etc/nginx/nginx.conf
RUN chown appuser:appgroup /etc/nginx/nginx.conf && chmod 644 /etc/nginx/nginx.conf
RUN nginx -t


COPY start.sh /start.sh
RUN chmod +x /start.sh

# Allow non-root user to run nginx and write to required dirs
RUN mkdir -p /var/lib/nginx/body /var/lib/nginx/proxy /var/lib/nginx/fastcgi \
    /var/lib/nginx/uwsgi /var/lib/nginx/scgi /var/log/nginx /run && \
    chown -R appuser:appgroup /app /var/lib/nginx /var/log/nginx /run /var/cache/nginx /etc/nginx 2>/dev/null || true && \
    # nginx needs to write its pid
    touch /run/nginx.pid && chown appuser:appgroup /run/nginx.pid


ENV NODE_ENV=production
ENV PORT=3000
ENV BACKEND_PORT=8000
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

EXPOSE 3000

# Switch to non-root user
USER appuser

CMD ["/start.sh"]

