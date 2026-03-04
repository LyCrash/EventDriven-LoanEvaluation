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
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )
    
    connection.close()

## Previous consumer > before consistency
# def consume_event(queue: str, callback):
#     connection = _connect()
#     channel = connection.channel()
#     channel.queue_declare(queue=queue, durable=True) 
#     # durable=True i.e if RabbitMQ’s memory gets too full, it will even "spill" that data onto the Hard Drive to ensure it isn't lost

#     def wrapper(ch, method, properties, body):
#         callback(json.loads(body))

#     channel.basic_consume(
#         queue=queue,
#         on_message_callback=wrapper,
#         auto_ack=True # This tells RabbitMQ: "The moment you hand me the data, you can delete it from your memory/disk."
#     )

#     print(f"Waiting for events on queue '{queue}'")
#     channel.start_consuming()

# New consumer > for consistency
def consume_event(queue: str, callback):
    connection = _connect()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    def wrapper(ch, method, properties, body):
        try:
            callback(json.loads(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue=queue, on_message_callback=wrapper)
    print(f"Waiting for events on queue '{queue}'")
    channel.start_consuming()