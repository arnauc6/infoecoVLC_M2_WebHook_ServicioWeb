#!/usr/bin/python
# -*- coding: utf-8 -*-

##------------------------------------------------------------------------------
## Imports (Importamos todos los documentos que responden a cada pregunta)
##------------------------------------------------------------------------------

from respuestas.pago_barrios import *
from respuestas.complemento_Saludo import *
from respuestas.complemento_Desconocido import *


##------------------------------------------------------------------------------
## Diccionario para hacer el Case en Python
##------------------------------------------------------------------------------

# Cada nueva respuesta añadir un key: <nombre_función>
funcionGestorRespuesta = {
    "r.pagoBarrios": pagoBarrios,
    "c.Saludo": complementoSaludo,
    "c.Desconocido": complementoDesconocido
    } # Tiene que estar al final de las funciones que pretendemos llamar


##------------------------------------------------------------------------------
## Conexión MongoDB
##------------------------------------------------------------------------------
import pymongo
try:
    from variables import URL_de_MongoDB, URL_de_MongoDB_U
    uri = URL_de_MongoDB # Variable de entorno
    uri_u = URL_de_MongoDB_U
except Exception as e:
    print "     ", time.strftime("%c"), "- Error al cargar URLs de MongoDB: ", type(e), e

try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database() # Accedemos a la BD donde tenemos las colecciones
except Exception as e:
    print "     ", time.strftime("%c"), "- Error al conectarse a la BD de MongoDB Respuestas: ", type(e), e

try:
    clientU = pymongo.MongoClient(uri_u)
    dbU = clientU.get_default_database() # Accedemos a la BD donde tenemos las colecciones
except Exception as e:
    print "     ", time.strftime("%c"), "- Error al conectarse a la BD de MongoDB Usuarios: ", type(e), e
