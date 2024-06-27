FROM node:22.3.0-alpine
WORKDIR /usr/src/nodejsserver
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080
CMD npm run start


