FROM wiremock/wiremock:3.9.1

WORKDIR /home/wiremock

COPY . .

EXPOSE 8080
EXPOSE 8443

ENTRYPOINT ["/docker-entrypoint.sh", "--global-response-templating", "--disable-gzip", "--verbose"]
