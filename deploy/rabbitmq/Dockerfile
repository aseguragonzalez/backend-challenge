FROM rabbitmq:3.12.0-management

COPY ./settings ./etc/rabbitmq/
COPY ./healthcheck.sh /etc/rabbitmq/

RUN chmod +x /etc/rabbitmq/healthcheck.sh

EXPOSE 5672
EXPOSE 15672
