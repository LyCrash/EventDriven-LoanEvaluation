import json
import os
import asyncio
import threading
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from shared.rabbitmq import consume_event
from shared.events import LOAN_DECIDED

# -------------------------------------------------
# Audit Log Configuration (KEEP EXISTING)
# -------------------------------------------------

LOG_FILE_PATH = "/app/audit/loan_history.jsonl"

# Async queue for real-time push
event_queue = asyncio.Queue()
main_loop = None

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()

# -------------------------------------------------
# RabbitMQ Consumer Callback
# -------------------------------------------------

def audit_notification(loan):
    """
    Captures the final enriched loan object containing:
    - Initial data (client, amount, loan_id)
    - Credit data (credit_score, credit_ok)
    - Property data (property_value)
    - Result data (approved)
    """

    # Add timestamp (KEEP EXISTING BEHAVIOR)
    loan["finalized_at"] = datetime.now().isoformat()

    # Ensure directory exists
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    # Append full loan to JSONL audit file
    with open(LOG_FILE_PATH, "a") as f:
        f.write(json.dumps(loan) + "\n")

    # Log in container
    status = "✅ APPROVED" if loan["approved"] else "❌ REJECTED"
    print(f"Audit Logged: Loan {loan['loan_id']} for {loan['client']} - {status}")

    # Push event to async queue for WebSocket & SSE
    main_loop.call_soon_threadsafe(event_queue.put_nowait, loan)


# -------------------------------------------------
# Start RabbitMQ Consumer in Background Thread
# -------------------------------------------------

print("Notification Service is active (Audit + Realtime)...")

threading.Thread(
    target=consume_event,
    args=(LOAN_DECIDED, audit_notification),
    daemon=True
).start()

# -------------------------------------------------
# 1- WebSocket Endpoint
# -------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected via WebSocket")

    try:
        while True:
            loan = await event_queue.get()
            await websocket.send_json(loan)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")


# -------------------------------------------------
# 2- Server-Sent Events (SSE)
# -------------------------------------------------

@app.get("/sse")
async def sse_endpoint():

    async def event_generator():
        while True:
            loan = await event_queue.get()
            yield f"data: {json.dumps(loan)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# Serve dashboard static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")