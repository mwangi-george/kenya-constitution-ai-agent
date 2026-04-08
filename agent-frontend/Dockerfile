# ------------------------
# Stage 1: Build React app
# ------------------------
FROM node:22-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and lock file first (for caching dependencies)
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy rest of the app
COPY . .

# Build the React app
RUN npm run build

# ------------------------
# Stage 2: Serve with nginx
# ------------------------
FROM nginx:alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy built React files (not public!)
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config (SPA fallback)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
