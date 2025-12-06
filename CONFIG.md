# Configuration et lancement de l'application

## Prerequisites

- Docker et Docker Compose doivent être installés sur ta machine
- Git pour cloner le repo (si ce n'est pas déjà fait)

## Lancer l'application

### Méthode 1 : Avec Docker Compose (recommandé)

Va à la racine du projet et lance cette commande:

```
docker compose up --build
```

Ça va:
- Créer et lancer la base de données PostgreSQL
- Builder et lancer l'API FastAPI
- Lancer le serveur frontend

L'appli sera accessible sur:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Documentation API: http://localhost:8000/docs

### Méthode 2 : En local sans Docker

Si tu veux lancer sans Docker:

1. Configure la base de données PostgreSQL localement
2. Va dans le dossier backend et active l'env virtuel:
   ```
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
   ```

3. Installe les dépendances:
   ```
   pip install -r requirements.txt
   ```

4. Applique les migrations:
   ```
   alembic upgrade head
   ```

5. Lance l'API:
   ```
   uvicorn app.main:app --reload
   ```

6. Dans un autre terminal, lance le frontend:
   ```
   cd frontend
   python -m http.server 3000
   ```

## Arrêter l'application

Si tu utilises Docker:
```
docker compose down
```

## Remplir la base de données avec des données de test

Une fois que tout est lancé:
```
docker compose exec api python -m app.seed
```

Ça crée un utilisateur de démo et quelques cours. Les credentials sont:
- Username: demo
- Password: demo

## Aide et logs

Pour voir les logs de l'API:
```
docker compose logs api
```

Pour voir tous les logs:
```
docker compose logs
```

Si quelque chose ne marche pas, essaie de rebuild:
```
docker compose up --build
```
