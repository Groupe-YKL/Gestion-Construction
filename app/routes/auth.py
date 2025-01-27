from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, verify_access_token
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from datetime import timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Route pour l'inscription
@router.post("/signup")
async def signup(user: UserCreate):
    # Vérifie si l'utilisateur existe déjà dans la base de données
    existing_user = await User.filter(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hachage du mot de passe
    hashed_password = pwd_context.hash(user.password)

    # Sauvegarde l'utilisateur dans la base de données
    new_user = await User.create(username=user.username, email=user.email, hashed_password=hashed_password)
    
    return {"message": "User created successfully"}

# Route pour la connexion et la création d'un token JWT
@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.filter(username=form_data.username).first() # Fetch user from DB
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
