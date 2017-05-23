#!/usr/bin/python
# -*- coding: utf-8 -*-

def unirTexto(texto, *parametros):
    respuesta = u""
    if len(texto)==len(parametros):
        for i in range(0,len(texto)):
            respuesta = respuesta+texto[i]+unicode(parametros[i])

##    print respuesta

    return respuesta
