from pydantic import  BaseModel

class DniSchema(BaseModel):
    username: str
    email: str

class DniUserSchema(BaseModel):
    dni: int
    name: str
    ape_pat: str
    ape_mat: str