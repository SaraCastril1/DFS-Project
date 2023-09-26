from concurrent import futures
from dotenv import dotenv_values

import os
import grpc
import fnmatch
import file_pb2
import file_pb2_grpc
#CONSUMER
config = dotenv_values("../.env")

HOST = config['HOST']



#Link el microservicio con una clase de python
class File(file_pb2_grpc.FileServicer):
        
        def Find_file(self, request, context):
                file_path = os.path.join(request.file)
                print("Find: ",file_path)
                if os.path.exists(file_path):
                        return file_pb2.file_response(file= 1, coincidence = [file_path])
                else:
                       #return file_pb2.file_response(file= 0, coincidence = 'File not found')
                       matching_files = fnmatch.filter(os.listdir("."), os.path.basename(file_path))
                       if matching_files:
                            return file_pb2.file_response(file=1, coincidence = matching_files)
                       else:
                             return file_pb2.file_response(file= 0, coincidence = ["File not found -> No coincidences"])
                
        def List_file(self, request, context):
              try:
                files = os.listdir(request.file)
                print("List: ", request.file)
                return file_pb2.list_response(file = files)
              except OSError as e:
                return f"Error listing files in '{request.file}': {e}"
                #return []
                

               
      
       
   
#    def AddProduct(self, request, context):
#       print("Request is received: " + str(request))
#       return Service_pb2.TransactionResponse(status_code=1)

def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        file_pb2_grpc.add_FileServicer_to_server(File(), server)
        server.add_insecure_port(HOST)
        print("Service find/list is running... ")
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    serve()