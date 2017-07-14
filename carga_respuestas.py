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
    from variables import URL_de_MongoDB
    uri = URL_de_MongoDB # Variable de entorno
except:
    print "Error al cargar URL de MongoDB"

try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database() # Accedemos a la BD donde tenemos las colecciones
except:
    print "Error al conectarse a la BD de MongoDB"
