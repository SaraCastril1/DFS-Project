from concurrent import futures
from dotenv import dotenv_values
import os
import grpc
import fnmatch
import apiGateway_nameNode_pb2
import apiGateway_nameNode_pb2_grpc

config = dotenv_values(".env")
HOST = config['HOST']

class File(apiGateway_nameNode_pb2_grpc.NameNodeServiceServicer):
    def __init__(self):
        self.data_nodes = ["dn1"]
        self.metaData = {}

    def add_file(self, fileName, immediateFolder, dataNode):
        self.metaData[fileName] = {
            "Immediate folder": immediateFolder,
            "Data node": dataNode
        }

    def WriteFile(self, request, context):
        fileName = request.filename
        immediateFolder = request.folder
        dataNode = self.data_nodes[0]  # Supongamos que siempre usamos el primer DataNode

        self.add_file(fileName, immediateFolder, dataNode)
        print("Added --> ", self.metaData[fileName])

        return apiGateway_nameNode_pb2.WriteFileResponse(file_id=fileName, data_node_addresses=[dataNode])

    def ReadFile(self, request, context):
        fileName = request.filename
        immediateFolder = request.folder

        if fileName in self.metaData:
            dataNode = self.metaData[fileName]["Data node"]
            return apiGateway_nameNode_pb2.ReadFileResponse(file_id=fileName, data_node_addresses=[dataNode])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"El archivo '{fileName}' no se encontró en el sistema.")
            return apiGateway_nameNode_pb2.ReadFileResponse()

    def ListFiles(self, request, context):
        file_names = list(self.metaData.keys())

        return apiGateway_nameNode_pb2.ListFilesResponse(filenames=file_names)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service = File()
    apiGateway_nameNode_pb2_grpc.add_NameNodeServiceServicer_to_server(file_service, server)
    server.add_insecure_port(HOST)
    print("NameNode {} is running... ".format(HOST))

    # Agrega archivos a la estructura de datos metaData antes de iniciar el servidor
    file_service.add_file(".env", ".", "50052")
    file_service.add_file("Makefile", ".", "50052")
    file_service.add_file("casco.jpg", ".", "50052")
    file_service.add_file("casemiro.gif", ".", "50052")
    file_service.add_file("testfile.txt", ".", "50052")
    file_service.add_file("dataNode.py", "src", "50052")
    file_service.add_file("dataNode_apiGateway_pb2_grpc.py", "src", "50052dn1")
    file_service.add_file("dataNode_apiGateway_pb2.pyi", "src", "50052")
    file_service.add_file("dataNode_apiGateway_pb2.py", "src", "50052")
    file_service.add_file("dataNode-apiGateway.proto", "protobufs", "50052")

    print(file_service.metaData)

    server.start()
    server.wait_for_termination()

def main():
    serve()

if __name__ == "__main__":
    main()
