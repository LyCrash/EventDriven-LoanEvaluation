FROM python:3.11-slim

WORKDIR /app

# Copy service code
COPY property-service/main.py property-service/tasks.py ./

# Shared
COPY shared/ /app/shared/

RUN pip install fastapi uvicorn pika celery redis

CMD ["python", "main.py"]
