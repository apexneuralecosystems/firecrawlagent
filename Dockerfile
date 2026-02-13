# -----------------------------------------------------------------------------
# Stage 1: Build Vite frontend (same-origin API in production)
# -----------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /app

ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --omit=dev || npm install

COPY frontend/ .
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 2: Runtime (Python + nginx)
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS runner
WORKDIR /app

# Install nginx + netcat for startup health-check only (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

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
RUN nginx -t

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENV NODE_ENV=production
ENV PORT=3000
ENV BACKEND_PORT=8000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD nc -z 127.0.0.1 3000 || exit 1

CMD ["/start.sh"]
