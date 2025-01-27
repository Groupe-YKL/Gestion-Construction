from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Raise an exception if the secret key is not set. This is CRUCIAL for security.
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set.")

# Convert the secret key to bytes if it's a string, this handles both cases
if isinstance(SECRET_KEY, str):
    SECRET_KEY = SECRET_KEY.encode('utf-8')

# Fonction pour créer un token JWT
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    print(f"Token à encoder : {to_encode}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token généré : {encoded_jwt}")
    return encoded_jwt

# Fonction pour vérifier et décoder un token JWT
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload.get("exp")
        if exp_timestamp and datetime.utcfromtimestamp(exp_timestamp) < datetime.utcnow():
            return None  # Token is expired
        return payload
    except JWTError:
        return None
