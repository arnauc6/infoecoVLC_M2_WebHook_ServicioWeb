#!/usr/bin/python
# -*- coding: utf-8 -*-

##//////////////////////////////////////////////////////////////////////////////
## Importar
##//////////////////////////////////////////////////////////////////////////////

# Importar locales solo si el valor resultado es numérico
import locale #Librería que nos permite adaptar el formato numérico al Español

locale.setlocale(locale.LC_ALL, '')


from bson.son import SON

from unir_texto import * # Llama a la función que une el texto


##//////////////////////////////////////////////////////////////////////////////
## Texto respuesta
##//////////////////////////////////////////////////////////////////////////////

# Texto ejemplo:
#   - El barrio de Benimaclet paga 6,428,288.48 € de impuestos en el año 2016

# Texto en la lista:
textoRespuesta = [u"El barrio de ", u" paga ", u"€ de ", u" en el año "]


##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////
def pagoBarrios(result,db):
    print u"Recibimos petición de", result["action"]
    dbBarrios = db.barrios # Accedemos a la colección donde almacenamos todos los datos

    # Sacamos los parámetros  de result ----------------------------------------
    try: 
        impuesto = result["parameters"]["impuestos"]
        barrio = result["parameters"]["barrios"]
        anyo = result["parameters"]["anyo"]
    except:
        print u"    - Error al obtener los parametros"
    #---------------------------------------------------------------- parámetros
    try:
        valor, anyo = valorPagoBarrios(impuesto,barrio,anyo,dbBarrios)
 
    except:
        print u"    - Error función valor"

    try:
        if valor == u"-1,00" or valor == u"-1.00":
            texto = u"No disponemos de los datos del año "+unicode(anyo)
        else:
            texto = unirTexto(textoRespuesta, barrio, valor, impuesto, anyo)
    except:
        print u"    - Error función unirTexto"
    #Condiciones unirTexto():
    #   - Ejemplo de uso: unirTexto(textoRespuesta, parámetro1, parámetro2)
    #   - Puede tener muchos parámetros.
    #   - len(textoRespuesta) = Núm. parámetros que insertamos (barrio, etc.)
    #   - El resultado será: texto[0]+parametro1+texto[1]+parametro2+etc.

    return texto


##//////////////////////////////////////////////////////////////////////////////
## Funciones
##//////////////////////////////////////////////////////////////////////////////

def valorPagoBarrios(impuesto,barrio,anyo,dbBarrios):   

    if anyo == u"null": #Sin datos de año cogemos el último año
        anyo = { "$exists": "true" }

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
    except:
        print u"     - Error en suma"
        
    try:
        pipeline[3]["$project"]["valor"]["$sum"].extend(suma)
    except:
        print u"     - Error al añadir suma a pipline"   

    # Consulta DB
    try:
        respuesta = list(dbBarrios.aggregate(pipeline))
    except:
        print "     - Error en la consulta PagoBarrios"

    if respuesta == []:
        valor = -1
    else:
        valor = respuesta[0][u"valor"]
        anyo = respuesta[0][u"anyo"]

    
    
##    for dato in respuesta:
##        print type(dato)
##        valor = dato[u"valor"]
##        anyo = dato[u"anyo"]
##        break

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

    else:
        print u"     - Error en valorPagoBarrios - Datos sin año"

    return suma

    
