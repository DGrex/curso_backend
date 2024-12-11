from fastapi import APIRouter, HTTPException
from routers import users



users_list = users.users_list
User = users.User
router = APIRouter(prefix="/user",tags=["usuario"],
                   responses= {404:{"message":" Usuario no encontrado"}})

# path
@router.get("/{id}")
async def user(id : int):
    users = filter(lambda item: item.id == id,  users_list)
    try:
        return list(users)[0] # Accedo a la posicion 0 para que no devuelva un listado
    except:
        return {"error":"No se ha encontrado el usuario"}
   
    """
    for user in users_list:
        if user.id == id:
          return user 
    # Podria hacerlo tambien con un for     
    """     
    """
    item es simplemente el nombre de la variable que se asigna temporalmente 
    a cada objeto User en la lista users_list durante la iteración del filter. 
    como lo aria un for 
    """

# Query

@router.get("/userquery/")
async def user(id : int):
    return search_user(id)
    
# http://127.0.0.1:8000/userquery/?id=1 == llamar
# Podriamos tambien crar un funcion aparte y retornarla

# Post
@router.post("/", response_model= User, status_code= 201)
async def user(user : User):
    return agregar_usuario(user)

#http://127.0.0.1:8000/user/
#{"id":4, "name":"Denis", "surname":"Goyes", "email":"goyes@gmail.com", "ege":21}

# put

@router.put("/")
async def user(user:User):
    return actualizar_usuario(user)

#http://127.0.0.1:8000/user/
#{"id":4, "name":"Denis", "surname":"Goyes", "email":"goyes@gmail.com", "ege":22}

#Delete

@router.delete("/{id}")
async def user(id : int):
    return eliminar_usuario(id)



### Funciones ###
def eliminar_usuario(id : int):
    found = False

    for index, values_list in enumerate(users_list):
        if values_list.id == id:
            del users_list[index]
            found = True 
            return f"Usuario {id} eliminado:"            
        #else:
            #return {"error":"No se ha eliminado el usuario"}
    if not found:
        return {"error":"No se ha eliminado el usuario"}




def actualizar_usuario(user:User):
    found = False

    for index, values_list in enumerate(users_list):
        if values_list.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

def agregar_usuario(user:User):
    #if isinstance(search_user(user.id), User):
    if type(search_user(user.id)) == User:
        #return {"error":"El usuario ya existe"}
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

    
def search_user(id : int):
    users = filter(lambda item: item.id == id,  users_list)
    try:
        return list(users)[0] # Accedo a la posicion 0 para que no devuelva un listado
    except:
        return {"error":"No se ha encontrado el usuario"}