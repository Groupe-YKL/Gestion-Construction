# Authentification avec FastAPI

## Ce document détaille la mise en place de l'authentification dans le projet GestionConstruction, en utilisant FastAPI, JWT pour la gestion des tokens, et PostgreSQL pour la gestion des utilisateurs.

### Description du Module
    Cette partie du projet implémente un système d'authentification basé sur JSON Web Tokens (JWT). Elle permet :
- L'enregistrement des utilisateurs dans une base de données PostgreSQL.
- La génération et la vérification de tokens JWT pour sécuriser les routes.
- La protection des routes nécessitant une authentification.

### Installation
1. Clonez le dépôt et placez-vous sur la branche BackEnd-Auth :
    ```bash
        git clone <URL_DU_DEPOT>
        git checkout BackEnd-Auth
    ```
2. Configurez et lancez les conteneurs Docker :
    ```bash
        docker-compose up --build
    ```
3. Accédez à l'application sur http://localhost:8000.

### Configuration
    Configuration : Les variables sensibles comme la clé secrète JWT et les informations de connexion à la base de données sont définies dans un fichier .env. (Vous devez creer le fichier .env à la racine de votre dossier et y inserer les variables suivantes :
    - DATABASE_USER=
    - DATABASE_PASSWORD=
    - DATABASE_HOST=postgres-db
    - DATABASE_PORT=5432
    - DATABASE_NAME=gesconstruction
    - DATABASE_URL=
    - SECRET_KEY=
    )

### Endpoints principaux
#### - Enregistrement (Register)
    Permet de créer un nouvel utilisateur dans la base de données PostgreSQL.
    Méthode : POST
    URL : /register
        Corps de la requête :
            {
            "username": "string",
            "password": "string",
            "email":"test@test.com
            }
        Réponse (succès) :
            {
            "message": "User created successfully"
            }

#### - Connexion (Login)
    Permet de générer un token JWT pour un utilisateur existant.
    Méthode : POST
    URL : /login    
    Corps de la requête :
        {
        "username": "string",
        "password": "string"
        }
    Réponse (succès) :
        {
        "access_token": "string",
        "token_type": "bearer"
        }

#### - Route protégée
    Permet d'accéder à une ressource sécurisée après authentification via un token JWT.
    Méthode : GET
    URL : /protected_route
    En-tête :
        Authorization: Bearer <token>
    Réponse (succès) :
        {
        "message": "Hello, <username>, you have access!"
        }


### Exécution du projet
    Pour exécuter le projet en local :
    Lancez les conteneurs Docker :
    docker-compose up
    Utilisez un outil comme Postman ou curl pour tester les endpoints.

### Tests
Testez l'enregistrement d'un utilisateur via /register.
Testez la connexion et la génération du token via /login.
Accédez à la route protégée /protected_route avec un token valide.