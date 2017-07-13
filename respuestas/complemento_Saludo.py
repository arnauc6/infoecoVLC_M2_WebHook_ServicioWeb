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
                [u"¡Buenos días ", u"!"], # ¡Buenos días $nombre!
                [u"Buenos días ", u", ¿Qué tal?"] # Buenos días $nombre, ¿Qué tal?
        ],
        "Val": [
                [u"Bon dia ", u"!"], # Bon dia $nombre!
                [u"Bon dia ", u", què tal?"] # Bon dia $nombre, què tal?
        ]
        }

##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////

def complementoSaludo(result,dbValencia):
    print time.strftime("%c"), u"- Recibimos petición de", result["action"]

    # Sacamos los parámetros  de result ----------------------------------------
    try:
        nombre = result["parameters"]["nombre"]
        idioma = result["parameters"]["idioma"]
    except Exception as e:
        print "     ", time.strftime("%c"), "- Error al obtener los parametros: ", type(e), e
    #---------------------------------------------------------------- parámetros

    textoRespuestaI = textoRespuesta[idioma]
    l = len(textoRespuestaI)
    texto = ""

    try:
        texto = unirTexto(textoRespuestaI[random.randrange(l)], nombre)

    except Exception as e:
        print "     ", time.strftime("%c"), "- Error función unirTexto: ", type(e), e

    return texto
