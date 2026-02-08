from shared.rabbitmq import consume_event, publish_event
from shared.events import PROPERTY_EVALUATED, LOAN_DECIDED

def make_decision(loan):
    approved = loan["credit_ok"] and loan["property_value"] >= loan["amount"]
    loan["approved"] = approved

    publish_event(LOAN_DECIDED, loan)

consume_event(PROPERTY_EVALUATED, make_decision)
