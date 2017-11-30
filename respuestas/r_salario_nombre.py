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

from unir_texto import unirTexto # Llama a la función que une el texto
##//////////////////////////////////////////////////////////////////////////////
## Texto respuesta
##//////////////////////////////////////////////////////////////////////////////

# Texto ejemplo (2 mensajes):
# M1 - Joan Ribó gana 82.602,94 € de retribución anual bruta (sin antigüedad) por su cargo de Alcalde desde el 08 de julio de 2015.
# M2 - O lo que es lo mismo 5.900.21 € mensuales con 2 pagas extras en junio y diciembre.

# Texto en la lista:
textoRespuesta1 = {
        "Cast": [u"", u" gana ", u"€ de retribución anual bruta (sin antigüedad) por su cargo de ", u" desde el ", u"."],
        "Val": [u"", u" guanya ", u"€ de retribució anual bruta (sense antiguitat) pel seu càrrec de ", u" des del ", u"."]
        }

textoRespuesta2 = {
        "Cast": [u"O lo que es lo mismo ", u"€ mensuales con 2 pagas extras en junio y diciembre."],
        "Val": [u""]
        }

textoFaltaNombre = {
        "Cast": [u"Pregunta otra vez."],
        "Val": [u"Pregunta altra volta."]
        }

textoAnyoSinDatos = {
        "Cast": [u"Pregunta otra vez."],
        "Val": [u"Pregunta altra volta."]
        }


##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////
def salarioNombre(result,db):
    print time.strftime("%c"), "- Recibimos petición de salarioNombre"
    dbSalarios = db.salarios # Accedemos a la colección donde almacenamos todos los datos


    # Sacamos los parámetros  de result ----------------------------------------
    try:
        nombre = result["parameters"]["nombre"]
        anyo = result["parameters"]["anyo"]
        idioma = result["parameters"]["idioma"]
    except Exception as e:
        print "     ", time.strftime("%c"), "- Error al obtener los parametros: ", type(e), e
    #---------------------------------------------------------------- parámetros

    # Si falta nombre se pide
    if nombre == u"":
        return textoFaltaNombre[idioma]

    try:
        valor, valorMes, cargo, fecha = valorSalarioNombre(nombre, anyo, dbSalarios)
    except Exception as e:
        print "     ", time.strftime("%c"), "- Error función valor: ", type(e), e

    try:
        if valor == u"-1,00" or valor == u"-1.00":
            texto = unirTexto(textoAnyoSinDatos[idioma], anyo)
        else:
            valorMes = valor/14
            texto1 = unirTexto(textoRespuesta1[idioma], nombre, valor, cargo, fecha)
            texto2 = unirTexto(textoRespuesta2[idioma], valorMes)

    except Exception as e:
        print "     ", time.strftime("%c"), "- Error función unirTexto: ", type(e), e

    return texto1



##//////////////////////////////////////////////////////////////////////////////
## Funciones
##//////////////////////////////////////////////////////////////////////////////

def valorSalarioNombre(nombre, anyo, dbSalarios):
    valor = 82602.94
    cargo = u"Alcalde"
    fecha = u"20/07/2016"

    valorMes = valor/14
    return valor, valorMes, cargo, fecha
