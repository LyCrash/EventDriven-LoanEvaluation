from shared.rabbitmq import consume_event
from shared.events import PROPERTY_EVALUATED
from tasks import generate_documents_task

def decide(loan):
    loan["approved"] = loan["credit_ok"] and loan["property_value"] >= loan["amount"]
    generate_documents_task.delay(loan)

consume_event(PROPERTY_EVALUATED, decide)
