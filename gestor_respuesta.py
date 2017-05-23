#!/usr/bin/python
# -*- coding: utf-8 -*-

##------------------------------------------------------------------------------
## Importar
##------------------------------------------------------------------------------

import pymongo
import os

# Importamos todos los módulos que contienen las respuestas a las distintas preguntas
from respuestas.pago_barrios import *



##------------------------------------------------------------------------------
## Conexión MongoDB
##------------------------------------------------------------------------------

# Eliminar si añadimos la uri en el campo inferior -----------------------------
try: 
    from variables import *
except:
    pass
#------------------------------ Eliminar si añadimos la uri en el campo inferior

##uri = tu_URL_de_MongoDB # Sustituir tu_URL_de_MongoDB por la URL de tu servidor
try:
    uri = os.environ['URL_de_MongoDB'] # Variable de entorno para Heroku
except:
##    uri = 'mongodb://localhost:27017/collection'
    print "Error al cargar URL de MongoDB"

client = pymongo.MongoClient(uri)
db = client.get_default_database()
dbValencia = db.impuestosBarrios # Accedemos a la colección donde almacenamos todos los datos


##------------------------------------------------------------------------------
## Función que selecciona la función que obtiene la respuesta correcta
##------------------------------------------------------------------------------
def gestorRespuesta(f,q):
    respuesta = funcionGestorRespuesta[f](q,dbValencia)
    
    return respuesta


##------------------------------------------------------------------------------
## Diccionario para hacer el Case en Python
##------------------------------------------------------------------------------

# Cada nueva respuesta añadir un key: <nombre_función>
funcionGestorRespuesta = {
    "pagoBarrios": pagoBarrios
    } # Tiene que estar al final de las funciones que pretendemos llamar
