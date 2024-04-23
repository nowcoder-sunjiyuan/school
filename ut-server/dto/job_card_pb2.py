# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: job_card.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='job_card.proto',
  package='com.nowcoder.ut.idl',
  syntax='proto3',
  serialized_options=b'\n\023com.nowcoder.ut.idlP\000',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0ejob_card.proto\x12\x13\x63om.nowcoder.ut.idl\"\xb7\x02\n\x12JobCardUserFeature\x12\x0e\n\x06gender\x18\x01 \x01(\t\x12\x13\n\x0bschool_type\x18\x02 \x01(\t\x12\x11\n\tedu_level\x18\x03 \x01(\t\x12\x13\n\x0bhonor_level\x18\x04 \x01(\t\x12\x17\n\x0fwork_want_place\x18\x05 \x03(\t\x12\x1b\n\x13work_want_place_len\x18\x06 \x01(\x03\x12\x17\n\x0f\x63\x61reer_job_id_1\x18\x07 \x01(\t\x12\x17\n\x0f\x63\x61reer_job_id_2\x18\x08 \x01(\t\x12\x17\n\x0f\x63\x61reer_job_id_3\x18\t \x01(\t\x12\x0f\n\x07user_id\x18\n \x01(\t\x12\x14\n\x0cschool_major\x18\x0b \x01(\t\x12\x13\n\x0bhist_job_id\x18\x0c \x03(\t\x12\x17\n\x0fhist_job_id_len\x18\r \x01(\x03\"\x9f\x03\n\x11JobCardJobFeature\x12\x0e\n\x06job_id\x18\x01 \x01(\t\x12\x12\n\ncompany_id\x18\x02 \x01(\t\x12\x16\n\x0e\x64\x61y_salary_min\x18\x03 \x01(\x03\x12\x16\n\x0e\x64\x61y_salary_max\x18\x04 \x01(\x03\x12\x13\n\x0bi_edu_level\x18\x05 \x01(\t\x12\x10\n\x08job_city\x18\x06 \x03(\t\x12\x14\n\x0cjob_city_len\x18\x07 \x01(\x03\x12\x15\n\rcareer_job_id\x18\x08 \x01(\t\x12\x14\n\x0crecruit_type\x18\t \x01(\t\x12\x15\n\rprocess_count\x18\n \x01(\x03\x12\x1b\n\x13latest_process_time\x18\x0b \x01(\x03\x12\x18\n\x10\x61vg_process_rate\x18\x0c \x01(\x03\x12\x17\n\x0f\x61vg_process_sec\x18\r \x01(\x03\x12\x13\n\x0b\x66rom_create\x18\x0e \x01(\x02\x12\x1e\n\x16initiative_deliver_cnt\x18\x0f \x01(\x03\x12\x1a\n\x12invite_success_cnt\x18\x10 \x01(\x03\x12\x14\n\x0c\x63ompany_size\x18\x11 \x01(\t\"\x8c\x01\n\x0eJobCardRequest\x12=\n\x0cuser_feature\x18\x01 \x01(\x0b\x32\'.com.nowcoder.ut.idl.JobCardUserFeature\x12;\n\x0bjob_feature\x18\x02 \x03(\x0b\x32&.com.nowcoder.ut.idl.JobCardJobFeature\"!\n\x0fJobCardResponse\x12\x0e\n\x06scores\x18\x01 \x03(\x02\x42\x17\n\x13\x63om.nowcoder.ut.idlP\x00\x62\x06proto3'
)




_JOBCARDUSERFEATURE = _descriptor.Descriptor(
  name='JobCardUserFeature',
  full_name='com.nowcoder.ut.idl.JobCardUserFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='gender', full_name='com.nowcoder.ut.idl.JobCardUserFeature.gender', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='school_type', full_name='com.nowcoder.ut.idl.JobCardUserFeature.school_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='edu_level', full_name='com.nowcoder.ut.idl.JobCardUserFeature.edu_level', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='honor_level', full_name='com.nowcoder.ut.idl.JobCardUserFeature.honor_level', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_want_place', full_name='com.nowcoder.ut.idl.JobCardUserFeature.work_want_place', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_want_place_len', full_name='com.nowcoder.ut.idl.JobCardUserFeature.work_want_place_len', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job_id_1', full_name='com.nowcoder.ut.idl.JobCardUserFeature.career_job_id_1', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job_id_2', full_name='com.nowcoder.ut.idl.JobCardUserFeature.career_job_id_2', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job_id_3', full_name='com.nowcoder.ut.idl.JobCardUserFeature.career_job_id_3', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='com.nowcoder.ut.idl.JobCardUserFeature.user_id', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='school_major', full_name='com.nowcoder.ut.idl.JobCardUserFeature.school_major', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hist_job_id', full_name='com.nowcoder.ut.idl.JobCardUserFeature.hist_job_id', index=11,
      number=12, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hist_job_id_len', full_name='com.nowcoder.ut.idl.JobCardUserFeature.hist_job_id_len', index=12,
      number=13, type=3, cpp_type=2, label=1,
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
  serialized_start=40,
  serialized_end=351,
)


