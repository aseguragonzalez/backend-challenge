#!/bin/bash

rabbitmq-diagnostics ping

rabbitmqadmin -u guest -p guest -V / list exchanges name | grep -q "events.ex"
exchange_status=$?

rabbitmqadmin -u guest -p guest -V / list queues name | grep -q "events"
queue_status=$?

if [ $exchange_status -eq 0 ] && [ $queue_status -eq 0 ]; then
  echo "RabbitMQ is running and the exchange and queue exist"
  exit 0
else
  echo "RabbitMQ is not running or the exchange and queue do not exist"
  exit 1
fi
