FROM node:22.3.0-alpine

# Install Redis
RUN apk add --no-cache redis

# Set the working directory for the Node.js application
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose ports for the Node.js application and Redis
EXPOSE 8080 6379

# Create a directory for Redis data
RUN mkdir -p /data

# Set the volume to persist Redis data
VOLUME ["/data"]

# Start Redis and Node.js application
CMD redis-server --daemonize yes --dir /data && npm run start

