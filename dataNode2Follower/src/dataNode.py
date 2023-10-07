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

      # def ReadFile(self,request,context):
      #       try:
      #             with open(f"files/{request.file_name}", 'rb') as file:
      #                   file_contents = file.read()
      #                   response = dataNode_apiGateway_pb2.ReadFileResponseData(file_data=file_contents)
      #                   return response
                  
      #       except Exception as error:
      #             return(error)
      def ReadFile(self,request,context):
            print(f'file request: {request.file_name}')
            
            try:
                  with open(f'files/{request.file_name}', 'rb') as file:
                        print(request.file_name)
                        file_contents = file.read()
                        response = dataNode_apiGateway_pb2.ReadFileResponseData(file_data=file_contents)
                        return response
                  
            except Exception as error:
                  return(error)


      # def WriteFile(self, request, context):
      #       if(request.create_folder != ''):
      #             os.mkdir(f"files/{request.create_folder}")
                  
      #       try:
      #             with open(f"files/{request.folder}/{request.filename}",'wb') as file:
      #                         file.write(request.file_data)
      #             response = dataNode_apiGateway_pb2.WriteFileResponseData(write_success=True)
      #             print(response)
      #             #replication_response = Replicate(request.filename,request.folder,request.file_data,request.create_folder)
      #             #print(replication_response)
      #             return response
      #       except Exception as error:
      #                   response = dataNode_apiGateway_pb2.WriteFileResponseData(write_success=False)
      #                   context.set_code(grpc.StatusCode.INTERNAL)  
      #                   context.set_details(f"Error writing file: {str(error)}")
      #                   return response


      def WriteFile(self, request, context):
            print("Writting ", request.filename)
            if(request.create_folder != ''):
                  #os.makedirs(os.path.dirname(f'{request.folder}/{request.filename}'), exist_ok=True)
                  os.mkdir(f'files/{request.create_folder}')

            try:
                  with open(f'files/{request.folder}/{request.filename}', 'wb') as file:
                        file.write(request.file_data)

                  response = dataNode_apiGateway_pb2.WriteFileResponseData(write_success=True)
                  return response
            except Exception as error:
                  response = dataNode_apiGateway_pb2.WriteFileResponseData(write_success=False)
                  context.set_code(grpc.StatusCode.INTERNAL)
                  context.set_details(f"Error writing file: {str(error)}")
                  return response

      
            


def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[('grpc.max_receive_message_length', 1024 * 1024 * 100)])
        dataNode_apiGateway_pb2_grpc.add_DataNodeServiceServicer_to_server(File(), server)
        server.add_insecure_port(DN2)
        print("DataNode {} is running... ".format(DN2))
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    serve()





      
            
