# ==========================
# 1️⃣ Build Stage — Node.js
# ==========================
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files first (for dependency caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY . .

# Build the production-optimized React app
RUN npm run build

# ==========================
# 2️⃣ Production Stage — Nginx
# ==========================
FROM nginx:stable-alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy build output from Node stage to Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom Nginx configuration file (optional, can skip if not using one)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 3000 (React default) or 80 (Nginx default)
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
