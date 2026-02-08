FROM python:3.11-slim

WORKDIR /app

# Copy service code
COPY property-service/main.py .

# Shared
COPY shared/ /app/shared/

RUN pip install fastapi uvicorn pika

CMD ["python", "main.py"]
