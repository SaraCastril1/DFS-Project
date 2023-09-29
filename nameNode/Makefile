.PHONY = pb2
SHELL := /bin/bash

nameNode:
	python3 -m grpc_tools.protoc -I ./protobufs --python_out=./src --pyi_out=./src --grpc_python_out=./src ./protobufs/apiGateway-nameNode.proto