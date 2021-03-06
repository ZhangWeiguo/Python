# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: userinfo.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='userinfo.proto',
  package='grpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0euserinfo.proto\x12\x04grpc\"\xb7\x01\n\x08UserInfo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12#\n\x05phone\x18\x04 \x03(\x0b\x32\x14.grpc.UserInfo.Phone\x1a?\n\x05Phone\x12\x0e\n\x06number\x18\x01 \x01(\t\x12&\n\x04type\x18\x02 \x01(\x0e\x32\x18.grpc.UserInfo.PhoneType\"+\n\tPhoneType\x12\n\n\x06MOBILE\x10\x00\x12\x08\n\x04HOME\x10\x01\x12\x08\n\x04WORK\x10\x02\x62\x06proto3')
)



_USERINFO_PHONETYPE = _descriptor.EnumDescriptor(
  name='PhoneType',
  full_name='grpc.UserInfo.PhoneType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MOBILE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOME', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WORK', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=165,
  serialized_end=208,
)
_sym_db.RegisterEnumDescriptor(_USERINFO_PHONETYPE)


_USERINFO_PHONE = _descriptor.Descriptor(
  name='Phone',
  full_name='grpc.UserInfo.Phone',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='grpc.UserInfo.Phone.number', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='grpc.UserInfo.Phone.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=100,
  serialized_end=163,
)

_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='grpc.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='grpc.UserInfo.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='grpc.UserInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phone', full_name='grpc.UserInfo.phone', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_USERINFO_PHONE, ],
  enum_types=[
    _USERINFO_PHONETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=208,
)

_USERINFO_PHONE.fields_by_name['type'].enum_type = _USERINFO_PHONETYPE
_USERINFO_PHONE.containing_type = _USERINFO
_USERINFO.fields_by_name['phone'].message_type = _USERINFO_PHONE
_USERINFO_PHONETYPE.containing_type = _USERINFO
DESCRIPTOR.message_types_by_name['UserInfo'] = _USERINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), dict(

  Phone = _reflection.GeneratedProtocolMessageType('Phone', (_message.Message,), dict(
    DESCRIPTOR = _USERINFO_PHONE,
    __module__ = 'userinfo_pb2'
    # @@protoc_insertion_point(class_scope:grpc.UserInfo.Phone)
    ))
  ,
  DESCRIPTOR = _USERINFO,
  __module__ = 'userinfo_pb2'
  # @@protoc_insertion_point(class_scope:grpc.UserInfo)
  ))
_sym_db.RegisterMessage(UserInfo)
_sym_db.RegisterMessage(UserInfo.Phone)


# @@protoc_insertion_point(module_scope)
