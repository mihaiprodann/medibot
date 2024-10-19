FROM python:3.11

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY .env .env

CMD ["python", "main.py"]
