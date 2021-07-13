FROM redpwn/jail:v0.0.2

COPY --from=debian:bullseye / /srv
COPY out /srv/app
COPY deploy/bootstrap.sh /srv/app/run
COPY flag1.txt flag2.txt /srv/app/

# HACK to get RUNPATH ${ORIGIN} to resolve correctly without a procfs
# in the chroot
RUN mkdir -p /srv/proc/self && ln -s /app/bin/chall /srv/proc/self/exe
