from fastapi import APIRouter , HTTPException
from pydantic import BaseModel # Esto para poder crear la clase sin constructores

router = APIRouter(prefix="/users", tags=["Usuarios"],
                   responses= {404: {"message":"No encontrado"}})

class User(BaseModel):
   id: int
   name: str
   surname: str
   email: str
   ege: int

users_list = [
    User(id = 1 ,name = "Denis", surname = "Goyes", email = "goyes@gmail.com", ege = 21),
    User(id = 2 , name = "Denis", surname = "Goyes", email = "goyes@gmail.com", ege = 22),
    User(id = 3 , name = "Denis", surname = "Goyes", email = "goyes@gmail.com", ege = 23)
]


@router.get("/usersjson")
async def usersjson():
    return [{"name":"Denis", "surname":"Goyes", "email":"goyes@gmail.com", "ege":21},
            {"name":"Denis", "surname":"Goyes", "email":"goyes@gmail.com", "ege":21},
            {"name":"Denis", "surname":"Goyes", "email":"goyes@gmail.com", "ege":21}]


@router.get("/")
async def users():
    #return users(name = "Denis", surname = "Goyes", email = "goyes@gmail.com", ege = "21")
    return users_list

