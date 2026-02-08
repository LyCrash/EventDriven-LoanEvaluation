from celery import Celery
from shared.rabbitmq import publish_event
from shared.events import LOAN_DECIDED
import time

celery_app = Celery(
    "decision_tasks",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0"
)
celery_app.conf.task_default_queue = 'decision_queue'

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 2})
def generate_documents_task(self, loan):
    # Simulate heavy work
    time.sleep(5)

    loan["repayment_plan_generated"] = True
    publish_event(LOAN_DECIDED, loan)
