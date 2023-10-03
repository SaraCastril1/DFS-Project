# info de la materia: ST0263 Temas especiales en telemática
#
# Estudiante(s): Manuela Tolosa Gracia, mtolosag@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co
#

# Procesos comunicantes por API REST, RPC y MOM
#
# 1. breve descripción de la actividad
#
<texto descriptivo>
En este proyecto, desarrollé dos microservicios mserv1 y mserv2 que se comunican con  API Gateway a través de RPC y MOM. Usamos REST API  y gRPC para RPC y elegimos MOM para  RabbitMQ. Los microservicios se centran en enumerar y buscar archivos. Cada microservicio tiene un archivo de configuración que se carga al inicio. MOM se utiliza como respaldo en caso de problemas de comunicación RPC. Implementó una puerta de enlace API  en Node.js usando Express para probar la funcionalidad de sus microservicios. En resumen, este proyecto permite una comunicación sólida y flexible entre microservicios para proporcionar servicios relacionados con archivos.

## 1.1.Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
En términos de requisitos funcionales, fue posible implementar  dos servicios (enumerar archivos y encontrar si existen) a través del middleware gRPC al que se accede a través de una puerta de enlace API. Cuando se realiza una solicitud a API Gateway, primero se comunica  con el servicio a través de gRPC y, si eso falla, se comunica de forma asincrónica a través de MOM. 

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
La única parte que no se cumplió del enunciado del reto fue que cuando le llega un mensaje a la cola del MOM el consumer es capaz de leer los mensajes pero no de devolver una respuesta. 

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se trató de implementar la arquitectura planteada por el profesor, en la cual se tiene el Postman que se conecta al API Gateway mediante el API rest , el API Gateway tiene dos conexiones, la primera con el servidor 2 y están conectados a través de la comunicación gRPC y la segunda conexión es con el servidor 1 y entre esa conexión esa la conexión con el servidor MOM.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
lenguaje: JavaScript.

librerias: express, dotenv, amqplib, glob, fs, @grpc/grpc-js

## como se compila y ejecuta.
En primera parte se debe de asegurar que la imagen del Docker este corriendo con el comando “docker start rabbit-Server”. Segundo debes entrar a la carpeta de API Gateway y escribir el comando “npm start” luego en otra consola de la misma máquina virtual entrar a la carpeta “microservicio 1” y hacer el mismo comando (“npm start”) , se sigue el mismo procedimiento con el “microservicio 2”.despues desde un cliente (postman) para ver la lista de archivos debes hacer un GET a la siguiente IP:54.225.226.200:3000/listararchivos/ , luego para buscar un archivo en específico se debe hacer un POST a la siguiente IP: 54.225.226.200:3000/buscararchivos/ (IMPORTANTE :el body de la request POST debe seguir el siguiente formato tipo json  
{
  "file":""
}
Dentro de las comillas colocar el archivo a buscar, se aceptan wildcards)

Para probar el MOM matar el proceso del microservicio 1 

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
Cada microservicio cuenta con sus propias variables de entorno donde cada una se define el puerto , las direcciones para las conexiones  a los servidores , la dirección de la carpeta en la cual se almacenas los archivos .

## 
## resultados o pantallazos 

