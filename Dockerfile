# -----------------------------------------------------------------------------
# Stage 1: Build Vite frontend (same-origin API in production)
# -----------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /app

# Build with empty API URL so browser uses same origin; nginx will proxy /api to backend
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

# Install nginx and netcat for health-check wait
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Backend Python dependencies (root has workflow/llama deps; backend adds asyncpg/psycopg2)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Application code (excluding dev artifacts via .dockerignore)
COPY . .

# Overlay frontend build from stage 1 (replaces any placeholder)
COPY --from=frontend-builder /app/dist ./frontend/dist

# Nginx: remove defaults and use our config
RUN rm -rf /etc/nginx/sites-enabled /etc/nginx/sites-available 2>/dev/null || true
COPY nginx.conf /etc/nginx/nginx.conf
RUN nginx -t || (echo "=== NGINX CONFIG ERROR ===" && cat /etc/nginx/nginx.conf && exit 1)

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Ports: 3000 = public (nginx), 8000 = backend (FastAPI) – keep different
ENV NODE_ENV=production
ENV PORT=3000
ENV BACKEND_PORT=8000

EXPOSE 3000

CMD ["/start.sh"]
