from jose import jwt, JWTError
import time

SECRET = "supersecretkey123"
ALG = "HS256"

def make_token(username):
    return jwt.encode({
        "username": username,
        "exp": time.time() + 3600
    }, SECRET, algorithm=ALG)

def decode_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALG])["username"]
    except JWTError:
        return None
