from celery import Celery
import random, time
from shared.rabbitmq import publish_event
from shared.events import CREDIT_CHECKED

celery_app = Celery(
    "credit_tasks",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0"
)
celery_app.conf.task_default_queue = 'credit_queue'

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def check_credit_task(self, loan):
    credit_score = random.randint(300, 850)
    time.sleep(6)  # simulate heavy credit analysis

    loan["credit_score"] = credit_score
    loan["credit_ok"] = credit_score >= 600

    publish_event(CREDIT_CHECKED, loan)
