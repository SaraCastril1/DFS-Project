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

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas:

### Componentes:

#### Cliente: 
El cliente es la interfaz principal a través de la cual los usuarios acceden y administran los archivos en el sistema de archivos distribuidos. Proporcionar una API  de línea de comandos (CLI) para interactuar con el DFS.

#### NameNode Leader: 
Es responsable de llevar un registro de la ubicación de los archivos en el sistema. Su tarea principal es mantener un mapa de qué archivos se almacenan en qué DataNodes y garantizar que haya al menos dos copias de cada archivo para tolerancia a fallos. También debe tomar decisiones sobre la asignación de archivos a DataNodes para la escritura inicial y las réplicas de archivos.

#### NameNode Follower:
El NameNode seguidor no procesa solicitudes de escritura ni asigna ubicaciones para nuevos bloques de datos. Pero realizar procesos de lectura en caso de ser necesario, pero su función principal es estar sincronizado con el líder y listo para tomar el control en caso de un fallo.

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


![Arquitectura_Telemática drawio](https://github.com/SaraCastril1/DFS-Project/assets/84990901/9a5a4612-4fff-43d6-9a8a-0ce022fd8fea)

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

## como se compila y ejecuta.
Para compilar debes colocar en la consola :hay que ubicarse en la carpeta que quieres ejecutra,le das "cd .\nameNode\" luego enter  das enter y despues ingresas "make NameNode"
Para ejecucion: "python .\src\nameNode.py"
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

## detalles técnicos
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## 
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto

#### versión README.md -> 1.0 (2022-agosto)
