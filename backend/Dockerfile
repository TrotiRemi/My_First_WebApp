FROM python:3.10-slim

WORKDIR /app

# Copie d'abord juste requirements pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensuite copie tout le code
COPY . .

# Expose le port
EXPOSE 8000

# Commande par défaut
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]