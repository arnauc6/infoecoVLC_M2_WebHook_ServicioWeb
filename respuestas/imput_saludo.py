#!/usr/bin/python
# -*- coding: utf-8 -*-

##//////////////////////////////////////////////////////////////////////////////
## Importar
##//////////////////////////////////////////////////////////////////////////////

from unir_texto import *


##//////////////////////////////////////////////////////////////////////////////
## Texto respuesta
##//////////////////////////////////////////////////////////////////////////////

# Texto ejemplo:
#   - El barrio de Benimaclet paga 6,428,288.48 € de impuestos
# Texto en la lista:
##textoRespuesta = [u"El barrio de ", u" paga ", u"€ de "]
textoRespuesta = u"Buenos días"


##//////////////////////////////////////////////////////////////////////////////
## Funcion principal
##//////////////////////////////////////////////////////////////////////////////

def imputSaludo(result,dbValencia):
    print u"Recibimos petición de", type(result["action"])
    texto = textoRespuesta
    return texto
