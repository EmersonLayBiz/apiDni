from pydantic import  BaseModel

class DniSchema(BaseModel):
    username: str
    email: str