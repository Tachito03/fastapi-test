import email
from telnetlib import STATUS
from unittest import result
from urllib import response
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Request, Depends, Response, status
from sqlalchemy import null
from config.db import conn
from models.mails import clientes, template
from schemas.mails import Clientes, Template, SendMail
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse

#seguridad
from fastapi.security import HTTPBearer
token_auth_scheme = HTTPBearer()
from utils import VerifyToken

#librerias para mails
import smtplib
from smtplib import SMTPResponseException
from email.message import EmailMessage
import re

mails = APIRouter()
# response_model=Clientes,
@mails.get('/getQuota/{centro}', tags=["For mails"])
async def getQuota(centro:int, response: Response, token: str = Depends(token_auth_scheme)):
    cadena = "SELECT descripcion, qoute FROM clientes WHERE id=%s"
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    else:
        result = conn.execute(cadena, centro).first()

    if result is None:
        return JSONResponse(status_code=401, content={"message": "El recurso solicitado no existe.", "status":"404"})
    else:
        return result

@mails.get('/getTemplates/{centro}', tags=["For mails"])
async def getTemplates(centro:int, token: str = Depends(token_auth_scheme)):
    sql = "SELECT id, nombre, descripcion, fecha_creado FROM templates WHERE idtemplate=%s"
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    else:
        result = conn.execute(sql, centro).first()
    
    if result is None: 
        return JSONResponse(status_code=401, content={"message": "El recurso solicitado no existe.", "status":"404"})
    else:
        return result

@mails.get('/getSent/{centro}', tags=["For mails"])
async def getSent(centro:int, token: str = Depends(token_auth_scheme)):
    sql_sent = "SELECT descripcion, qoute, enviados FROM clientes WHERE id=%s"

    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    else:
        result = conn.execute(sql_sent, centro).first()

    if result is None:
        return JSONResponse(status_code=401, content={"message": "El recurso solicitado no existe.", "status":"404"})
    else:
        disponibles = result.qoute - result.enviados
        return JSONResponse(status_code=200, content={"Centro": result.descripcion , "Enviados": str(result.enviados), "Qouta disponible": str(disponibles)})

@mails.get('/showTemplate/{idtemplate}', tags=["For mails"])
async def getSent(idtemplate:int, request:Request, token: str = Depends(token_auth_scheme)):
    get_template = "SELECT nombre, descripcion, template FROM templates WHERE idtemplate=%s"
    result = VerifyToken(token.credentials).verify()
    
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    else:
        result = conn.execute(get_template, idtemplate).first()

    if result is None:
        return JSONResponse(status_code=401, content={"message": "El recurso solicitado no existe.", "status":"404"})
    else:
        html = result.template

        f = open('template-test.html', 'w')
        html = result.template
        f.write(html)
        f.close()
        method_document = 'showTemplate'
        path_url = request.base_url
        full_path = str(path_url) + method_document

        return JSONResponse(status_code=200, content={"Nombre": result.nombre , "Descripcion": result.descripcion, "Link plantilla": full_path})

@mails.post('/sendEmail', tags=["For mails"])
async def sendEmail(datamails: SendMail, token: str = Depends(token_auth_scheme)):

    sql_template = "SELECT idtemplate, template FROM templates WHERE idtemplate = %s"
    query_template = conn.execute(sql_template, datamails.idtemplate).first()

    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    else:
        msg = EmailMessage()
        msg['Subject'] = datamails.subject
        msg['From'] = 'arellanos.baaeus@gmail.com'
        msg['To'] = datamails.to
        emailvalidate = datamails.to
        html = query_template.template
        msg.add_alternative(html, subtype="html")
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", emailvalidate):
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                    smtp.login('arellanos.baaeus@gmail.com','vkkvjuzevdnnfwcw')

                    sql_enviados = "SELECT qoute, enviados FROM clientes WHERE id=%s"
                    qouta_centro_enviados = conn.execute(sql_enviados, datamails.centro).first()
                    if qouta_centro_enviados.enviados < qouta_centro_enviados.qoute:
                        smtp.send_message(msg)

                        enviados_centro = qouta_centro_enviados.enviados + 1
                        update_qouta = "UPDATE clientes SET enviados = %s WHERE id=%s"
                        num_qoute = conn.execute(update_qouta,enviados_centro, datamails.centro)
                        return JSONResponse(status_code=200, content={"message": "se ha enviado el email", "status":"200"})
                    else:
                        return JSONResponse(status_code=401, content={"message": "se ha excedido el limite de envios", "status":"401"})

            except SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error

                return JSONResponse(status_code=error_code, content={"message": error_message})
        else: 
            return JSONResponse(status_code=401, content={"message": "El email es inválido "})




@mails.get('/showTemplate', response_class=HTMLResponse, tags=["For mails"], include_in_schema=False)
async def getDocument():
    f = open('template-test.html', 'r')
    html = f.read()
    return HTMLResponse(content=html, status_code=200)
    f.close()
    