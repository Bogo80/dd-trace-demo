FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# ddtrace-run patches Flask automatically at startup
CMD ["python", "app.py"]
