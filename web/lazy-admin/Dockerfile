FROM node:16-buster-slim

ENV NODE_ENV production
ENV FLAG flag{d15c0rd_b07_n07_r34lly_n3c3554ry}

WORKDIR /client
COPY client/package.json client/yarn.lock /client/
RUN yarn

WORKDIR /server
COPY server/package.json server/yarn.lock /server/
RUN yarn

WORKDIR /
COPY client /client
COPY server /server
COPY entrypoint.sh ./

EXPOSE 80

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--", "/entrypoint.sh"]
