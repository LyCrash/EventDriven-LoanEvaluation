import pika
import json
import time

RABBITMQ_HOST = "rabbitmq"

def _connect():
    while True:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 3 seconds...")
            time.sleep(3)

def publish_event(queue: str, payload: dict):
    connection = _connect()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(payload)
    )
    connection.close()

def consume_event(queue: str, callback):
    connection = _connect()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True) 
    # durable=True i.e if RabbitMQ’s memory gets too full, it will even "spill" that data onto the Hard Drive to ensure it isn't lost

    def wrapper(ch, method, properties, body):
        callback(json.loads(body))

    channel.basic_consume(
        queue=queue,
        on_message_callback=wrapper,
        auto_ack=True # This tells RabbitMQ: "The moment you hand me the data, you can delete it from your memory/disk."
    )

    print(f"Waiting for events on queue '{queue}'")
    channel.start_consuming()
