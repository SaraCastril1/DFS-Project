from flask import Flask, request, Response, send_file
from flask_cors import CORS
import os
from dotenv import dotenv_values
import grpc
import apiGateway_nameNode_pb2_grpc
import apiGateway_nameNode_pb2
import  apiGateway_dataNode_pb2
import  apiGateway_dataNode_pb2_grpc

app = Flask(__name__)
CORS(app)
config = dotenv_values(".env")

PRODUCER_HOST = config['PRODUCER_HOST']
PRODUCER_PORT = config['PRODUCER_PORT']
dn1 = config['DATA_NODE_PORT-1']

def get_data_node_address(filename):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{50051}") as channel:
            stub = apiGateway_nameNode_pb2_grpc.NameNodeServiceStub(channel)
            response = stub.ReadFile(apiGateway_nameNode_pb2.ReadFileRequest(filename=filename))
            return response.data_node_addresses[0]
    except Exception as error:
        print(f"Error al obtener la dirección del DataNode: {error}")
        return None


def get_file_from_data_node(data_node_address, filename):
    print("Voy a establecer conexión con {}:{}".format(PRODUCER_HOST,data_node_address))
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{data_node_address}",options=[
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
        data_node_address = get_data_node_address(filename)
        print("El archivo solicitado está en: {}".format(data_node_address))

        if not data_node_address:
            return Response('No se pudo obtener la dirección del DataNode', status=500, content_type='application/json')

         # Inicia la conexión con el DataNode y solicita el archivo
        file_data = get_file_from_data_node(data_node_address, filename)

        if not file_data:
            return Response('Archivo no encontrado', status=404, content_type='application/json')

        return Response(file_data, content_type='application/octet-stream')


    except Exception as error:
        print(f"Error en la solicitud: {error}")
        return Response('Error en la solicitud', status=500, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
