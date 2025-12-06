# Cloud School - Application de gestion scolaire

## Vue d'ensemble

Cloud School est une application web qui permet aux étudiants de centraliser et d'organiser leurs cours, documents et notes en un seul endroit. C'est une alternative simple aux solutions complexes ou à garder des documents dispersés un peu partout.

## Fonctionnalités principales

### Authentification et profil utilisateur

Les utilisateurs peuvent créer un compte avec un email et un mot de passe. Une fois connectés, ils reçoivent un token JWT qui sécurise l'accès à leurs données.

### Gestion des cours

Chaque utilisateur peut créer autant de cours qu'il veut. Pour chaque cours, il y a un titre, une description optionnelle et des dates (début/fin). Les cours peuvent être supprimés à tout moment.

### Gestion des documents

Dans chaque cours, on peut ajouter des documents de deux façons:
- En uploadant un fichier depuis l'ordinateur
- En fournissant un lien vers un fichier externe

Chaque document a un titre et un type (cours, exercice, TD, correction, partiel, etc). Les documents s'affichent avec une petite icône et une couleur selon leur type pour les retrouver facilement.

### Visualisation et téléchargement

Les documents qui sont des images, PDF ou fichiers texte s'affichent directement. Les autres fichiers peuvent être téléchargés via un lien.

### Sessions

Quand on se connecte, une session est créée. Quand on se déconnecte, la session est supprimée. Cela aide à tracker les utilisateurs actifs.

## Ce que le site fait - Frontend

Le frontend est une page HTML avec une interface simple et responsive. Voici ce qu'on peut faire:

### Page d'accueil

Un formulaire d'authentification avec deux onglets: un pour se connecter, un pour créer un compte. Le design utilise une palette de couleurs beige, bleu ciel et orange pour un look moderne et épuré.

### Tableau de bord utilisateur (après connexion)

Une fois connecté, on voit la liste de tous ses cours sous forme de cartes. On peut:
- Cliquer sur un cours pour voir ses documents
- Ajouter un nouveau cours via un bouton "+"
- Supprimer un cours (avec confirmation)
- Se déconnecter

### Détail d'un cours

En ouvrant un cours, on voit:
- Le titre, la description et les dates du cours
- Tous les documents classés par type (cours, exercices, corrections, etc)
- Un bouton pour ajouter un nouveau document
- Les documents s'affichent avec une petite icône et une couleur unique selon leur type

### Upload de documents

On peut ajouter un document en:
- Uploadant un fichier depuis l'ordinateur
- Ou en donnant un lien URL externe
- En choisissant le type (cours, exercice, partiel...)

Les fichiers uploadés sont stockés sur le serveur et accessibles via un lien sécurisé.

### Affichage des documents

Les images s'affichent directement. Les PDF s'affichent aussi directement (preview). Les fichiers texte et markdown peuvent être lus. Les autres types de fichiers (Word, etc) affichent une icône avec option de téléchargement.

## Ce que le site fait - Backend

Le backend est une API FastAPI qui gère toute la logique métier et les données.

### Authentification et sécurité

L'API fournit des endpoints pour s'inscrire et se connecter. Quand on se connecte, on reçoit un JWT token qu'on doit envoyer dans le header de chaque requête. Ce token est valide pendant 7 jours.

Les endpoints sensibles (créer un cours, ajouter un document, etc) nécessitent d'être authentifié. L'API vérifie que chaque utilisateur n'accède qu'à ses propres données.

### Gestion des données

L'API stocke dans la base de données:
- Les utilisateurs (email, username, password hashé)
- Les cours de chaque utilisateur
- Les documents de chaque cours
- Les sessions actives de chaque utilisateur

### Endpoints principales

L'API expose ces endpoints (on peut les tester sur /docs):

Authentification:
- POST /auth/signup - Créer un compte
- POST /auth/login - Se connecter
- GET /auth/me - Récupérer son profil
- POST /auth/logout - Se déconnecter

Cours:
- GET /courses/ - Récupérer tous ses cours
- POST /courses/ - Créer un nouveau cours
- DELETE /courses/{id} - Supprimer un cours

Documents:
- GET /documents/course/{course_id} - Récupérer les docs d'un cours
- POST /documents/upload/{course_id} - Uploader un fichier
- POST /documents/ - Créer un doc avec un lien URL
- GET /documents/download/{filename} - Télécharger un fichier
- DELETE /documents/{id} - Supprimer un doc

### Gestion des uploads

Les fichiers uploadés sont stockés dans un dossier (par défaut ./uploads). Les noms de fichier sont anonymisés pour la sécurité. Quand on supprime un document, le fichier est aussi supprimé du serveur.

### Gestion des erreurs

L'API retourne des codes HTTP standards:
- 200/201: Success
- 400: Mauvaise requête (données invalides)
- 401: Pas authentifié
- 403: Accès refusé (pas le propriétaire)
- 404: Ressource non trouvée
- 422: Données invalides (validation Pydantic)

## Comment ça marche - Flux utilisateur complet

1. L'utilisateur arrive sur http://localhost:3000
2. Il crée un compte ou se connecte
3. Le frontend envoie les credentials au backend via POST /auth/signup ou /auth/login
4. Le backend crée l'utilisateur ou vérifie les credentials, puis retourne un JWT token
5. Le frontend stocke le token dans localStorage
6. L'utilisateur voit sa liste de cours vide
7. Il clique sur "Ajouter un cours" et remplit le formulaire
8. Le frontend envoie les données au backend avec le JWT token dans le header
9. Le backend crée le cours dans la base de données
10. Le frontend affiche le nouveau cours
11. L'utilisateur ouvre le cours et clique sur "Ajouter un document"
12. Il peut uploader un fichier ou donner un lien
13. Le backend reçoit le fichier ou le lien, le stocke, et le sauvegarde en base
14. Le frontend affiche le document avec son icône et sa couleur selon le type

À chaque action, le JWT token est envoyé pour vérifier que c'est bien l'utilisateur qui fait l'action.

## Architecture technique

Le frontend communique avec le backend par des requêtes HTTP (REST). Le backend communique avec PostgreSQL pour stocker les données. Alembic gère les migrations de la base de données. Les fichiers uploadés sont stockés sur le disque du serveur.

## Points d'intérêt technique

- Sécurité: tokens JWT qui expirent, vérification des permissions, noms de fichiers anonymisés
- Migrations auto: la base de données se met à jour automatiquement au démarrage
- Stockage sécurisé: les uploads ne sont pas accessibles directement, seulement via l'API
- Responsive: le frontend s'adapte à tous les écrans
- Gestion des erreurs: l'API retourne des messages clairs en cas d'erreur
- Tests automatisés: une suite de tests pytest vérifie que tout marche

## Cas d'usage

Un étudiant crée un compte et rentre ses cours du semestre. Pour chaque cours, il upload les PDFs des slides, des exercices corrigés, et des anciennes partiels. Tout est en un seul endroit, classé par type et facile à retrouver. Il peut ajouter des liens vers des ressources externes aussi. Quand il se déconnecte, sa session est supprimée de la base.
