from fastapi import FastAPI
from shared.rabbitmq import publish_event
from shared.events import LOAN_CREATED
import uuid

app = FastAPI(title="Loan Service")

@app.post("/loans")
def create_loan(loan: dict):
    loan_id = str(uuid.uuid4())
    loan["loan_id"] = loan_id

    publish_event(LOAN_CREATED, loan)

    return {
        "message": "Loan application created",
        "loan_id": loan_id
    }
