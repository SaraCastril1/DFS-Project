from concurrent import futures
from dotenv import dotenv_values
import os
import grpc
import dataNode_apiGateway_pb2
import dataNode_apiGateway_pb2_grpc

config = dotenv_values("../.env")

HOST = config['HOST']


class File(dataNode_apiGateway_pb2_grpc.DataNodeServiceServicer):
      def ReadFile(self,request,context):
            file = open('testfile.txt')
            return dataNode_apiGateway_pb2.ReadFileResponseData(file_data=file)


def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        dataNode_apiGateway_pb2_grpc.add_DataNodeServiceServicer_to_server(File(), server)
        server.add_insecure_port(HOST)
        print("Service find/list is running... ")
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    serve()