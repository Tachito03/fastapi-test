from xmlrpc.client import DateTime
from pymysql import Timestamp
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Text
from config.db import meta, engine

clientes = Table('clientes', meta,
    Column('id', Integer, primary_key=True),
    Column('descripcion', String(40)),
    Column('qoute', Integer()),
    Column('enviados', Integer()),
    Column('fecha_creado', String(20)))

template = Table('templates', meta,
    Column('id', Integer, primary_key= True),
    Column('idtemplate', Integer()),
    Column('nombre', String(40)),
    Column('descripcion', String(40)),
    Column('template', Text()),
    Column('fecha_creado', String(20)))



meta.create_all(engine)