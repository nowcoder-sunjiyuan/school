# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: comment_predict.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from dto import common_pb2 as dto_dot_common__pb2

from dto.common_pb2 import *

DESCRIPTOR = _descriptor.FileDescriptor(
  name='comment_predict.proto',
  package='com.nowcoder.ut.idl',
  syntax='proto3',
  serialized_options=b'\n\023com.nowcoder.ut.idlP\000',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15\x63omment_predict.proto\x12\x13\x63om.nowcoder.ut.idl\x1a\x10\x64to/common.proto\"\xbd\x03\n\x19\x43ommentPredictUserFeature\x12\x15\n\rbe_interested\x18\x01 \x01(\t\x12\x11\n\tclock_day\x18\x02 \x01(\x05\x12\x18\n\x10\x63ompany_overtime\x18\x03 \x01(\x05\x12\x1c\n\x14\x63omplete_career_info\x18\x04 \x01(\x05\x12\x11\n\tedu_level\x18\x05 \x01(\t\x12\x16\n\x0e\x66ollow_circles\x18\x06 \x01(\t\x12\x0e\n\x06gender\x18\x07 \x01(\t\x12\x13\n\x0bhonor_level\x18\x08 \x01(\x05\x12\x13\n\x0bhonor_score\x18\t \x01(\x02\x12\x0b\n\x03job\x18\n \x01(\t\x12\x12\n\nlogin_type\x18\x0b \x01(\x05\x12\x17\n\x0fregister_client\x18\x0c \x01(\x05\x12\x14\n\x0cschool_major\x18\r \x01(\t\x12\x15\n\rtest_keep_day\x18\x0e \x01(\x05\x12\x11\n\twork_info\x18\x0f \x01(\t\x12\x1a\n\x12work_status_detail\x18\x10 \x01(\x05\x12\x11\n\twork_time\x18\x11 \x01(\x05\x12\x17\n\x0fyear_salary_max\x18\x12 \x01(\x03\x12\x17\n\x0fyear_salary_min\x18\x13 \x01(\x03\".\n\x19\x43ommentPredictItemFeature\x12\x11\n\tentity_id\x18\x01 \x01(\x03\"\xc7\x01\n\x15\x43ommentPredictRequest\x12<\n\x04user\x18\x01 \x01(\x0b\x32..com.nowcoder.ut.idl.CommentPredictUserFeature\x12<\n\x04item\x18\x02 \x03(\x0b\x32..com.nowcoder.ut.idl.CommentPredictItemFeature\x12\x32\n\ndebug_info\x18\x03 \x01(\x0b\x32\x1e.com.nowcoder.ut.idl.DebugInfo\"\\\n\x16\x43ommentPredictResponse\x12\x0e\n\x06scores\x18\x01 \x03(\x02\x12\x32\n\ndebug_info\x18\x02 \x01(\x0b\x32\x1e.com.nowcoder.ut.idl.DebugInfoB\x17\n\x13\x63om.nowcoder.ut.idlP\x00P\x00\x62\x06proto3'
  ,
  dependencies=[dto_dot_common__pb2.DESCRIPTOR,],
  public_dependencies=[dto_dot_common__pb2.DESCRIPTOR,])




_COMMENTPREDICTUSERFEATURE = _descriptor.Descriptor(
  name='CommentPredictUserFeature',
  full_name='com.nowcoder.ut.idl.CommentPredictUserFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='be_interested', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.be_interested', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clock_day', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.clock_day', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='company_overtime', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.company_overtime', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='complete_career_info', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.complete_career_info', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='edu_level', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.edu_level', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='follow_circles', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.follow_circles', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gender', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.gender', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='honor_level', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.honor_level', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='honor_score', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.honor_score', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='job', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.job', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='login_type', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.login_type', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='register_client', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.register_client', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='school_major', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.school_major', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_keep_day', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.test_keep_day', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_info', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.work_info', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_status_detail', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.work_status_detail', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_time', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.work_time', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='year_salary_max', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.year_salary_max', index=17,
      number=18, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='year_salary_min', full_name='com.nowcoder.ut.idl.CommentPredictUserFeature.year_salary_min', index=18,
      number=19, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=65,
  serialized_end=510,
)


