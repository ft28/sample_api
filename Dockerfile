FROM python:3.10-slim

WORKDIR /app
ADD api_server.py .

CMD ["python", "api_server.py"]
