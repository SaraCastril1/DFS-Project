# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: apiGateway.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x61piGateway.proto\"(\n\x13ReadFileRequestData\x12\x11\n\tfile_name\x18\x01 \x01(\t\")\n\x14ReadFileResponseData\x12\x11\n\tfile_data\x18\x01 \x01(\x0c\x32L\n\x11\x41piGatewayService\x12\x37\n\x08ReadFile\x12\x14.ReadFileRequestData\x1a\x15.ReadFileResponseDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'apiGateway_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_READFILEREQUESTDATA']._serialized_start=20
  _globals['_READFILEREQUESTDATA']._serialized_end=60
  _globals['_READFILERESPONSEDATA']._serialized_start=62
  _globals['_READFILERESPONSEDATA']._serialized_end=103
  _globals['_APIGATEWAYSERVICE']._serialized_start=105
  _globals['_APIGATEWAYSERVICE']._serialized_end=181
# @@protoc_insertion_point(module_scope)