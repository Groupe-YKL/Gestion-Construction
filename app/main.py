from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.fastapi import register_tortoise
from decouple import config  # Pour lire les variables depuis .env
from app.utils.jwt import verify_access_token
from app.routes import protected
from app.routes import auth

# Instantiation l'application FastAPI
app = FastAPI()

# l'URL de la base de données depuis .env
DATABASE_URL = config("DATABASE_URL")

# Configuration de Tortoise ORM
register_tortoise(
    app,
    db_url=DATABASE_URL, 
    modules={"models": ["app.models"]}, 
    generate_schemas=True,  # Génère automatiquement les tables dans la base de données
    add_exception_handlers=True,  # Ajoute des handlers pour les erreurs liées à Tortoise
)


app.include_router(auth.router)
app.include_router(protected.router)
