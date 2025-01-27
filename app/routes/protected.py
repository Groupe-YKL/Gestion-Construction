from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
import jwt
from tortoise import Tortoise
from app.models import User
from typing import Optional
from fastapi import APIRouter
from decouple import config

SECRET_KEY = config("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()
   
# Fonction pour obtenir l'utilisateur à partir du token JWT
def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):

    if token is None:  # Handle missing token explicitly
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",  # Message d'erreur plus précis
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"Token reçu dans l'en-tête : {token}")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"Décodage du token avec la clé secrète...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"Payload: {payload}")
        username: str = payload.get("sub")
        if username is None:
            print("Erreur : le champ 'sub' est manquant dans le payload.")
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        print("Erreur : Le token a expiré.")
        raise credentials_exception
    except jwt.exceptions.PyJWTError as e:
        print(f"Erreur de validation du token: {e}")
        raise credentials_exception
    return username

# Route protégée
@router.get("/protected_route")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}, you have access!"}
