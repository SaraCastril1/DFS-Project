## info de la materia: Tópicos especiales en Telemática st0263 
#
## Estudiante(s): 
- Simon Gomez Arango - sgomez13@eafit.edu.co
- Sara María Castrillón Ríos - smcastril1@eafit.edu.co
- Manuela Tolosa - mtolosag@eafit.edu.co
#
## Profesor: 
Edwin Nelson Montoya Múnera - emontoya@eafit.edu.co
#
# Sistema de archivos distribuidos:

## 1. breve descripción de la actividad
#
Un sistema de archivos distribuidos, permite compartir y acceder de forma concurrente un conjunto de archivos que se encuentran almacenados en diferentes nodos. Uno de los sistemas más maduros, vigente y antiguo de estos sistemas es el NFS (Network File System) desarrollado en su momento por Sun Microsystems y que hoy en día es ampliamente usado en sistemas Linux. 
Este proyecto, propone un NFS como se describirá más adelante.

Acceda al marco teoríco en el siguiente link -> Informe.pdf

## Que se logró y que no se logro:
### A Nivel funcional:
- **Se logró**
  - El listado de archivos
  - La busqueda de archivos
  - La escritura de archivos
  - La lectura de archivos
  - Todos lo requisitos funcionales
- **No se logró**:
  - Nada
### A nivel no funcional:
- **Se logró**
  - La replicación de los datanodes
  - La tolerancia a fallos de los datanode, cuando se cae un datanode su follower lo remplaza y se evita la caida del servicio
- **No se logró**
  - Que el ciente se comuniqué directamente con el dataNode
  - replicación y tolerancia a fallos en el nameNode   

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas:

### Componentes:

#### Cliente: 
El cliente es la interfaz principal a través de la cual los usuarios acceden y administran los archivos en el sistema de archivos distribuidos. Proporcionar una aplicación web donde se puede realizar todas las operacioes

#### NameNode Leader: 
Es responsable de llevar un registro de la ubicación de los archivos en el sistema. Su tarea principal es mantener un mapa de qué archivos se almacenan en qué DataNodes y garantizar que haya al menos dos copias de cada archivo para tolerancia a fallos. También debe tomar decisiones sobre la asignación de archivos a DataNodes para la escritura inicial y las réplicas de archivos.

#### DataNodes: 
Los DataNodes son los nodos de almacenamiento reales donde se ubican los archivos. Cada DataNode es responsable de almacenar y administrar los archivos que se le asignan. Además, un DataNode puede actuar como líder (Leader) o seguidor (Follower) para ciertos archivos para garantizar la tolerancia a fallos y la redundancia. Los DataNodes deben además proporcionar un canal de datos para que los clientes escriban y lean archivos directamente.

### Flujo de operación:

#### Escritura de un archivo:
- El cliente se comunica con el NameNode para solicitar la escritura de un archivo.
- El NameNode selecciona un DataNode adecuado para la escritura inicial y notifica al cliente.
- El cliente envía el archivo al DataNode seleccionado.
- El DataNode seleccionado se convierte en el líder (Leader) del archivo y luego replica el archivo en otro DataNode que actúa como seguidor (Follower) para garantizar la tolerancia a fallos.
  
#### Lectura de un archivo:
- El cliente se comunica con el NameNode para solicitar la lectura de un archivo.
- El NameNode selecciona al menos dos DataNode que contienen el archivo para su lectura para la lectura y notifica al cliente.
- El cliente selecciona uno de los DataNodes y recupera el archivo directamente desde ese DataNode. En caso de fallo, puede intentar recuperar el archivo de otro DataNode.
  
#### Tolerancia a fallos:
- Si un DataNode falla, el NameNode debe ser capaz de detectarlo y tomar medidas para reemplazar la réplica del archivo en otro DataNode.
- El DataNode líder (Leader) para un archivo debe asegurarse de que su réplica en el DataNode seguidor (Follower) esté actualizada y lista para asumir el liderazgo en caso de fallo.

#### Canal de Control y Canal de Datos:
El canal de control se utiliza para la comunicación entre el cliente y el NameNode para solicitar información sobre archivos y para la administración general del DFS.
El canal de datos se utiliza para la transferencia directa de archivos entre el cliente y los DataNodes.

#### Selección de DataNode:
La selección de DataNode inicial para la escritura y lectura puede ser gestionada por el NameNode utilizando un criterio de optimización, como el enfoque de round-robin para equilibrar la carga.

