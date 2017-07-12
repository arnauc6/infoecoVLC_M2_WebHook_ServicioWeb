#!/usr/bin/python
# -*- coding: utf-8 -*-

def unirTexto(texto, *parametros):
    respuesta = u""
    if len(texto)+1==len(parametros): #R+p+R+p+R
        for i in range(0,len(texto)):
            respuesta = respuesta+texto[i]+unicode(parametros[i])
        respuesta = respuesta+texto[i]
    # 
    # elif len(texto)==len(parametros): #R+p+R+p
    #     for i in range(0,len(texto)):
    #         respuesta = respuesta+texto[i]+unicode(parametros[i])

##    print respuesta

    return respuesta
