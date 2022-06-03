from typing import Optional
from pydantic import BaseModel

class Clientes(BaseModel):
    descripcion: str
    qoute: str

class Template(BaseModel):
    id: int
    nombre: str
    descripcion: str
    fecha_creado: str

class SendMail(BaseModel):
    centro: int
    idtemplate: int
    subject: str
    to: str
