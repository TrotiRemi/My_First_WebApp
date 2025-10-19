# Utilise une image Python officielle
FROM python:3.10-slim

# Définit le dossier de travail
WORKDIR /app

# Copie le code source dans le conteneur
COPY . .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["python", "app.py"]
