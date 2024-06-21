FROM node:22.3.0-alpine

# Set the working directory for the Node.js application
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port for the Node.js application
EXPOSE 8080

# Start Node.js application
CMD npm run start
