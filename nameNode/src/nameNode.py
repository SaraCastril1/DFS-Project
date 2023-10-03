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


    def load_metadata_from_log(self, log_file_path):
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                parts = line.strip().split('|')
                #print(parts)
                if len(parts) >= 3:
                    file_name = parts[0].strip()
                    immediate_folder = parts[1].strip()
                    data_nodes = [dn.strip() for dn in parts[2:]]
                self.add_file(file_name, immediate_folder, data_nodes)





    def add_file(self, fileName, immediateFolder, dataNodes):

        self.metaData[fileName.strip()] = {
            "Immediate folder": immediateFolder.strip(),
            "Data nodes": dataNodes
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
            data_nodes = self.metaData[fileName]["Data nodes"]  # Cambio aquí: fileName en lugar de file_name
            return apiGateway_nameNode_pb2.ReadFileResponse(file_id=fileName, data_node_addresses=data_nodes)
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
    file_service.load_metadata_from_log(r"C:\Users\dulce\OneDrive\Escritorio\EAFIT\2023-2\Telematica\Proyect\DFS-PROYECT-DEFINITIVO\DFS-Project\nameNode\metadata.log")
    # file_service.add_file(".env", ".", "50052")
    # file_service.add_file("Makefile", ".", "50052")
    # file_service.add_file("casco.jpg", ".", "50052")
    # file_service.add_file("casemiro.gif", ".", "50052")
    # file_service.add_file("testfile.txt", ".", "50052")
    # file_service.add_file("dataNode.py", "src", "50052")
    # file_service.add_file("dataNode_apiGateway_pb2_grpc.py", "src", "50052dn1")
    # file_service.add_file("dataNode_apiGateway_pb2.pyi", "src", "50052")
    # file_service.add_file("dataNode_apiGateway_pb2.py", "src", "50052")
    # file_service.add_file("dataNode-apiGateway.proto", "protobufs", "50052")

    print(file_service.metaData)

    server.start()
    server.wait_for_termination()

def main():
    serve()

if __name__ == "__main__":
    main()
