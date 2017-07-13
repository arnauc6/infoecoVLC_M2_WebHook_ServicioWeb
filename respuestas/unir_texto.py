#!/usr/bin/python
# -*- coding: utf-8 -*-

def unirTexto(texto, *parametros):
    '''
    Condiciones unirTexto():
       - Ejemplo de uso: unirTexto(textoRespuesta, parámetro1, parámetro2)
       - Puede tener muchos parámetros.
       - len(textoRespuesta)+1 = Núm. parámetros que insertamos (barrio, etc.)
       - El resultado será: texto[0]+parametro1+texto[1]+parametro2+etc+texto[n].
    '''

    respuesta = u""

    if len(texto)-1==len(parametros): #R+p+R+p+R
        for i in range(0,len(parametros)):
            respuesta = respuesta+texto[i]+unicode(parametros[i])
        respuesta = respuesta+texto[i+1]
    #
    # elif len(texto)==len(parametros): #R+p+R+p
    #     for i in range(0,len(texto)):
    #         respuesta = respuesta+texto[i]+unicode(parametros[i])


    return respuesta
