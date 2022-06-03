from fastapi import FastAPI, Depends
from routes.mailrelay import mails
from routes.heartrate import heart



app = FastAPI(title='endPoints ', 
              description='Primera versión de envio de mails, detalle de centros, calcúlo de frecuencia cardíaca ', 
              version='1.0.1', openapi_tags=[{
                  'name': 'fastAPI',
                  'description': 'endPoint Test'
              }])

app.include_router(mails)
app.include_router(heart)
