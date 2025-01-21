from src.seedwork.infrastructure.queues.rabbit_mq import ConsumerSettings, RabbitMqConsumer


def test_start_should_retrieves_messages_until_cancel(faker, rabbitmq_connection):
    exchange = faker.word()
    queue = faker.word()
    routing_key = faker.word()
    message = faker.sentence().encode("utf-8")
    with rabbitmq_connection.channel() as channel:
        channel.exchange_declare(exchange=exchange, exchange_type="direct")
        channel.queue_declare(queue=queue)
        channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    settings = ConsumerSettings(queue_name=queue)
    with RabbitMqConsumer(connection=rabbitmq_connection, settings=settings) as consumer:

        def _message_callback(actual_message):
            consumer.cancel()
            assert actual_message == message

        consumer.start(message_handler=_message_callback)
