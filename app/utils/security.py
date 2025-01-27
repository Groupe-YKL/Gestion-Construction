from passlib.context import CryptContext

# Initialisation du contexte pour le hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction pour hasher un mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Fonction pour vérifier si le mot de passe correspond
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
