# **Módulo 2: WebHook (Servicio Web)**

Módulo responsable de gestionar las respuestas a las preguntas ya clasificadas por el agente inteligente. Consulta los datos actualizados y construye la respuesta final. Se comunica con el módulo 4 (Integración Telegram). Si quieres más información entra al proyecto **[infoecoVLC: Asistente virtual para información económica municipal](https://github.com/areahackerscivics/infoecoVLC)**

## Descripción
![](https://github.com/areahackerscivics/infoecoVLC_M2_WebHook_ServicioWeb/blob/master/Documentaci%C3%B3n/Diagrama_M2-WebHook.png)


## Guía de uso

### Lenguaje de programación
Python 2.7.12

### Librerías empleadas
Las librerías actualizadas siempre estarán actualizadas en el documento [**requirements.txt**](./requirements.txt) consultar en caso de errores.

    Flask==0.12
    pymongo==3.4.0

### Instalación
El modulo consta con todos los archivos necesarios para ser ejecutado en utilizando apache y la librería flask. La guía de instalación cuenta con que se tiene instalado apache. De no ser el caso podéis instalarlo siguiendo la guía de instalación de apache.

**Pasos**
1. Instalar apache:

        sudo apt-get install apache2

    Versión emplada:

        apache2 = 2.4.18-2ubuntu3.5

1. Instalar pip y virtualenv:

        sudo apt-get install python-pip virtualenv

    Versión empleadas:

        python-pip = 8.1.1-2ubuntu0.4
        virtualenv = 15.0.1+ds-3ubuntu1

1. Iniciamos modo sudo:

        sudo su

1. Nos movemos a una carpeta donde hay documentos de configuración:

        cd /etc/apache2/sites-available/

1. Creamos un nuevo archivo:

        nano flask.conf

    Copiamos en el archivo "flask.conf":

        <VirtualHost *:80>
                serverName   flaskapp.com
                WSGIScriptAlias / /var/www/python/infoecoVLC_M2_WebHook_ServicioWeb/webhook.wsgi

                <Directory /var/www/python/infoecoVLC_M2_WebHook_ServicioWeb/>
                Order allow,deny
                Allow from all
                </Directory>

                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/error.log combined

        </VirtualHost>

1. Instalamos wsgi:

        apt-get install libapache2-mod-wsgi

    Versión empleadas:

        libapache2-mod-wsgi = 4.3.0-1.1build1

1. Creamos las siguientes carpetas:

        cd /var/www/
        mkdir python
        cd python/

1. Descargamos el módulo:

        git clone https://github.com/areahackerscivics/infoecoVLC_M2_WebHook_ServicioWeb.git

1. Cambiamos el  nombre de variables_ejemplo.py por **variables.py**.

        cd infoecoVLC_M2_WebHook_ServicioWeb
        mv variables_ejemplo.py variables.py

1. Sustituir las “XXX” de dentro de **variables.py** por las variables personales.

        nano variables.py

1. Instalamos flask: (Y el resto de librerías).

        pip install flask
        pip install pymongo


1. Cambiamos el archivo de configuración:

        a2ensite flask.conf

1. Deshabilitamos el anterior .conf

        a2dissite 000-default.conf

1. Reiniciamos el servicio apache:

        service apache2 reload

## Colaboración
Se puede colaborar:
- Difundiendo.
- Ampliando o modificando el proyecto.

## Términos de uso

El contenido de este repositorio está sujeto a la licencia [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

![](https://www.gnu.org/graphics/gplv3-127x51.png)
