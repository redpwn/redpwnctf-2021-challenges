FROM ubuntu:20.04 AS app
ADD ./libc.tar.gz /
RUN sed -i '1s/^/\/lib64\n/' /etc/ld.so.conf && /sbin/ldconfig -v && \
    rm /lib/x86_64-linux-gnu/libc.so.6

FROM redpwn/jail:v0.0.2

COPY --from=app / /srv
COPY bin/* /srv/app/
COPY hook.sh /jail/hook.sh

ENV JAIL_POW=100000
ENV JAIL_PIDS=10
