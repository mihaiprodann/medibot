FROM python:3.11

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY .env .env

RUN apt-get update && apt-get install -y postgresql-client
RUN echo "source /app/.env && alias dbconnect='echo psql \$DATABASE_URL'" >> ~/.bashrc

CMD ["python", "main.py"]
