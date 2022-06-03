import email
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Request
from sqlalchemy import null
from config.db import conn
from models.mails import clientes, template
from schemas.mails import Clientes, Template, SendMail
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse

#librerias para mails
import smtplib
from smtplib import SMTPResponseException
from email.message import EmailMessage
import re

mails = APIRouter()

@mails.get('/getQuota/{centro}', response_model=Clientes, tags=["For mails"])
async def getQuota(centro:int):
    cadena = "SELECT descripcion, qoute FROM clientes WHERE id=%s"
    resultado = conn.execute(cadena, centro).first()

    if resultado is None:
        return JSONResponse(status_code=401, content={"message": "Sin resultados", "status":"401"})
    else:
        return resultado


@mails.get('/getTemplates/{centro}', response_model=Template, tags=["For mails"])
async def getTemplates(centro:int):
    sql = "SELECT id, nombre, descripcion, fecha_creado FROM templates WHERE idtemplate=%s"
    res = conn.execute(sql, centro).first()

    if res is None:
        return JSONResponse(status_code=401, content={"message": "Sin resultados", "status":"401"})
    else:
        return res

@mails.get('/getSent/{centro}', tags=["For mails"])
async def getSent(centro:int):
    sql_sent = "SELECT descripcion, qoute, enviados FROM clientes WHERE id=%s"
    resultado = conn.execute(sql_sent, centro).first()

    if resultado is None:
        return JSONResponse(status_code=401, content={"message": "Sin resultados", "status":"401"})
    else:
        disponibles = resultado.qoute - resultado.enviados
        return JSONResponse(status_code=200, content={"Centro": resultado.descripcion , "Enviados": str(resultado.enviados), "Qouta disponible": str(disponibles)})

@mails.get('/showTemplate/{idtemplate}', tags=["For mails"])
async def getSent(idtemplate:int, request:Request):
    get_template = "SELECT nombre, descripcion, template FROM templates WHERE idtemplate=%s"
    resultado = conn.execute(get_template, idtemplate).first()

    if resultado is None:
        return JSONResponse(status_code=401, content={"message": "Sin resultados", "status":"401"})
    else:
        html = resultado.template

        f = open('template-test.html', 'w')
        html = resultado.template
        f.write(html)
        f.close()
        method_document = 'showTemplate'
        path_url = request.base_url
        full_path = str(path_url) + method_document

        return JSONResponse(status_code=200, content={"Nombre": resultado.nombre , "Descripcion": resultado.descripcion, "Link plantilla": full_path})

@mails.post('/sendEmail', response_model=SendMail, tags=["For mails"])
async def sendEmail(datamails: SendMail):

    sql_template = "SELECT idtemplate, template FROM templates WHERE idtemplate = %s"
    query_template = conn.execute(sql_template, datamails.idtemplate).first()

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
    
    

