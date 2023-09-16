## info de la materia: Tópicos especiales en Telemática st0263 
#
## Estudiante(s): 
- Simon Gomez Arango - sgomez13@eafit.edu.co
- Sara María Castrillón Ríos - smcastril1@eafit.edu.co
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
Arquitectura_Telemática.drawio.png

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


