from shared.rabbitmq import consume_event
from shared.events import CREDIT_CHECKED
from tasks import property_evaluation_task

def on_credit_checked(loan):
    property_evaluation_task.delay(loan)

consume_event(CREDIT_CHECKED, on_credit_checked)
