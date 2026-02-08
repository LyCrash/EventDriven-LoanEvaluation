import json
import os
from datetime import datetime
from shared.rabbitmq import consume_event
from shared.events import LOAN_DECIDED

# Path inside the container where the audit log will be stored
LOG_FILE_PATH = "/app/audit/loan_history.jsonl"

def audit_notification(loan):
    """
    Captures the final enriched loan object containing:
    - Initial data (client, amount, loan_id)
    - Credit data (credit_score, credit_ok)
    - Property data (property_value)
    - Result data (approved)
    """
    # Add a timestamp for the audit trail
    loan["finalized_at"] = datetime.now().isoformat()
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    # Append the full loan data as a single line in a JSONL file
    with open(LOG_FILE_PATH, "a") as f:
        f.write(json.dumps(loan) + "\n")
    
    # Visual confirmation in docker logs
    status = "✅ APPROVED" if loan["approved"] else "❌ REJECTED"
    print(f"Audit Logged: Loan {loan['loan_id']} for {loan['client']} - {status}")

print("Notification Service is active and auditing...")
consume_event(LOAN_DECIDED, audit_notification)