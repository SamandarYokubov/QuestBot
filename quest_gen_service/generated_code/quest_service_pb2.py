# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: quest_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13quest_service.proto\"s\n\x07Request\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x13\n\x0b\x63ourse_name\x18\x02 \x01(\t\x12\x15\n\rcourse_module\x18\x03 \x01(\x05\x12\x15\n\rquestion_type\x18\x04 \x01(\t\x12\x14\n\x0c\x63ontent_type\x18\x05 \x01(\t\"\x1d\n\x08Response\x12\x11\n\tquestions\x18\x01 \x01(\t26\n\x0cQuestService\x12&\n\rget_questions\x12\x08.Request\x1a\t.Response\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'quest_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUEST']._serialized_start=23
  _globals['_REQUEST']._serialized_end=138
  _globals['_RESPONSE']._serialized_start=140
  _globals['_RESPONSE']._serialized_end=169
  _globals['_QUESTSERVICE']._serialized_start=171
  _globals['_QUESTSERVICE']._serialized_end=225
# @@protoc_insertion_point(module_scope)
