#!/usr/bin/python
# -*- coding: utf-8 -*-

##//////////////////////////////////////////////////////////////////////////////
## Importar
##//////////////////////////////////////////////////////////////////////////////
import time # Para añadir fecha y hora a los errores (except)
import random # Para que sea una entre varias respuestas

from unir_texto import unirTexto # Llama a la función que une el texto


##//////////////////////////////////////////////////////////////////////////////
## Texto respuesta
##//////////////////////////////////////////////////////////////////////////////
textoRespuesta = {
        "Cast": [ # Responderá una de las opciones
                u"¡Huy! Esa pregunta no la tenía contemplada.", # ¡Huy! Esa pregunta no la tenía contemplada.
                u"¡Qué pregunta más buena! La tendremos en cuenta para futuras actualizaciones." # ¡Qué pregunta más buena! La tendremos en cuenta para futuras actualizaciones.
        ],
        "Val": [
                u"Huy! Aquesta pregunta no la tenia contemplada.", # Bon dia $nombre!
                u"Quina pregunta més bona! La tindrem en compte per a futures actualitzacions." # Bon dia $nombre, què tal?
        ]
        }

##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////

def complementoDesconocido(post,dbUsuario):
    print time.strftime("%c"), "- Recibimos petición de", post["result"]["action"]
    idUsuario = u""
    # Sacamos los parámetros  de result ----------------------------------------
    try:
        idUsuario = post["sessionId"]
    except Exception as e:
        print "     ", time.strftime("%c"), "- Error al obtener los parametros: ", type(e), e


    usuario = buscarUsuario(idUsuario, dbUsuario)

    if 'idioma' in usuario and 'nombre' in usuario:
        nombre = usuario["nombre"]
        idioma = usuario["idioma"]
    else:
        nombre = "Ciudadano"
        idioma = "Cast"

    #---------------------------------------------------------------- parámetros



    textoRespuestaI = textoRespuesta[idioma]
    l = len(textoRespuestaI)
    texto = ""

    try:
        texto = textoRespuestaI[random.randrange(l)]
        # texto = unirTexto(textoRespuestaI[random.randrange(l)])

    except Exception as e:
        print "     ", time.strftime("%c"), "- Error función unirTexto: ", type(e), e

    return texto

# //////////////////////////////////////////////////////////////////////////////
# MongoDB
# //////////////////////////////////////////////////////////////////////////////

def buscarUsuario(idUsario, db):
    dbUsuarios = db.usuarios # Colección
    query = {
        '_id': int(idUsario)
        }

    cursor = ""

    try:
        cursor = dbUsuarios.find_one(query)
    except Exception as e:
        print "     ", time.strftime("%c"), "- Error buscarUsuario: ", type(e), e

    return cursor
