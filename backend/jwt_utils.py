import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET_KEY", "changeme")
ALGO = "HS256"

def make_token(username):
    expire = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode({"sub": username, "exp": expire}, SECRET, algorithm=ALGO)

def read_token(token):
    return jwt.decode(token, SECRET, algorithms=[ALGO])