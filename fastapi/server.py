import shutil

import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form
import pandas as pd
from typing import  List

from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
class UFOData(BaseModel):
    Date_time: str
    Year: int
    Month: int

class Contrato(BaseModel):
    #titulo:str
    #autor:str
    #pais:str
    #genero:str
    fecha:str
    centro_seccion:str
    nreg:str
    nexp:str
    objeto:str
    tipo:str
    procedimiento:str
    numlicit:str
    numinvitcurs:str
    proc_adjud:str
    presupuesto_con_iva:str
    valor_estimado:str
    importe_adj_con_iva:str
    adjuducatario:str
    fecha_formalizacion:str
    I_G:str


class ListadoUFOS(BaseModel):
    ufos = List[UFOData]

class ListadoContratos(BaseModel):
    contratos = List[Contrato]

app = FastAPI(
    title="Servidor de datos",
    description="""Servimos datos de contratos, pero podríamos hacer muchas otras cosas, la la la.""",
    version="0.1.0",
)

@app.get("/ufo_sightings/")
def get_all_ufo_sightings():
    data = pd.read_csv('./ufo-sightings-transformedCORTO.csv', sep=';')
    data.fillna(0)
    todosmisdatosdict = data.to_dict(orient='records')
    listado = ListadoUFOS()
    listado.ufos = todosmisdatosdict
    return listado

@app.get("/retrieve_data/")
#def insercion_endpoint (titulo:str = Form(...), autor:str=Form(...), pais:str=Form(...),genero:str=File(...),  archivo: UploadFile=File(...)):
def retrieve_data ():
    todosmisdatos = pd.read_csv('./ufo-sightings-transformed.csv.csv',sep=';')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = ListadoContratos()
    listado.contratos = todosmisdatosdict
    return listado
