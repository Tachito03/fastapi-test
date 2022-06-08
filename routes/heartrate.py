from fastapi import APIRouter, FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
from schemas.heartrate import ReserveHR, HostaticTest

heart = APIRouter()

@heart.get('/maxHR/{edad}', tags=["Heart Rate"])
def maxHR(edad:int):
    if edad < 110:
        res_hr = 200 - edad
        return JSONResponse(status_code=200, content={"message": "Tu frecuencia cardíaca máxima estimada es: " + str(res_hr) + ' bpm' , "status":"200"})
    else:
         return JSONResponse(status_code=200, content={"message": "Vaya, la edad ingresada no es válida" , "status":"401"})

@heart.post('/reserveHR', response_model=ReserveHR, tags=["Heart Rate"])
def reserveHR(datareserve: ReserveHR):
    if datareserve.edad == 0 or datareserve.reserveHR == 0: 
        return JSONResponse(status_code=501, content={"message": "Datos erróneos, no se puede tener valores con 0" , "status":"501"})
    else:
        if datareserve.edad < 110:
            res_maxhr = 200 - datareserve.edad
            FCR = res_maxhr - datareserve.reserveHR
            return JSONResponse(status_code=200, content={"message": "Su frecuencia cardíaca de reserva es: " + str(FCR) + " pulsaciones/min" , "status":"200"})
        else:
            return JSONResponse(status_code=401, content={"message": "Vaya, la edad ingresada no es válida" , "status":"401"})

@heart.post('/orthostaticTest', response_model=HostaticTest, tags=["Heart Rate"])
def orthostaticTest(dataTest:HostaticTest):
    if dataTest.hr_one == 0 or dataTest.hr_two == 0: 
        return JSONResponse(status_code=501, content={"message": "Datos erróneos, no se puede tener valores con 0" , "status":"501"})
    else:
        res_test = dataTest.hr_one - dataTest.hr_two
        or_thostatic = str(res_test)
        return JSONResponse(status_code=200, content={"message": "Tu nivel de Ortostática en el corazón es: " + or_thostatic.replace('-', '') + " bpm" , "status":"200"})
