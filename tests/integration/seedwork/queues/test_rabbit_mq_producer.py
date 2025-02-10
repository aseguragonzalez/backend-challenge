import pytest

from src.seedwork.infrastructure.queues.rabbit_mq import ProducerSettings, RabbitMqProducer


@pytest.mark.integration
def test_send_message_should_publish_messages(faker, rabbitmq_connection):
    exchange = faker.word()
    queue = faker.word()
    routing_key = faker.word()
    with rabbitmq_connection.channel() as channel:
        channel.exchange_declare(exchange=exchange, exchange_type="direct")
        channel.queue_declare(queue=queue)
        channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
    settings = ProducerSettings(exchange=exchange, routing_key=routing_key)
    message = faker.sentence().encode("utf-8")

    with RabbitMqProducer(connection=rabbitmq_connection, settings=settings) as producer:
        producer.send_message(message)

    with rabbitmq_connection.channel() as channel:
        (_, _, body) = channel.basic_get(queue=queue, auto_ack=True)
        assert body == message
