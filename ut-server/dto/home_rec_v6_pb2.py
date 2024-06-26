# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: home_rec_v6.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='home_rec_v6.proto',
  package='com.nowcoder.ut.idl',
  syntax='proto3',
  serialized_options=b'\n\023com.nowcoder.ut.idlP\000',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11home_rec_v6.proto\x12\x13\x63om.nowcoder.ut.idl\"\xde\x02\n\x15HomeRankV6UserFeature\x12\x11\n\twork_info\x18\x01 \x01(\t\x12\x0e\n\x06school\x18\x02 \x01(\t\x12\x0e\n\x06gender\x18\x03 \x01(\t\x12\x17\n\x0f\x65\x64u_work_status\x18\x04 \x01(\t\x12\x15\n\rcareer_job1_1\x18\x05 \x01(\t\x12\x15\n\rcareer_job1_2\x18\x06 \x01(\t\x12\x15\n\rcareer_job1_3\x18\x07 \x01(\t\x12\x11\n\tedu_level\x18\x08 \x01(\t\x12\x11\n\twork_year\x18\t \x01(\t\x12\x1a\n\x12work_status_detail\x18\n \x01(\t\x12\x14\n\x0cschool_major\x18\x0b \x01(\t\x12\x13\n\x0bschool_type\x18\x0c \x01(\t\x12\x16\n\x0ehist_entity_id\x18\r \x03(\t\x12\x11\n\thist_type\x18\x0e \x03(\t\x12\x0f\n\x07max_len\x18\x0f \x01(\x05\x12\x0b\n\x03uid\x18\x10 \x01(\t\"\x96\x04\n\x15HomeRankV6ItemFeature\x12\x16\n\x0epostmodule_var\x18\x01 \x01(\t\x12\x18\n\x10\x63ontenttopic_var\x18\x02 \x01(\t\x12\x16\n\x0elikenumber_var\x18\x03 \x01(\x05\x12\x16\n\x0eviewnumber_var\x18\x04 \x01(\x05\x12\x17\n\x0freplynumber_var\x18\x05 \x01(\x05\x12\x16\n\x0e\x63irclename_var\x18\x06 \x01(\t\x12\x17\n\x0f\x63ontentmode_var\x18\x07 \x01(\t\x12\x0c\n\x04type\x18\x08 \x01(\t\x12\x10\n\x08ge_score\x18\t \x01(\x02\x12\x10\n\x08wv_score\x18\n \x01(\x02\x12\x0b\n\x03\x63tr\x18\x0b \x01(\x02\x12\x11\n\tentity_id\x18\x0c \x01(\t\x12\x18\n\x10\x61uthor_work_info\x18\r \x01(\t\x12\x15\n\rauthor_school\x18\x0e \x01(\t\x12\x1c\n\x14\x61uthor_career_job1_1\x18\x0f \x01(\t\x12\x18\n\x10\x61uthor_edu_level\x18\x10 \x01(\t\x12\x1b\n\x13\x61uthor_school_major\x18\x11 \x01(\t\x12\x1a\n\x12\x61uthor_school_type\x18\x12 \x01(\t\x12\x12\n\nauthor_uid\x18\x13 \x01(\t\x12\x11\n\ttaxonomy1\x18\x14 \x01(\t\x12\x11\n\ttaxonomy2\x18\x15 \x01(\t\x12\x0c\n\x04\x66orm\x18\x16 \x01(\t\x12\x15\n\rquality_human\x18\x17 \x01(\t\"\x97\x01\n\x11HomeRankV6Request\x12@\n\x0cuser_feature\x18\x01 \x01(\x0b\x32*.com.nowcoder.ut.idl.HomeRankV6UserFeature\x12@\n\x0citem_feature\x18\x02 \x03(\x0b\x32*.com.nowcoder.ut.idl.HomeRankV6ItemFeatureB\x17\n\x13\x63om.nowcoder.ut.idlP\x00\x62\x06proto3'
)




