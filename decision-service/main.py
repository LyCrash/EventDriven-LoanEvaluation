# from shared.rabbitmq import consume_event
# from shared.events import PROPERTY_EVALUATED
# from tasks import generate_documents_task

# def decide(loan):
#     loan["approved"] = loan["credit_ok"] and loan["property_value"] >= loan["amount"]
#     generate_documents_task.delay(loan)

# consume_event(PROPERTY_EVALUATED, decide)

import threading
from shared.rabbitmq import consume_event, publish_event
from shared.events import (
    PROPERTY_EVALUATED,
    PROPERTY_EVALUATION_FAILED,
    CREDIT_COMPENSATE,
    LOAN_DECIDED
)
from tasks import generate_documents_task

# -------------------------
# Existing Exercise 2 Logic
# -------------------------

def decide(loan):
    loan["approved"] = loan["credit_ok"] and loan["property_value"] >= loan["amount"]
    generate_documents_task.delay(loan)

# -------------------------
# Exercise 3 Failure Reaction
# -------------------------

def on_property_failure(loan):
    print(f"[SAGA] Property evaluation failed. Triggering credit compensation for {loan['loan_id']}")
    publish_event(CREDIT_COMPENSATE, loan)
    loan["approved"] = False
    loan["failure_reason"] = "Property evaluation failed"
    publish_event(LOAN_DECIDED, loan)

# -------------------------
# Run Consumers in Threads
# -------------------------

if __name__ == "__main__":
    print("Decision Service started")
    threading.Thread(
        target=consume_event,
        args=(PROPERTY_EVALUATED, decide),
        daemon=True
    ).start()

    threading.Thread(
        target=consume_event,
        args=(PROPERTY_EVALUATION_FAILED, on_property_failure),
        daemon=True
    ).start()

    while True:
        pass