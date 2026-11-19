# ─── Stage 1: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copia arquivos de manifesto e lockfile de dependencias
COPY package.json package-lock.json ./

# Instala as dependencias de forma deterministica
RUN npm ci --silent

# Copia apenas os artefatos necessarios ao build (evita copiar .env ou .git)
COPY index.html vite.config.js .eslintrc.cjs ./
COPY src/ ./src/
RUN npm run build

# ─── Stage 2: Serve ──────────────────────────────────────────────────────────
FROM nginx:alpine AS runner

LABEL org.opencontainers.image.title="est-web-frontend-echo" \
      org.opencontainers.image.description="Frontend React do Sistema de Reservas Hoteleiras - Equipe Echo" \
      org.opencontainers.image.vendor="Unicatolica - Equipe Echo"

# Remove configuracao padrao do nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuracao customizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos estaticos gerados pelo Vite para o servidor nginx
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
