FROM node:16-buster-slim

COPY package.json yarn.lock /app/
WORKDIR /app

ENV NODE_ENV production
ENV FASTIFY_SECRET ef3f4b9dde3f514320f1a837ae6d71d60e912451da59b7313a8a3091d1de7384
ENV FLAG flag{w0w_4n07h3r_60lf1n6_ch4ll3n63}
RUN yarn

COPY . .

EXPOSE 3000

CMD ["node", "/app/index.js"]

