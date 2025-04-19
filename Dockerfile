FROM python:3.11-slim

WORKDIR /app

COPY legacy_airline_system.py .

CMD ["python", "legacy_airline_system.py"]
