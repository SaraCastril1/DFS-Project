from flask import Flask, request, Response
from flask_cors import CORS
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
    print("Voy a establecer conexión con {}:{}".format(PRODUCER_HOST, data_node_address))
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
        data_node_addresses = get_data_node_addresses(filename)
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

def writeFile(filename,folder,file_data,create_folder, data_node_port):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{data_node_port}",options=[
        ('grpc.max_receive_message_length', 1024 * 1024 * 100)  
    ]) as channel:
            stub = apiGateway_dataNode_pb2_grpc.DataNodeServiceStub(channel)
            response = stub.WriteFile(apiGateway_dataNode_pb2.WriteFileRequestData(file_data=file_data,filename=filename,folder=folder,create_folder=create_folder))
            return response
    except Exception as error:
        print(error)


@app.route('/writefile', methods=['POST'])
def writefile_route():

    folder = request.form.get('folder')
    filename = request.files['file_data'].filename
    file_data = request.files['file_data'].read() 
    create_folder = request.form.get('create_folder')

    data_node_response = writeFile(filename,folder,file_data,create_folder)
    return {'succes':data_node_response.write_success}

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
