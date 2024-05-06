# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nowpick_invite_user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19nowpick_invite_user.proto\x12\x13\x63om.nowcoder.ut.idl\"\x1a\n\tHrFeature\x12\r\n\x05hr_id\x18\x01 \x01(\x03\"\x91\x01\n\rFilterFeature\x12\x19\n\x11workTimeMinMillis\x18\x01 \x01(\x03\x12\x19\n\x11workTimeMaxMillis\x18\x02 \x01(\x03\x12\x16\n\x0egraduationYear\x18\x03 \x01(\x05\x12\x12\n\nsocialType\x18\x04 \x01(\x05\x12\x0e\n\x06jobIds\x18\x05 \x03(\x03\x12\x0e\n\x06\x63ities\x18\x06 \x03(\t\"\xe0\x02\n\rResumeFeature\x12\x11\n\tresume_id\x18\x01 \x01(\x03\x12+\n\x06reason\x18\x02 \x01(\x0e\x32\x1b.com.nowcoder.ut.idl.Reason\x12\x15\n\rcareer_job_id\x18\x03 \x01(\x03\x12\x0e\n\x06gender\x18\x04 \x01(\t\x12\x15\n\rschool_status\x18\x05 \x01(\t\x12\x0e\n\x06job_id\x18\x06 \x01(\x03\x12\x17\n\x0fgraduation_time\x18\x07 \x01(\t\x12\x19\n\x11highest_education\x18\x08 \x01(\t\x12\x12\n\nbirth_time\x18\t \x01(\t\x12\x14\n\x0c\x63\x61ndidate_id\x18\n \x01(\t\x12\x18\n\x10last_online_time\x18\x0b \x01(\t\x12\x17\n\x0fyear_salary_min\x18\x0c \x01(\t\x12\x17\n\x0fwork_want_place\x18\r \x01(\t\x12\x17\n\x0fyear_salary_max\x18\x0e \x01(\t\"\xc9\x01\n\x18NowpickInviteUserRequest\x12\x33\n\x0bhr_features\x18\x01 \x01(\x0b\x32\x1e.com.nowcoder.ut.idl.HrFeature\x12;\n\x0f\x66ilter_features\x18\x02 \x01(\x0b\x32\".com.nowcoder.ut.idl.FilterFeature\x12;\n\x0fresume_features\x18\x03 \x03(\x0b\x32\".com.nowcoder.ut.idl.ResumeFeature\"q\n\x0eResumeResponse\x12\x11\n\tresume_id\x18\x01 \x01(\x03\x12\r\n\x05score\x18\x02 \x01(\x02\x12+\n\x06reason\x18\x03 \x01(\x0e\x32\x1b.com.nowcoder.ut.idl.Reason\x12\x10\n\x08punished\x18\x04 \x01(\x02\"T\n\x19NowpickInviteUserResponse\x12\x37\n\nresumeList\x18\x01 \x03(\x0b\x32#.com.nowcoder.ut.idl.ResumeResponse*H\n\x06Reason\x12\x0b\n\x07\x64\x65\x66\x61ult\x10\x00\x12\x08\n\x04grem\x10J\x12\x14\n\x10nowpickOriginRec\x10\n\x12\x11\n\rnowpickSecRec\x10\x0b\x42\x17\n\x13\x63om.nowcoder.ut.idlP\x00\x62\x06proto3')

_REASON = DESCRIPTOR.enum_types_by_name['Reason']
Reason = enum_type_wrapper.EnumTypeWrapper(_REASON)
default = 0
grem = 74
nowpickOriginRec = 10
nowpickSecRec = 11


_HRFEATURE = DESCRIPTOR.message_types_by_name['HrFeature']
_FILTERFEATURE = DESCRIPTOR.message_types_by_name['FilterFeature']
_RESUMEFEATURE = DESCRIPTOR.message_types_by_name['ResumeFeature']
_NOWPICKINVITEUSERREQUEST = DESCRIPTOR.message_types_by_name['NowpickInviteUserRequest']
_RESUMERESPONSE = DESCRIPTOR.message_types_by_name['ResumeResponse']
_NOWPICKINVITEUSERRESPONSE = DESCRIPTOR.message_types_by_name['NowpickInviteUserResponse']
HrFeature = _reflection.GeneratedProtocolMessageType('HrFeature', (_message.Message,), {
  'DESCRIPTOR' : _HRFEATURE,
  '__module__' : 'nowpick_invite_user_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.HrFeature)
  })
_sym_db.RegisterMessage(HrFeature)

FilterFeature = _reflection.GeneratedProtocolMessageType('FilterFeature', (_message.Message,), {
  'DESCRIPTOR' : _FILTERFEATURE,
  '__module__' : 'nowpick_invite_user_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.FilterFeature)
  })
_sym_db.RegisterMessage(FilterFeature)

ResumeFeature = _reflection.GeneratedProtocolMessageType('ResumeFeature', (_message.Message,), {
  'DESCRIPTOR' : _RESUMEFEATURE,
  '__module__' : 'nowpick_invite_user_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.ResumeFeature)
  })
_sym_db.RegisterMessage(ResumeFeature)

NowpickInviteUserRequest = _reflection.GeneratedProtocolMessageType('NowpickInviteUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _NOWPICKINVITEUSERREQUEST,
  '__module__' : 'nowpick_invite_user_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.NowpickInviteUserRequest)
  })
_sym_db.RegisterMessage(NowpickInviteUserRequest)

ResumeResponse = _reflection.GeneratedProtocolMessageType('ResumeResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESUMERESPONSE,
  '__module__' : 'nowpick_invite_user_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.ResumeResponse)
  })
_sym_db.RegisterMessage(ResumeResponse)

NowpickInviteUserResponse = _reflection.GeneratedProtocolMessageType('NowpickInviteUserResponse', (_message.Message,), {
  'DESCRIPTOR' : _NOWPICKINVITEUSERRESPONSE,
  '__module__' : 'nowpick_invite_user_pb2'
  # @@protoc_insertion_point(class_scope:com.nowcoder.ut.idl.NowpickInviteUserResponse)
  })
_sym_db.RegisterMessage(NowpickInviteUserResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023com.nowcoder.ut.idlP\000'
  _REASON._serialized_start=986
  _REASON._serialized_end=1058
  _HRFEATURE._serialized_start=50
  _HRFEATURE._serialized_end=76
  _FILTERFEATURE._serialized_start=79
  _FILTERFEATURE._serialized_end=224
  _RESUMEFEATURE._serialized_start=227
  _RESUMEFEATURE._serialized_end=579
  _NOWPICKINVITEUSERREQUEST._serialized_start=582
  _NOWPICKINVITEUSERREQUEST._serialized_end=783
  _RESUMERESPONSE._serialized_start=785
  _RESUMERESPONSE._serialized_end=898
  _NOWPICKINVITEUSERRESPONSE._serialized_start=900
  _NOWPICKINVITEUSERRESPONSE._serialized_end=984
# @@protoc_insertion_point(module_scope)