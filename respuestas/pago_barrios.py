#!/usr/bin/python
# -*- coding: utf-8 -*-

##//////////////////////////////////////////////////////////////////////////////
## Importar
##//////////////////////////////////////////////////////////////////////////////

# Importar locales solo si el valor resultado es numérico
import locale #Librería que nos permite adaptar el formato numérico al Español
locale.setlocale(locale.LC_ALL,'')

from unir_texto import *


##//////////////////////////////////////////////////////////////////////////////
## Texto respuesta
##//////////////////////////////////////////////////////////////////////////////

# Texto ejemplo:
#   - El barrio de Benimaclet paga 6,428,288.48 € de impuestos
# Texto en la lista:
textoRespuesta = [u"El barrio de ", u" paga ", u"€ de "]


##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////
def pagoBarrios(result,dbValencia):
    print u"Recibimos petición de", result["action"]

    # Sacamos los parámetros  de result ---------------------------------------
    impuesto = result["parameters"]["impuestos"]
    barrio = result["parameters"]["barrios"]
    #--------------------------------------------------------------- parámetros
    
    query = {"barrio": barrio.lower()} #------------------------------------ Consulta
    
    try:
        cursor = dbValencia.find(query) # Realizamos la consulta en la BD
    except:
        print "Error en la consulta: ", query
        
    valor = valorPagoBarrios(cursor, impuesto)
    
    texto = unirTexto(textoRespuesta, barrio, valor, impuesto)
    #Condiciones unirTexto():
    #   - Ejemplo de uso: unirTexto(textoRespuesta, parámetro1, parámetro2)
    #   - Puede tener muchos parámetros.
    #   - len(textoRespuesta) = Núm. parámetros que insertamos (barrio, etc.)
    #   - El resultado será: texto[0]+parametro1+texto[1]+parametro2+etc.

    return texto


##//////////////////////////////////////////////////////////////////////////////
## Funciones
##//////////////////////////////////////////////////////////////////////////////

def valorPagoBarrios(cursor, impuesto):
    try:
        # Por la estructura de la BD solo nos interesa obtener el último doc.
        doc = cursor[0]

        # Según el impuesto calculamos el valor con la fórmula que toque
        if impuesto == "impuestos":
            valor = float(doc[u"IVTNU Esforç Fiscal Personas Jurídicas"])+float(doc[u"IVTNU Esforç Fiscal Personas Físicas"])+float(doc[u"IAE Esforç Fiscal"])+float(doc[u"IVTM Esforç Fiscal Persones Jurídicas"])+float(doc[u"IVTM Esforç Fiscal Persones Físicas"])+float(doc[u"IBI Esforç Fiscal Persones Jurídicas"])+float(doc[u"IBI Esforç Fiscal Persones Físicas"])

        elif impuesto=="IVTNU":
            valor = float(doc[u"IVTNU Esforç Fiscal Personas Jurídicas"])+float(doc[u"IVTNU Esforç Fiscal Personas Físicas"])
                
        elif impuesto=="IAE":
            valor = float(doc[u"IAE Esforç Fiscal"])
                
        elif impuesto=="IVTM":
            valor = float(doc[u"IVTM Esforç Fiscal Persones Jurídicas"])+float(doc[u"IVTM Esforç Fiscal Persones Físicas"])
                
        elif impuesto=="IBI":
            valor = float(doc[u"IBI Esforç Fiscal Persones Jurídicas"])+float(doc[u"IBI Esforç Fiscal Persones Físicas"])
    
        else:
            valor = -1
    except:
         print "Error en la gestión de la consulta sobre el impuesto: ", impuesto
         valor = -1

    # Cambia el formato para que aparezcan los . de millar y solo 2 decimales
    valor = locale.format("%.2f", valor, grouping=True)
    return valor
    
