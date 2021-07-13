FROM sagemath/sagemath:9.0-py3

USER root

RUN useradd -m app \
 && mkdir -m 700 /home/app/.sage \
 && chown app:app /home/app/.sage
RUN sage --pip install pycryptodome
ENV HOME /home/app
COPY flag.txt /
COPY secret.txt /
COPY server.sage /home/app/

USER app
WORKDIR /
CMD ["sage", "/home/app/server.sage"]

EXPOSE 9999