_HOMERANKV6USERFEATURE = _descriptor.Descriptor(
  name='HomeRankV6UserFeature',
  full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='work_info', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.work_info', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='school', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.school', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gender', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.gender', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='edu_work_status', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.edu_work_status', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job1_1', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.career_job1_1', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job1_2', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.career_job1_2', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='career_job1_3', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.career_job1_3', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='edu_level', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.edu_level', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_year', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.work_year', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_status_detail', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.work_status_detail', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='school_major', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.school_major', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='school_type', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.school_type', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hist_entity_id', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.hist_entity_id', index=12,
      number=13, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hist_type', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.hist_type', index=13,
      number=14, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_len', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.max_len', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uid', full_name='com.nowcoder.ut.idl.HomeRankV6UserFeature.uid', index=15,
      number=16, type=9, cpp_type=9, label=1,
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
  serialized_start=43,
  serialized_end=393,
)


_HOMERANKV6ITEMFEATURE = _descriptor.Descriptor(
  name='HomeRankV6ItemFeature',
  full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='postmodule_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.postmodule_var', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='contenttopic_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.contenttopic_var', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='likenumber_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.likenumber_var', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='viewnumber_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.viewnumber_var', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='replynumber_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.replynumber_var', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='circlename_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.circlename_var', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='contentmode_var', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.contentmode_var', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.type', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ge_score', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.ge_score', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wv_score', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.wv_score', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ctr', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.ctr', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_id', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.entity_id', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_work_info', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_work_info', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_school', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_school', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_career_job1_1', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_career_job1_1', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_edu_level', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_edu_level', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_school_major', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_school_major', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_school_type', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_school_type', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_uid', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.author_uid', index=18,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='taxonomy1', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.taxonomy1', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='taxonomy2', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.taxonomy2', index=20,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='form', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.form', index=21,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quality_human', full_name='com.nowcoder.ut.idl.HomeRankV6ItemFeature.quality_human', index=22,
      number=23, type=9, cpp_type=9, label=1,
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
  serialized_start=396,
  serialized_end=930,
)


_HOMERANKV6REQUEST = _descriptor.Descriptor(
  name='HomeRankV6Request',
  full_name='com.nowcoder.ut.idl.HomeRankV6Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_feature', full_name='com.nowcoder.ut.idl.HomeRankV6Request.user_feature', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='item_feature', full_name='com.nowcoder.ut.idl.HomeRankV6Request.item_feature', index=1,
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
  serialized_start=933,
  serialized_end=1084,
)

_HOMERANKV6REQUEST.fields_by_name['user_feature'].message_type = _HOMERANKV6USERFEATURE
_HOMERANKV6REQUEST.fields_by_name['item_feature'].message_type = _HOMERANKV6ITEMFEATURE
DESCRIPTOR.message_types_by_name['HomeRankV6UserFeature'] = _HOMERANKV6USERFEATURE
DESCRIPTOR.message_types_by_name['HomeRankV6ItemFeature'] = _HOMERANKV6ITEMFEATURE
DESCRIPTOR.message_types_by_name['HomeRankV6Request'] = _HOMERANKV6REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HomeRankV6UserFeature = _reflection.GeneratedProtocolMessageType('HomeRankV6UserFeature', (_message.Message,), {
  'DESCRIPTOR' : _HOMERANKV6USERFEATURE,
  '__module__' : 'home_rec_v6_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.HomeRankV6UserFeature)
  })
_sym_db.RegisterMessage(HomeRankV6UserFeature)

HomeRankV6ItemFeature = _reflection.GeneratedProtocolMessageType('HomeRankV6ItemFeature', (_message.Message,), {
  'DESCRIPTOR' : _HOMERANKV6ITEMFEATURE,
  '__module__' : 'home_rec_v6_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.HomeRankV6ItemFeature)
  })
_sym_db.RegisterMessage(HomeRankV6ItemFeature)

HomeRankV6Request = _reflection.GeneratedProtocolMessageType('HomeRankV6Request', (_message.Message,), {
  'DESCRIPTOR' : _HOMERANKV6REQUEST,
  '__module__' : 'home_rec_v6_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.HomeRankV6Request)
  })
_sym_db.RegisterMessage(HomeRankV6Request)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
