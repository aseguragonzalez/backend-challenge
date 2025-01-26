FROM rnwood/smtp4dev:latest

WORKDIR /home/smtp4dev

COPY ./healthcheck.sh /home/smtp4dev/healthcheck.sh

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
    && chmod +x /home/smtp4dev/healthcheck.sh

EXPOSE 25
EXPOSE 80
