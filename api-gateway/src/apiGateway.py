from    flask import Flask, request
import  os
from    dotenv import dotenv_values
import  grpc
import  apiGateway_nameNode_pb2_grpc
import  apiGateway_nameNode_pb2
import  apiGateway_dataNode_pb2
import  apiGateway_dataNode_pb2_grpc

app = Flask(__name__)
config = dotenv_values(".env")

PRODUCER_HOST = config['PRODUCER_HOST']
PRODUCER_PORT = config['PRODUCER_PORT']
DATA_NODE_PORT = config['DATA_NODE_PORT']


def find_file(pattern):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = apiGateway_nameNode_pb2_grpc.FileStub(channel)
            response = stub.Find_file(apiGateway_nameNode_pb2.file_request(file=pattern))
            return response
    except:
        print("ERROR")



def list_files(directory):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = apiGateway_nameNode_pb2_grpc.FileStub(channel)
            response = stub.List_file(apiGateway_nameNode_pb2.file_request(file=directory))
            return response.file
    except:
        print("ERROR")

def readFile(file_name):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{DATA_NODE_PORT}") as channel:
            stub = apiGateway_dataNode_pb2_grpc.DataNodeServiceStub(channel)
            response = stub.ReadFile(apiGateway_dataNode_pb2.ReadFileRequestData(file_name=file_name))
            print(response)
    except Exception as error:
        print(error)

@app.route('/readfile', methods=['POST'])
def readfile_route():
    filename = request.json['file']
    print(filename)
    response = readFile(filename)
    return("helloworld")


@app.route('/find/<pattern>', methods=['GET'])
def find_route(pattern):
    response = find_file(pattern)
    return f"Find result: {response.file}, {response.coincidence}"

@app.route('/list/<directory>', methods=['GET'])
def list_route(directory):
    #my_path = os.path.join("/", directory)
    response = list_files(directory)
    
    if response is not None:
        return f"List result: {response}"  
    else:
        return "List result: No files found"
    




if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')