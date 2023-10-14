from fastapi import FastAPI, HTTPException, Query, Request,Path
from schemas.dni_schema import DniSchema, DniUserSchema
from models.dni_model import DniModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.apis_net_pe import ApisNetPe


app = FastAPI()
APIS_TOKEN = "apis-token-5861.9xsntyl7U-O8FnrYwHpBqUJJ29i5rref"
# Configura la ruta para servir archivos estáticos (cambiar "static" al directorio real)
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates") 

conn = DniModel()


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/insert", response_class=HTMLResponse)
async def show_insert_page(request: Request):
    # Renderiza la página de inserción
    return templates.TemplateResponse("insert.html", {"request": request})

@app.get("/consult_dni", response_class=HTMLResponse)
async def show_consult_page(request: Request):
    # Renderiza la página de inserción
    return templates.TemplateResponse("consult_dni.html", {"request": request})

@app.get("/dnis/")
async def read_all():
    data = conn.read_all()
    return {"data": data}


@app.post("/users/")
def create_user(user: DniSchema):
    try:
        name = user.username
        email = user.email
        conn.create_user(name,email)
        return{
            "message": "User inserted succesfull"
        }
    except Exception as e:  
        # Manejar cualquier excepción que pueda ocurrir durante la inserción
        raise HTTPException(status_code=500, detail=str(e))
    




@app.get("/dni/{dni}")
def get_one_dni(dni: int = Path(..., description="Número de DNI")):
    dictionary = {}
    data = conn.get_dni_one(dni)
    print(data)
    if data is not None:
        dictionary["dni"] = data[0]
        dictionary["nombre"] = data[1]
        dictionary["apellido_pat"] = data[2]
        dictionary["apellido_mat"] = data[3]
        return dictionary 

@app.post("/dni/")
def inser_dni(dni: DniUserSchema):
    try:
        dnis = dni.dni
        name = dni.name
        ape_pat = dni.ape_pat
        ape_mat = dni.ape_mat
        conn.create_dni(dnis, name, ape_pat, ape_mat)
        return{
            "message": "User Dni inserted succesfull"
        }
    except Exception as e:  
        # Manejar cualquier excepción que pueda ocurrir durante la inserción
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/")
def get_one(userId: int = Query(..., description="Insert Userd ID")):
    dictionary = {}
    data = conn.get_user_by_id(userId)
    if data is not None:
        dictionary["id"] = data[0]
        dictionary["username"] = data[1]
        dictionary["email"] = data[2]
        return data





# Actualizar un usuario por ID
@app.put("/users/{user_id}", response_model=DniSchema)
def update_user(user_id: int, updated_user: DniSchema):
    try:
        existing_user = conn.get_user_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        new_username = updated_user.username
        new_email = updated_user.email
        conn.update_user(user_id, new_username, new_email)
        
        return {
            "username": new_username,
            "email": new_email
        }
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la actualización
        raise HTTPException(status_code=500, detail=str(e))

# Eliminar un usuario por ID
@app.delete("/users/{user_id}", response_model=DniSchema)
def delete_user(user_id: int):
    try:
        existing_user = conn.get_user_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        deleted_user = conn.delete_user(user_id)
        
        return {
            "username": deleted_user[1],  # Nombre del usuario eliminado
            "email": deleted_user[2]  # Correo del usuario eliminado
        }
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la eliminación
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un usuario por ID
@app.get("/usersdc/{user_id}", response_model=DniSchema)
def read_user(user_id: int):
    user = conn.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": user[0],
        "username": user[1],
        "email": user[2]
    }


@app.get("/consultar_dni/{dni}")
async def consultar_dni(dni: str):
    try:
        api_consultas = ApisNetPe(APIS_TOKEN)
        data = api_consultas.get_person(dni)

        if data is None:
            raise HTTPException(status_code=404, detail="DNI no encontrado")

        # Crear un diccionario personalizado con los campos deseados
        response_data = {
            "dni": dni,
            "name": data['nombres'],
            "apellido_paterno": data['apellidoPaterno'],
            "apellido_materno":  data['apellidoMaterno']
        }

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)