from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from google.protobuf.json_format import MessageToJson
import os
from dotenv import dotenv_values
import grpc
import apiGateway_nameNode_pb2_grpc
import apiGateway_nameNode_pb2
import apiGateway_dataNode_pb2
import apiGateway_dataNode_pb2_grpc

app = Flask(__name__)
CORS(app)
config = dotenv_values(".env")

PRODUCER_HOST = config['PRODUCER_HOST']
PRODUCER_PORT = config['PRODUCER_PORT']


#ROUNDROBIN
current_data_node_index = 0
data_node_addresses = ["50052", "6000", "6500"]

#ROUNDROBIN
def get_next_data_node_address():
    global current_data_node_index
    address = data_node_addresses[current_data_node_index]
    current_data_node_index = (current_data_node_index + 1) % len(data_node_addresses)
    return address


 #READ FILE!!!!!------------------------------------------------------------------------
def get_data_node_addresses(filename):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = apiGateway_nameNode_pb2_grpc.NameNodeServiceStub(channel)
            response = stub.ReadFile(apiGateway_nameNode_pb2.ReadFileRequest(filename=filename))
            print("Addresses: ", response.data_node_addresses)
            return response.data_node_addresses
    except Exception as error:
        print(f"Error al obtener la dirección del DataNode: {error}")
        return None


def get_file_from_data_node(data_node_address, filename):
    print("Connected with: {}:{}".format(PRODUCER_HOST, data_node_address))
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{data_node_address}", options=[
            ('grpc.max_receive_message_length', 1024 * 1024 * 100)
        ]) as channel:
            stub = apiGateway_dataNode_pb2_grpc.DataNodeServiceStub(channel)
            # Envía una solicitud para leer el archivo al DataNode
            response = stub.ReadFile(apiGateway_dataNode_pb2.ReadFileRequestData(file_name=filename))
            return response.file_data
    except Exception as error:
        print(f"Error al recuperar el archivo del DataNode: {error}")
        return None



@app.route('/readfile', methods=['POST'])
def readfile_route():
    try:
        filename = request.json['file']
        print(filename)
        data_node_addresses = get_data_node_addresses(filename)
        print(data_node_addresses)
        print("El archivo solicitado está en las siguientes direcciones de DataNodes:", data_node_addresses)

        if not data_node_addresses:
            return Response('No se pudieron obtener las direcciones de los DataNodes', status=500, content_type='application/json')

        my_dataNode = get_next_data_node_address()
        file_data = get_file_from_data_node(data_node_addresses[0], filename)

        if not file_data:
            return Response('Archivo no encontrado en los DataNodes', status=404, content_type='application/json')

        return Response(file_data, content_type='application/octet-stream')

    except Exception as error:
        print(f"Error en la solicitud: {error}")
        return Response('Error en la solicitud', status=500, content_type='application/json')



# TO DO: WRITE FILE!!!!!------------------------------------------------------------------------

def write_file_to_data_node(data_node_address, filename, folder, file_data, create_folder):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{data_node_address}", options=[
            ('grpc.max_receive_message_length', 1024 * 1024 * 100)
        ]) as channel:
            stub = apiGateway_dataNode_pb2_grpc.DataNodeServiceStub(channel)
            # Obtener la ruta completa del archivo un nivel arriba del directorio actual
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", folder, filename)

            request = apiGateway_dataNode_pb2.WriteFileRequestData(
                folder=folder,
                filename=filename,
                file_data=file_data,
                create_folder=create_folder,
                file_path=file_path  # Pasar la ruta completa del archivo al DataNode
            )
            response = stub.WriteFile(request)
            # Verificar si la escritura fue exitosa
            if hasattr(response, 'write_success') and response.write_success:
                return True
            else:
                return False
    except Exception as error:
        print(f"Error on writting to the DataNode {data_node_address} : {error}")
        return None



def add_file_to_name_node(filename, folder, data_node_address):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = apiGateway_nameNode_pb2_grpc.NameNodeServiceStub(channel)
            request = apiGateway_nameNode_pb2.AddFileRequest(
                filename=filename,
                folder=folder,
                data_node_address=data_node_address
            )
            response = stub.AddFile(request)
            return response.success
    except Exception as error:
        print(f"Error al agregar el archivo al NameNode: {error}")
        return False



@app.route('/writefile', methods=['POST'])
def writefile_route():
    try:
        folder = request.form.get('folder')
        filename = request.files['file_data'].filename
        file_data = request.files['file_data'].read() 
        create_folder = request.form.get('create_folder')

        print("Received file:", filename, "in folder:", folder)
        print(file_data)

        my_dataNode = get_next_data_node_address()  # Get DataNode addresses from NameNode
        print("Data will be sent to: ", my_dataNode)

        data_node_response = write_file_to_data_node(my_dataNode, filename, folder, file_data, create_folder)

        if data_node_response:
            # Archivo escrito exitosamente, ahora agregar a la tabla y al archivo de registro (log)
            add_file_to_name_node(filename, folder, my_dataNode)
            response_data = {"message": "File written successfully"}
            return jsonify(response_data), 200

        else:
                return Response('Error al escribir el archivo en el DataNode', status=500, content_type='application/json')

    except Exception as error:
        print(f"Error en la solicitud: {error}")
        return Response('Error en la solicitud', status=500, content_type='application/json')



# LIST-------------------------------------------------------------------
def list_files_from_name_node():
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = apiGateway_nameNode_pb2_grpc.NameNodeServiceStub(channel)
            request = apiGateway_nameNode_pb2.ListFilesRequest()
            response = stub.ListFiles(request)
            #print (response.filenames)
            return response.filenames
    except Exception as error:
        app.logger.error(f"Error al listar archivos desde el NameNode: {error}")
        return []

@app.route('/listfiles', methods=['GET'])
def listfiles_route():
    try:
        files = list_files_from_name_node()
        print(files, type(files))
        files_list = list(files)
        print(files_list, type(files_list))
        return jsonify({"files": files_list})

    except Exception as error:
        return Response(f'Error en la solicitud: {error}', status=500, content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
