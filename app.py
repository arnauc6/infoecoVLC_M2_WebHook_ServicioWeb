#!/usr/bin/python
# -*- coding: utf-8 -*-

##------------------------------------------------------------------------------
## Importar
##------------------------------------------------------------------------------
import os
import json

# Flask es un framework minimalista que te permite crear aplicaciones web rápidamente
from flask import Flask
from flask import request
from flask import make_response

from carga_respuestas import * # Importa .py con las funciones de respuestas

##------------------------------------------------------------------------------
## Funciones
##------------------------------------------------------------------------------
# def makeWebhookResult(post):
#     print post
#     pass

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

app = Flask(__name__)


##------------------------------------------------------------------------------
## Rutas
##------------------------------------------------------------------------------

# RUTA POR DEFECTO /
@app.route("/") # Con esto podemos comprobar que el servidor está activo
def hello():
    return "Hello from Python!"


# RUTA DONDE APUNTA API.IA /////////////////////////////////////////////////////
@app.route('/webhook', methods=['POST'])    # Indicamos la ruta y los métodos
def webhook():                              # que aceptamos

    # Lee el json de la entrada y lo convierte en dic
    post = request.get_json(silent=True, force=True)

    respuesta = ""

    # Extraemos el nombre de la acción que será el nombre que pongamos a la función que le dará respuesta
    f = post["result"]["action"]

    # Para dar respuesta solo nos importa la información contenida en 'result'
    q = post["result"]

    # Buscamos el texto de la respuesta en la función que corresponda
    if f != "c.Desconocido":
        respuesta = funcionGestorRespuesta[f](q,db)
    else:
        respuesta = funcionGestorRespuesta[f](post,dbU)

    res = {
        "speech": respuesta,
        "displayText": respuesta,
##        "data": {},
##        "contextOut": [],
        "source": "arnau"#,
##        "followupEvent": {
##            "name": "WELCOME",
##            "data": {"nombreParam":"ValorParam"} #Llamada: #WELCOME.nombreParam en Action Value
##            }
        }

    # Convierte el diccionario en string para ser enviado como respuesta
    res = json.dumps(res, indent=4, ensure_ascii=False).encode('utf8')

    # Crea un objeto de respuesta para poder añadir valores en la cabecera
    r = make_response(res)

    # Añadimos la cabecera
    r.headers['Content-Type'] = 'application/json'

    return r
    #/////////////////////////////////////////////////////////////////// webhook

##------------------------------------------------------------------------------
## Programa
##------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
