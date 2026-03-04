# from shared.rabbitmq import consume_event
# from shared.events import LOAN_CREATED
# from tasks import check_credit_task

# def on_loan_created(loan):
#     check_credit_task.delay(loan)

# consume_event(LOAN_CREATED, on_loan_created)

import threading
from shared.rabbitmq import consume_event
from shared.events import LOAN_CREATED, CREDIT_COMPENSATE
from tasks import check_credit_task

# -------------------------
# Existing Exercise 2 Logic
# -------------------------

def on_loan_created(loan):
    check_credit_task.delay(loan)

# -------------------------
# Exercise 3 Compensation
# -------------------------

def compensate_credit(loan):
    loan["credit_score"] = None
    loan["credit_ok"] = False
    loan["credit_status"] = "COMPENSATED"
    print(f"[COMPENSATION] Credit rolled back for loan {loan['loan_id']}")

# -------------------------
# Run Consumers in Threads
# -------------------------

if __name__ == "__main__":
    print("Credit Service started")
    threading.Thread(
        target=consume_event,
        args=(LOAN_CREATED, on_loan_created),
        daemon=True
    ).start()

    threading.Thread(
        target=consume_event,
        args=(CREDIT_COMPENSATE, compensate_credit),
        daemon=True
    ).start()

    # Keep main thread alive
    while True:
        pass