_COMMENTPREDICTITEMFEATURE = _descriptor.Descriptor(
  name='CommentPredictItemFeature',
  full_name='com.nowcoder.ut.idl.CommentPredictItemFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity_id', full_name='com.nowcoder.ut.idl.CommentPredictItemFeature.entity_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=512,
  serialized_end=558,
)


_COMMENTPREDICTREQUEST = _descriptor.Descriptor(
  name='CommentPredictRequest',
  full_name='com.nowcoder.ut.idl.CommentPredictRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user', full_name='com.nowcoder.ut.idl.CommentPredictRequest.user', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='item', full_name='com.nowcoder.ut.idl.CommentPredictRequest.item', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='debug_info', full_name='com.nowcoder.ut.idl.CommentPredictRequest.debug_info', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=561,
  serialized_end=760,
)


_COMMENTPREDICTRESPONSE = _descriptor.Descriptor(
  name='CommentPredictResponse',
  full_name='com.nowcoder.ut.idl.CommentPredictResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scores', full_name='com.nowcoder.ut.idl.CommentPredictResponse.scores', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='debug_info', full_name='com.nowcoder.ut.idl.CommentPredictResponse.debug_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=762,
  serialized_end=854,
)

_COMMENTPREDICTREQUEST.fields_by_name['user'].message_type = _COMMENTPREDICTUSERFEATURE
_COMMENTPREDICTREQUEST.fields_by_name['item'].message_type = _COMMENTPREDICTITEMFEATURE
_COMMENTPREDICTREQUEST.fields_by_name['debug_info'].message_type = dto_dot_common__pb2._DEBUGINFO
_COMMENTPREDICTRESPONSE.fields_by_name['debug_info'].message_type = dto_dot_common__pb2._DEBUGINFO
DESCRIPTOR.message_types_by_name['CommentPredictUserFeature'] = _COMMENTPREDICTUSERFEATURE
DESCRIPTOR.message_types_by_name['CommentPredictItemFeature'] = _COMMENTPREDICTITEMFEATURE
DESCRIPTOR.message_types_by_name['CommentPredictRequest'] = _COMMENTPREDICTREQUEST
DESCRIPTOR.message_types_by_name['CommentPredictResponse'] = _COMMENTPREDICTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CommentPredictUserFeature = _reflection.GeneratedProtocolMessageType('CommentPredictUserFeature', (_message.Message,), {
  'DESCRIPTOR' : _COMMENTPREDICTUSERFEATURE,
  '__module__' : 'comment_predict_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.CommentPredictUserFeature)
  })
_sym_db.RegisterMessage(CommentPredictUserFeature)

CommentPredictItemFeature = _reflection.GeneratedProtocolMessageType('CommentPredictItemFeature', (_message.Message,), {
  'DESCRIPTOR' : _COMMENTPREDICTITEMFEATURE,
  '__module__' : 'comment_predict_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.CommentPredictItemFeature)
  })
_sym_db.RegisterMessage(CommentPredictItemFeature)

CommentPredictRequest = _reflection.GeneratedProtocolMessageType('CommentPredictRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMMENTPREDICTREQUEST,
  '__module__' : 'comment_predict_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.CommentPredictRequest)
  })
_sym_db.RegisterMessage(CommentPredictRequest)

CommentPredictResponse = _reflection.GeneratedProtocolMessageType('CommentPredictResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMENTPREDICTRESPONSE,
  '__module__' : 'comment_predict_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.CommentPredictResponse)
  })
_sym_db.RegisterMessage(CommentPredictResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)