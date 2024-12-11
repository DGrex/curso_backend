# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"

from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt ,JWTError
from passlib.context import CryptContext
from datetime import datetime , timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

# openssl rand -hex 32
SECRET = "0a8849a72ddf57722c20afdba5c29135a6608134ca6d141b98bcf362c3e00664"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])
class User(BaseModel):
    username: str
    full_name : str
    email : str
    disable : bool

class UserDB(User):
    password: str
    
users_db = {
    "DGrex": {
        "username":"DGrex",
        "full_name":"Denis Goyes",
        "email":"goyesdenis14@gmail.com",
        "disable": False,
        "password":"$2a$12$6f9l/x51n99hSenX.Zpu3OOEDpESmxLIv2zxQWfmn1w2DmifD7Zve"
    },
        "DGrex2": {
        "username":"DGrex2",
        "full_name":"Denis Goyes2",
        "email":"goyesdenis142@gmail.com",
        "disable": True,
        "password":"$2a$12$Zh1VpQKiDBFnUhOMRT4Nfe6gQ4RdLyZFyEqzikNZthIzKRTB1/4Re"
    }
}
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    exception= HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail= "Credenciales de autenticacion invalidas",
                            headers= {"WWW-Authenticate": "Bearer"})

    
    try:
        username = jwt.decode(token, SECRET, algorithms= [ALGORITHM]).get("sub")
        if username is None :
            raise exception

    except JWTError:
        raise exception

    return search_user(username)

    
        
async def current_user(user :User = Depends(auth_user)):
        
    if user.disable:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= "Usuario inactivo",
                            )
  
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code= 400, detail= "El usuario no es el correcto")
    
    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code= 400, detail= "La contraceña no es la correcta")


    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=(ACCESS_TOKEN_DURATION)),
                      }
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm= ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user : User = Depends(current_user)):
    return user 