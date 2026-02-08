from shared.rabbitmq import consume_event
from shared.events import LOAN_CREATED
from tasks import check_credit_task

def on_loan_created(loan):
    check_credit_task.delay(loan)

consume_event(LOAN_CREATED, on_loan_created)
