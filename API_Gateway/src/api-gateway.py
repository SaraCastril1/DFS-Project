from flask import Flask
import os
from dotenv import dotenv_values
import grpc
import file_pb2
import file_pb2_grpc


app = Flask(__name__)
config = dotenv_values("../.env")

PRODUCER_HOST = config['PRODUCER_HOST']
PRODUCER_PORT = config['PRODUCER_PORT']


def find_file(pattern):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = file_pb2_grpc.FileStub(channel)
            response = stub.Find_file(file_pb2.file_request(file=pattern))
            return response
    except:
        print("ERROR")



def list_files(directory):
    try:
        with grpc.insecure_channel(f"{PRODUCER_HOST}:{PRODUCER_PORT}") as channel:
            stub = file_pb2_grpc.FileStub(channel)
            response = stub.List_file(file_pb2.file_request(file=directory))
            return response.file
    except:
        print("ERROR")


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