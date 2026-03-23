from passlib.context import CryptContext

pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password):
    return pwd.hash(password)

def check_password(plain, hashed):
    return pwd.verify(plain, hashed)