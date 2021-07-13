FROM golang:1.16.5-buster AS golf

WORKDIR /golf
RUN git clone -n https://github.com/redpwn/rctf-golf . && git checkout 0710a69ce5e82731bbd29ceef639b32039bf51a6 && go build ./cmd/rctfgolf

FROM ubuntu:20.04 as app
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

FROM redpwn/jail:v0.0.2

COPY --from=app / /srv
COPY --from=golf /golf/rctfgolf /srv/app/
COPY bin/* /srv/app/
COPY hook.sh /jail/hook.sh

ENV JAIL_PIDS=25
