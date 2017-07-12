#!/usr/bin/python
# -*- coding: utf-8 -*-

##------------------------------------------------------------------------------
## Importar
##------------------------------------------------------------------------------
import os
import json

from flask import Flask         # Flask es un framework minimalista que te
from flask import request       # permite crear aplicaciones web rápidamente
from flask import make_response # tiene una licencia BSD

from gestor_respuesta import gestorRespuesta # Importa .py con las funciones de respuestas


##------------------------------------------------------------------------------
## Funciones
##------------------------------------------------------------------------------
def makeWebhookResult(post):
    respuesta = ""
    f = post["result"]["action"]  # Extraemos el nombre de la acción
                                            # que será el nombre que pongamos a
                                            # la función que le dará respuesta
    q = post["result"]  # Para dar respuesta solo nos importa la información
                            # contenida en result

    respuesta = gestorRespuesta(f,q)

    r = {
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
    
    return r ##--------------------------------------------- makeWebhookResult()


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


# RUTA DONDE APUNTA API.IA	
@app.route('/webhook', methods=['POST'])    # Indicamos la ruta y los métodos 
def webhook():                              # que aceptamos
    
    req = request.get_json(silent=True, force=True) # Lee el json de la entrada
                                                    # y lo convierte en dic
    
    res = makeWebhookResult(req) # Llamamos a la función que buscará la respuesta

    res = json.dumps(res, indent=4, ensure_ascii=False).encode('utf8') # Convierte el diccionario en string para ser enviado como respuesta

    r = make_response(res)  # Crea un objeto de respuesta para poder añadir
                            # valores en la cabecera
                            
    r.headers['Content-Type'] = 'application/json' # Añadimos la cabecera

    return r
	

##------------------------------------------------------------------------------
## Programa
##------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
