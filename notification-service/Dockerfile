FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copy service code
COPY notification-service/ .

# Shared
COPY shared/ /app/shared/

RUN pip install fastapi uvicorn pika

#CMD ["python", "main.py"]
