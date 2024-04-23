# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: response.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='response.proto',
  package='com.nowcoder.ut.idl',
  syntax='proto3',
  serialized_options=b'\n\023com.nowcoder.ut.idlP\000',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0eresponse.proto\x12\x13\x63om.nowcoder.ut.idl\"O\n\x0eRecallResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0b\n\x03ids\x18\x03 \x03(\x05\x12\x11\n\tdistances\x18\x04 \x03(\x02\">\n\rScoreResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06scores\x18\x03 \x03(\x02\"!\n\x0fPredictResponse\x12\x0e\n\x06scores\x18\x01 \x03(\x02\"?\n\x0eVectorResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06vector\x18\x03 \x03(\x02\x42\x17\n\x13\x63om.nowcoder.ut.idlP\x00\x62\x06proto3'
)




_RECALLRESPONSE = _descriptor.Descriptor(
  name='RecallResponse',
  full_name='com.nowcoder.ut.idl.RecallResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='com.nowcoder.ut.idl.RecallResponse.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='com.nowcoder.ut.idl.RecallResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ids', full_name='com.nowcoder.ut.idl.RecallResponse.ids', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='distances', full_name='com.nowcoder.ut.idl.RecallResponse.distances', index=3,
      number=4, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=118,
)


_SCORERESPONSE = _descriptor.Descriptor(
  name='ScoreResponse',
  full_name='com.nowcoder.ut.idl.ScoreResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='com.nowcoder.ut.idl.ScoreResponse.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='com.nowcoder.ut.idl.ScoreResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scores', full_name='com.nowcoder.ut.idl.ScoreResponse.scores', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=182,
)


_PREDICTRESPONSE = _descriptor.Descriptor(
  name='PredictResponse',
  full_name='com.nowcoder.ut.idl.PredictResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scores', full_name='com.nowcoder.ut.idl.PredictResponse.scores', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=217,
)


_VECTORRESPONSE = _descriptor.Descriptor(
  name='VectorResponse',
  full_name='com.nowcoder.ut.idl.VectorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='com.nowcoder.ut.idl.VectorResponse.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='com.nowcoder.ut.idl.VectorResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vector', full_name='com.nowcoder.ut.idl.VectorResponse.vector', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=219,
  serialized_end=282,
)

DESCRIPTOR.message_types_by_name['RecallResponse'] = _RECALLRESPONSE
DESCRIPTOR.message_types_by_name['ScoreResponse'] = _SCORERESPONSE
DESCRIPTOR.message_types_by_name['PredictResponse'] = _PREDICTRESPONSE
DESCRIPTOR.message_types_by_name['VectorResponse'] = _VECTORRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RecallResponse = _reflection.GeneratedProtocolMessageType('RecallResponse', (_message.Message,), {
  'DESCRIPTOR' : _RECALLRESPONSE,
  '__module__' : 'response_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.RecallResponse)
  })
_sym_db.RegisterMessage(RecallResponse)

ScoreResponse = _reflection.GeneratedProtocolMessageType('ScoreResponse', (_message.Message,), {
  'DESCRIPTOR' : _SCORERESPONSE,
  '__module__' : 'response_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.ScoreResponse)
  })
_sym_db.RegisterMessage(ScoreResponse)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTRESPONSE,
  '__module__' : 'response_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.PredictResponse)
  })
_sym_db.RegisterMessage(PredictResponse)

VectorResponse = _reflection.GeneratedProtocolMessageType('VectorResponse', (_message.Message,), {
  'DESCRIPTOR' : _VECTORRESPONSE,
  '__module__' : 'response_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.VectorResponse)
  })
_sym_db.RegisterMessage(VectorResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
