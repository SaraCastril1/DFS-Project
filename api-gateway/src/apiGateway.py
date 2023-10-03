from    flask import Flask, request, Response, send_file
from flask_cors import CORS
import  os
from    dotenv import dotenv_values
import  grpc
import  apiGateway_nameNode_pb2_grpc
import  apiGateway_nameNode_pb2
import  apiGateway_dataNode_pb2
import  apiGateway_dataNode_pb2_grpc

app = Flask(__name__)
CORS(app)
config = dotenv_values(".env")

PRODUCER_HOST = config['PRODUCER_HOST']
PRODUCER_PORT = config['PRODUCER_PORT']
DATA_NODE_PORT = config['DATA_NODE_PORT']


def readFile(filename):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{DATA_NODE_PORT}",options=[
        ('grpc.max_receive_message_length', 1024 * 1024 * 100)  
    ]) as channel:
            stub = apiGateway_dataNode_pb2_grpc.DataNodeServiceStub(channel)
            response = stub.ReadFile(apiGateway_dataNode_pb2.ReadFileRequestData(file_name=filename))
            return response
    except Exception as error:
        print(error)

def writeFile(filename,folder,file_data,create_folder):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{DATA_NODE_PORT}",options=[
        ('grpc.max_receive_message_length', 1024 * 1024 * 100)  
    ]) as channel:
            stub = apiGateway_dataNode_pb2_grpc.DataNodeServiceStub(channel)
            response = stub.WriteFile(apiGateway_dataNode_pb2.WriteFileRequestData(file_data=file_data,filename=filename,folder=folder,create_folder=create_folder))
            return response
    except Exception as error:
        print(error)


@app.route('/readfile', methods=['POST'])
def readfile_route():
    filename = request.json['file']
    
    file = readFile(filename)
    if not file:
        return Response('Archivo no encontrado',status=404, content_type='application/json')
    return Response(file.file_data,content_type='application/octet-stream')


#TO DO: WRITE FILE!!!!!
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

    