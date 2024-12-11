
from fastapi import FastAPI
from routers import products, users, user, jwt_auth, basic_auth, users_db
from fastapi.staticfiles import StaticFiles
app = FastAPI()

# router
app.include_router(products.router)
app.include_router(users.router)
app.include_router(user.router)
app.include_router(jwt_auth.router)
app.include_router(basic_auth.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
####

@app.get("/")
async def root():
    return "Hola FastAPI"

@app.get("/url")
async def url():
    return {"url":"https://mouredev.com/python"}


# Lanzar servidor: uvicorn main:app --reload
# Crear documentacion 
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/docs
# Thunder Client Extencion de vsc para ejecucion de cliente 
# postman para ejecucion de cliente 