![diagrama_corregido drawio](https://github.com/SaraCastril1/DFS-Project/assets/67118511/ba6c43b2-e7de-468d-ac14-e319fa926e47)


### Requisitos Funcionales:
-Escritura y Lectura de Archivos: El DFS debe permitir a los usuarios escribir y leer archivos de manera eficiente y confiable, tanto localmente como de 		forma distribuida.

-Replicación de Datos: El sistema debe ser capaz de replicar archivos en múltiples DataNodes para garantizar la tolerancia a fallos y la disponibilidad.

-Tolerancia a Fallos: El sistema debe ser capaz de detectar y recuperarse automáticamente de fallos en los DataNodes o en otros componentes del sistema.

-Gestión de Metadatos: Debe existir una gestión eficiente de metadatos, lo que incluye la gestión de la estructura de directorios y los atributos de 		archivos.

-Control de Acceso: El sistema debe proporcionar un mecanismo de control de acceso para garantizar que solo los usuarios autorizados puedan acceder a 		los archivos.

-Listado de Archivos: Los usuarios deben poder listar los archivos y directorios en el sistema para navegar y buscar archivos.

### Requisitos No Funcionales:
-Escalabilidad: El sistema debe ser escalable y capaz de manejar un gran volumen de archivos y usuarios.

-Rendimiento: Debe ser eficiente en términos de rendimiento para garantizar una lectura y escritura rápidas de archivos.

-Disponibilidad: El sistema debe estar disponible en todo momento para los usuarios, incluso en presencia de fallos.

-Escritura y Lectura de Archivos: El DFS debe permitir a los usuarios escribir y leer archivos de manera eficiente y confiable, tanto localmente como de 		forma distribuida.

-Replicación de Datos: El sistema debe ser capaz de replicar archivos en múltiples DataNodes para garantizar la tolerancia a fallos y la disponibilidad.

-Tolerancia a Fallos: El sistema debe ser capaz de detectar y recuperarse automáticamente de fallos en los DataNodes o en otros componentes del sistema

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Lenguaje de programacion: Python

Librerias :Flask , Grpcio y Vue js

## como se compila y ejecuta.
Todas las dependencias estan en el archivo dfs_env.yml sobre el cual se puede crear un entorno de conda de la siguiente forma:
```
conda env create -f dfs_env.yml
```
### Para ejectutar el dfs:

  - Para ejecturar el proyecto hay que correr por separado el namenode, el apigateway y los datanodes.
    - Para correr el api:
      - Moverse hastta la carperta api-gateway
      - Desde esa misma carpeta ejecutar el comando: ```sudo python src/api2.py```
  - Para correr el NameNode:
   - Moverse hasta la carpeta namenode
   - Ejecutar el comando ```python src/namenode.py```
 - Para correr los datanodes:
   - Hay 3 datanodes lideres y 3 datanode followers, moverse hasta la carpeta de cada datanode
   - Ejecutar el comando: ```python src/datanode.py```
   - **IMPORTANTE:** Si dentro de la carpeta de cada datanode no existe una carpeta files, crearla con el comando: ```mkdir files```
  

### Para ejecutar el cliente:
- Moverse hasta la carpeta front_client/dfs_client
- Ejecutar ```npm i``` (Si es la primera vez que lo corre)
- Ejecutar ```npm run dev```


Se hace lo mismo para el apiGateway y el dataNode , la unica diferencia es que en ves NameNode colocas  apiGateway o el dataNode que usaras ya que son 3.

## detalles del desarrollo.
Fase 1: Definición de Requisitos y Diseño Inicial 
Fase 2: Implementación del NameNode 

- Implementación del NameNode: Inicia la implementación del NameNode, centrándote en la gestión de metadatos y la comunicación con el cliente.

- Protocolo Cliente-NameNode: Define y crea los archivos proto para las operaciones de comunicación entre el cliente y el NameNode.


Fase 3: Implementación de DataNodes y Comunicación Cliente-DataNode 

- Implementación de DataNodes: Comienza a implementar la lógica de los DataNodes, centrándote en el almacenamiento y la replicación de datos.

- Protocolo Cliente-DataNode: Define y crea los archivos proto para las operaciones de comunicación entre el cliente y los DataNodes.

Fase 4: Pruebas Iniciales

- Pruebas de Integración: Realiza pruebas de integración básicas para verificar que el cliente pueda comunicarse con el NameNode y los DataNodes.

- Pruebas de Escritura y Lectura: Implementa operaciones de escritura y lectura básicas para validar que el sistema pueda almacenar y recuperar archivos.

Fase 5: Réplica de Datos 

- Implementación de la Réplica: Implementa la lógica necesaria para la replicación de datos entre DataNodes.

- Pruebas de Tolerancia a Fallos: Realiza pruebas para asegurarte de que el sistema pueda recuperarse de manera adecuada en caso de fallo de un DataNode.


Fase 6: Documentación y Entrega.


# descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## IP o nombres de dominio en nube o en la máquina servidor.
nameNode -> localhost:50051
dataNode -> localhost:50052
nameNode2 -> localhost:6000
nameNode3 -> localhost:6500

## como se lanza el servidor.
En el repositorio hay un archivo .yml con la version de Python y todas las dependencias que necesita el proyecto.Una ves instalada todas estas dependencias para correr el  apiGateway hay que moverse a la carpeta de la misma y colocar el siguiente comando "sudo python src/apigateway.py" y asi con el datanode y el namenode solo que cambia el comando para correr el datanode ```python src/datanode.py``` y para el namenode ```python src/namenode.py ```.

Para correr el cliente hay que dirigirse a la carpeta de dfs_client y corres los siguientes comandos:
```npm install``` (cuando es por primera vez)
```npm run dev``` (para correrlo)


## una mini guia de como un usuario utilizaría el software o la aplicación
Esta desplegado en: http://18.214.11.58:5000/
![image](https://github.com/SaraCastril1/DFS-Project/assets/74980999/2a616349-ddf3-411f-9ec1-236bdcd8dd85)
![image](https://github.com/SaraCastril1/DFS-Project/assets/74980999/dd950dd7-866e-486b-a4de-4aa414aa80df)
![image](https://github.com/SaraCastril1/DFS-Project/assets/74980999/5dc13488-24f1-42d8-88f0-5b994a3e2ae3)



