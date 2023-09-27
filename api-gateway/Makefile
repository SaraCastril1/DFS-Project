.PHONY = pb2
SHELL := /bin/bash

client:
	pip3 install grpcio grpcio-tools
	pip install Flask
	pip install pika

	python -m grpc_tools.protoc -I ./protobufs --python_out=./src --pyi_out=./src --grpc_python_out=./src ./protobufs/apiGateway_nameNode.proto