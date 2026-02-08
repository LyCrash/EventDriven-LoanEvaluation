FROM python:3.11-slim

WORKDIR /app

# Copy service code
COPY credit-service/main.py credit-service/tasks.py ./

# Shared
COPY shared/ /app/shared/

RUN pip install fastapi uvicorn pika celery redis

CMD ["python", "main.py"]
