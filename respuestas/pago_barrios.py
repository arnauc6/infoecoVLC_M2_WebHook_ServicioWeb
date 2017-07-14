#!/usr/bin/python
# -*- coding: utf-8 -*-

##//////////////////////////////////////////////////////////////////////////////
## Importar
##//////////////////////////////////////////////////////////////////////////////

# Importar locales solo si el valor resultado es numérico
import locale #Librería que nos permite adaptar el formato numérico al Español
import time # Para añadir fecha y hora a los errores (except)

try:
    locale.setlocale(locale.LC_ALL,'es_ES.utf8')
except:
    locale.setlocale(locale.LC_ALL,'')

from bson.son import SON

from unir_texto import unirTexto # Llama a la función que une el texto


##//////////////////////////////////////////////////////////////////////////////
## Texto respuesta
##//////////////////////////////////////////////////////////////////////////////

# Texto ejemplo:
#   - El barrio de Benimaclet pagó 6,428,288.48 € de impuestos en el año 2016.
#   - El barri de Benimaclet va pagar 6,428,288.48 € d'impostos l'any 2016.

# Texto en la lista:
textoRespuesta = {
        "Cast": [u"El barrio de ", u" pagó ", u"€ de ", u" en el año ", u"."],
        "Val": [u"El barri de ", u" va pagar ", u" € d'", u" l'any " , u"."]
        }

textoFaltaBarrio = {
        "Cast": u"""Por favor, indícanos el nombre del barrio del que quieras obtener la información.
(El nombre debe estar bien escrito)""",
        "Val": u"""Per favor, indica'ns el nom del barri del que vulgues obtenir la informació.
(El nom ha d'estar ben escrit)"""
        }

textoAnyoSinDatos = {
        "Cast": [u"No disponemos de los datos del año ", u"."],
        "Val": [u"No disposem de les dades de l'any ", u"."]
        }


##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////
def pagoBarrios(result,db):
    print time.strftime("%c"), "- Recibimos petición de pagoBarrios"
    dbBarrios = db.barrios # Accedemos a la colección donde almacenamos todos los datos

    texto = u"LLegó"
    # Sacamos los parámetros  de result ----------------------------------------
    try:
        impuesto = result["parameters"]["impuestos"]
        barrio = result["parameters"]["barrios"]
        anyo = result["parameters"]["anyo"]
        idioma = result["parameters"]["idioma"]
    except Exception as e:
        print "     ", time.strftime("%c"), "- Error al obtener los parametros: ", type(e), e
    #---------------------------------------------------------------- parámetros

    # Si falta barrio se pide
    if barrio == u"":
        return textoFaltaBarrio[idioma]

    try:
        valor, anyo = valorPagoBarrios(impuesto,barrio,anyo,dbBarrios)

    except Exception as e:
        print "     ", time.strftime("%c"), "- Error función valor: ", type(e), e

    try:
        if valor == u"-1,00" or valor == u"-1.00":
            texto = unirTexto(textoAnyoSinDatos[idioma], anyo)
        else:
            texto = unirTexto(textoRespuesta[idioma], barrio, valor, impuesto, anyo)

    except Exception as e:
        print "     ", time.strftime("%c"), "- Error función unirTexto: ", type(e), e

    return texto


##//////////////////////////////////////////////////////////////////////////////
## Funciones
##//////////////////////////////////////////////////////////////////////////////

def valorPagoBarrios(impuesto,barrio,anyo,dbBarrios):

    if anyo == u"null": #Sin datos de año cogemos el último año
        anyo = { "$exists": "true" }
    else:
        anyo = int(anyo)

    pipeline = [
        {"$match": {"barrio": barrio, "anio": anyo}},
        {"$sort": SON([("anio", -1)])},
        {"$limit": 1},
        {"$project": {
            "_id": "$barrio",
            "valor": {"$sum": []},
            "anyo": "$anio"
            }
         }
        ]

    try:
        suma = sumaImpuesto(impuesto)
    except Exception as e:
        print "          ", time.strftime("%c"), "- Error en suma: ", type(e), e


    try:
        pipeline[3]["$project"]["valor"]["$sum"].extend(suma)
    except Exception as e:
        print "          ", time.strftime("%c"), "- Error al añadir suma a pipeline: ", type(e), e

    # Consulta DB
    try:
        respuesta = list(dbBarrios.aggregate(pipeline))
    except Exception as e:
        print "          ", time.strftime("%c"), "- Error conexión PagoBarrios: ", type(e), e

    if respuesta == []:
        valor = -1
    else:
        valor = respuesta[0][u"valor"]
        anyo = respuesta[0][u"anyo"]

    # Cambia el formato para que aparezcan los . de millar y solo 2 decimales
    valor = locale.format("%.2f", valor, grouping=True)

    return valor, anyo


def sumaImpuesto(impuesto):
    suma = []
    if impuesto == "impuestos":
        suma = [
            "$impuestos.IVTNU Personas Físicas",
            "$impuestos.IVTNU Personas Jurídicas",
            "$impuestos.IAE",
            "$impuestos.IVTM Personas Físicas",
            "$impuestos.IVTM Personas Jurídicas",
            "$impuestos.IBI Personas Físicas",
            "$impuestos.IBI Personas Jurídicas"
            ]

    elif impuesto=="IVTNU":
        suma = [
            "$impuestos.IVTNU Personas Físicas",
            "$impuestos.IVTNU Personas Jurídicas"
            ]

    elif impuesto=="IAE":
        suma = [
            "$impuestos.IAE"
            ]

    elif impuesto=="IVTM":
        suma = [
            "$impuestos.IVTM Personas Físicas",
            "$impuestos.IVTM Personas Jurídicas"
            ]

    elif impuesto=="IBI":
        suma = [
            "$impuestos.IBI Personas Físicas",
            "$impuestos.IBI Personas Jurídicas"
            ]

    return suma
