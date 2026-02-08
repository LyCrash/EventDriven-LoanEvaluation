from celery import Celery
import random, time
from shared.rabbitmq import publish_event
from shared.events import PROPERTY_EVALUATED

celery_app = Celery(
    "property_tasks",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0"
)
celery_app.conf.task_default_queue = 'property_queue'

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def property_evaluation_task(self, loan):
    loan["property_value"] = random.randint(100_000, 500_000)
    time.sleep(8)  # simulate market analysis
    publish_event(PROPERTY_EVALUATED, loan)