_JOBCARDJOBFEATURE = _descriptor.Descriptor(
  name='JobCardJobFeature',
  full_name='com.nowcoder.ut.idl.JobCardJobFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='job_id', full_name='com.nowcoder.ut.idl.JobCardJobFeature.job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='company_id', full_name='com.nowcoder.ut.idl.JobCardJobFeature.company_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='day_salary_min', full_name='com.nowcoder.ut.idl.JobCardJobFeature.day_salary_min', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='day_salary_max', full_name='com.nowcoder.ut.idl.JobCardJobFeature.day_salary_max', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='i_edu_level', full_name='com.nowcoder.ut.idl.JobCardJobFeature.i_edu_level', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='job_city', full_name='com.nowcoder.ut.idl.JobCardJobFeature.job_city', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='job_city_len', full_name='com.nowcoder.ut.idl.JobCardJobFeature.job_city_len', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job_id', full_name='com.nowcoder.ut.idl.JobCardJobFeature.career_job_id', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recruit_type', full_name='com.nowcoder.ut.idl.JobCardJobFeature.recruit_type', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='process_count', full_name='com.nowcoder.ut.idl.JobCardJobFeature.process_count', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='latest_process_time', full_name='com.nowcoder.ut.idl.JobCardJobFeature.latest_process_time', index=10,
      number=11, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='avg_process_rate', full_name='com.nowcoder.ut.idl.JobCardJobFeature.avg_process_rate', index=11,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='avg_process_sec', full_name='com.nowcoder.ut.idl.JobCardJobFeature.avg_process_sec', index=12,
      number=13, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='from_create', full_name='com.nowcoder.ut.idl.JobCardJobFeature.from_create', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='initiative_deliver_cnt', full_name='com.nowcoder.ut.idl.JobCardJobFeature.initiative_deliver_cnt', index=14,
      number=15, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='invite_success_cnt', full_name='com.nowcoder.ut.idl.JobCardJobFeature.invite_success_cnt', index=15,
      number=16, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='company_size', full_name='com.nowcoder.ut.idl.JobCardJobFeature.company_size', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=354,
  serialized_end=769,
)


_JOBCARDREQUEST = _descriptor.Descriptor(
  name='JobCardRequest',
  full_name='com.nowcoder.ut.idl.JobCardRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_feature', full_name='com.nowcoder.ut.idl.JobCardRequest.user_feature', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='job_feature', full_name='com.nowcoder.ut.idl.JobCardRequest.job_feature', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=772,
  serialized_end=912,
)


_JOBCARDRESPONSE = _descriptor.Descriptor(
  name='JobCardResponse',
  full_name='com.nowcoder.ut.idl.JobCardResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scores', full_name='com.nowcoder.ut.idl.JobCardResponse.scores', index=0,
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
  serialized_start=914,
  serialized_end=947,
)

_JOBCARDREQUEST.fields_by_name['user_feature'].message_type = _JOBCARDUSERFEATURE
_JOBCARDREQUEST.fields_by_name['job_feature'].message_type = _JOBCARDJOBFEATURE
DESCRIPTOR.message_types_by_name['JobCardUserFeature'] = _JOBCARDUSERFEATURE
DESCRIPTOR.message_types_by_name['JobCardJobFeature'] = _JOBCARDJOBFEATURE
DESCRIPTOR.message_types_by_name['JobCardRequest'] = _JOBCARDREQUEST
DESCRIPTOR.message_types_by_name['JobCardResponse'] = _JOBCARDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JobCardUserFeature = _reflection.GeneratedProtocolMessageType('JobCardUserFeature', (_message.Message,), {
  'DESCRIPTOR' : _JOBCARDUSERFEATURE,
  '__module__' : 'job_card_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.JobCardUserFeature)
  })
_sym_db.RegisterMessage(JobCardUserFeature)

JobCardJobFeature = _reflection.GeneratedProtocolMessageType('JobCardJobFeature', (_message.Message,), {
  'DESCRIPTOR' : _JOBCARDJOBFEATURE,
  '__module__' : 'job_card_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.JobCardJobFeature)
  })
_sym_db.RegisterMessage(JobCardJobFeature)

JobCardRequest = _reflection.GeneratedProtocolMessageType('JobCardRequest', (_message.Message,), {
  'DESCRIPTOR' : _JOBCARDREQUEST,
  '__module__' : 'job_card_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.JobCardRequest)
  })
_sym_db.RegisterMessage(JobCardRequest)

JobCardResponse = _reflection.GeneratedProtocolMessageType('JobCardResponse', (_message.Message,), {
  'DESCRIPTOR' : _JOBCARDRESPONSE,
  '__module__' : 'job_card_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.JobCardResponse)
  })
_sym_db.RegisterMessage(JobCardResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
