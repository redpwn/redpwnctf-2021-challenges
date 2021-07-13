FROM node:16

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY app.js ./
COPY views ./views

CMD [ "node", "app.js" ]
