from shared.rabbitmq import consume_event, publish_event
from shared.events import LOAN_CREATED, CREDIT_CHECKED
import random

def process_loan(loan):
    credit_score = random.randint(300, 850)
    loan["credit_score"] = credit_score
    loan["credit_ok"] = credit_score >= 600

    publish_event(CREDIT_CHECKED, loan)

consume_event(LOAN_CREATED, process_loan)
