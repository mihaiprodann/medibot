# Folosește Python 3.11 ca imagine de bază
FROM python:3.11

# Setează directorul de lucru în container
WORKDIR /app

# Copiază fișierul requirements.txt din directorul `app` în container și instalează dependențele
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază toate fișierele din directorul `app` în container
COPY app/ .

# Expune portul necesar (Fly.io va redirecționa automat traficul către portul specificat în `fly.toml`)
EXPOSE 8080

# Rulează scriptul principal
CMD ["python", "main.py"]
