# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: resume_history.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14resume_history.proto\x12\x13\x63om.nowcoder.ut.idl\"\\\n\rresume_action\x12\x11\n\tresume_id\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x0f\n\x07pit_var\x18\x03 \x01(\x05\x12\x14\n\x0c\x63\x61ndidate_id\x18\x04 \x01(\t\"B\n\x0eresume_history\x12\x30\n\x04list\x18\x01 \x03(\x0b\x32\".com.nowcoder.ut.idl.resume_actionB\x17\n\x13\x63om.nowcoder.ut.idlP\x00\x62\x06proto3')



_RESUME_ACTION = DESCRIPTOR.message_types_by_name['resume_action']
_RESUME_HISTORY = DESCRIPTOR.message_types_by_name['resume_history']
resume_action = _reflection.GeneratedProtocolMessageType('resume_action', (_message.Message,), {
  'DESCRIPTOR' : _RESUME_ACTION,
  '__module__' : 'resume_history_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.resume_action)
  })
_sym_db.RegisterMessage(resume_action)

resume_history = _reflection.GeneratedProtocolMessageType('resume_history', (_message.Message,), {
  'DESCRIPTOR' : _RESUME_HISTORY,
  '__module__' : 'resume_history_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.resume_history)
  })
_sym_db.RegisterMessage(resume_history)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023com.nowcoder.ut.idlP\000'
  _RESUME_ACTION._serialized_start=45
  _RESUME_ACTION._serialized_end=137
  _RESUME_HISTORY._serialized_start=139
  _RESUME_HISTORY._serialized_end=205
# @@protoc_insertion_point(module_scope)
