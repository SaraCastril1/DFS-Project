from concurrent import futures
from dotenv import dotenv_values
import os
import grpc
import dataNode_apiGateway_pb2
import dataNode_apiGateway_pb2_grpc


config = dotenv_values(".env")

DN1 = config['HOST-1']
DN2 = config['HOST-2']

class File(dataNode_apiGateway_pb2_grpc.DataNodeServiceServicer):
      def ReadFile(self,request,context):
            try:
                  with open(request.file_name, 'rb') as file:
                        print(request.file_name)
                        file_contents = file.read()
                        response = dataNode_apiGateway_pb2.ReadFileResponseData(file_data=file_contents)
                        return response
                  
            except Exception as error:
                  return(error)
            


def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[('grpc.max_receive_message_length', 1024 * 1024 * 100)])
        dataNode_apiGateway_pb2_grpc.add_DataNodeServiceServicer_to_server(File(), server)
        server.add_insecure_port(DN1)
        print("DataNode {} is running... ".format(DN1))
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    serve()