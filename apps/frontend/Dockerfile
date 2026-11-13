# ─── Stage 1: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copia arquivos de dependencias
COPY package.json package-lock.json ./

# Instala as dependencias
RUN npm ci --silent

# Copia so o que o build precisa: COPY . . levaria .env, .git e afins para a imagem
COPY index.html vite.config.js .eslintrc.cjs ./
COPY src/ ./src/
RUN npm run build

# ─── Stage 2: Serve ──────────────────────────────────────────────────────────
FROM nginx:alpine AS runner

# Remove configuracao padrao do nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuracao customizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos buildados para o servidor nginx
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
