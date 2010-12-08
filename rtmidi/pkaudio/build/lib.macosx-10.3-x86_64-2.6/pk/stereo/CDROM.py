"""
	CDROM.py
		Constants for CDLow.py
	Copyright 2003 Christian Storgaard
   	Changes made by Ron Kuslak <rds@rdsarts.com>, 12/15/2003,
   	and are limited to the formating of this message.

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import struct
def sizeof(type):
  return struct.calcsize(type)

CDC_CD_R=0x2000
CDC_CD_RW=0x4000
CDC_CLOSE_TRAY=0x1
CDC_DRIVE_STATUS=0x800
CDC_DVD=0x8000
CDC_DVD_R=0x10000
CDC_DVD_RAM=0x20000
CDC_GENERIC_PACKET=0x1000
CDC_IOCTLS=0x400
CDC_LOCK=0x4
CDC_MCN=0x40
CDC_MEDIA_CHANGED=0x80
CDC_MULTI_SESSION=0x20
CDC_OPEN_TRAY=0x2
CDC_PLAY_AUDIO=0x100
CDC_RESET=0x200
CDC_SELECT_DISC=0x10
CDC_SELECT_SPEED=0x8
CDO_AUTO_CLOSE=0x1
CDO_AUTO_EJECT=0x2
CDO_CHECK_TYPE=0x10
CDO_LOCK=0x8
CDO_USE_FFLAGS=0x4
CDROMAUDIOBUFSIZ=0x5382
CDROMCLOSETRAY=0x5319
CDROMEJECT=0x5309
CDROMEJECT_SW=0x530f
CDROMGETSPINDOWN=0x531d
CDROMMULTISESSION=0x5310
CDROMPAUSE=0x5301
CDROMPLAYBLK=0x5317
CDROMPLAYMSF=0x5303
CDROMPLAYTRKIND=0x5304
CDROMREADALL=0x5318
CDROMREADAUDIO=0x530e
CDROMREADCOOKED=0x5315
CDROMREADMODE1=0x530d
CDROMREADMODE2=0x530c
CDROMREADRAW=0x5314
CDROMREADTOCENTRY=0x5306
CDROMREADTOCHDR=0x5305
CDROMRESET=0x5312
CDROMRESUME=0x5302
CDROMSEEK=0x5316
CDROMSETSPINDOWN=0x531e
CDROMSTART=0x5308
CDROMSTOP=0x5307
CDROMSUBCHNL=0x530b
CDROMVOLCTRL=0x530a
CDROMVOLREAD=0x5313
CDROM_AUDIO_COMPLETED=0x13
CDROM_AUDIO_ERROR=0x14
CDROM_AUDIO_INVALID=0x00
CDROM_AUDIO_NO_STATUS=0x15
CDROM_AUDIO_PAUSED=0x12
CDROM_AUDIO_PLAY=0x11
CDROM_CHANGER_NSLOTS=0x5328
CDROM_CLEAR_OPTIONS=0x5321
CDROM_DATA_TRACK=0x04
CDROM_DEBUG=0x5330
CDROM_DISC_STATUS=0x5327
CDROM_DRIVE_STATUS=0x5326
CDROM_GET_CAPABILITY=0x5331
CDROM_GET_MCN=0x5311
CDROM_GET_UPC=CDROM_GET_MCN
CDROM_LAST_WRITTEN=0x5395
CDROM_LBA=0x01
CDROM_LEADOUT=0xAA
CDROM_LOCKDOOR=0x5329
CDROM_MEDIA_CHANGED=0x5325
CDROM_MSF=0x02
CDROM_NEXT_WRITABLE=0x5394
CDROM_PACKET_SIZE=12
CDROM_SELECT_DISC=0x5323
CDROM_SELECT_SPEED=0x5322
CDROM_SEND_PACKET=0x5393
CDROM_SET_OPTIONS=0x5320
CDSL_CURRENT=( (int ) ( ~ 0 >> 1 ) )
CDSL_NONE=( (int ) ( ~ 0 >> 1 ) - 1 )
CDS_AUDIO=100
CDS_DATA_1=101
CDS_DATA_2=102
CDS_DISC_OK=4
CDS_DRIVE_NOT_READY=3
CDS_MIXED=105
CDS_NO_DISC=1
CDS_NO_INFO=0
CDS_TRAY_OPEN=2
CDS_XA_2_1=103
CDS_XA_2_2=104
CD_CHUNK_SIZE=24
CD_ECC_SIZE=276
CD_EDC_SIZE=4
CD_FRAMES=75
CD_FRAMESIZE=2048
CD_FRAMESIZE_RAW=2352
CD_SYNC_SIZE=12
CD_HEAD_SIZE=4
CD_FRAMESIZE_RAW0=( CD_FRAMESIZE_RAW - CD_SYNC_SIZE - CD_HEAD_SIZE )
CD_FRAMESIZE_RAW1=( CD_FRAMESIZE_RAW - CD_SYNC_SIZE )
CD_FRAMESIZE_RAWER=2646
CD_FRAMESIZE_SUB=96
CD_MINS=74
CD_MSF_OFFSET=150
CD_NUM_OF_CHUNKS=98
CD_PART_MAX=64
CD_PART_MASK=( CD_PART_MAX - 1 )
CD_SECS=60
CD_SUBHEAD_SIZE=8
CD_XA_HEAD=( CD_HEAD_SIZE + CD_SUBHEAD_SIZE )
CD_XA_SYNC_HEAD=( CD_SYNC_SIZE + CD_XA_HEAD )
CD_XA_TAIL=( CD_EDC_SIZE + CD_ECC_SIZE )
CD_ZERO_SIZE=8
CGC_DATA_NONE=3
CGC_DATA_READ=2
CGC_DATA_UNKNOWN=0
CGC_DATA_WRITE=1
DVD_AUTH=0x5392
DVD_AUTH_ESTABLISHED=5
DVD_AUTH_FAILURE=6
DVD_CGMS_RESTRICTED=3
DVD_CGMS_SINGLE=2
DVD_CGMS_UNRESTRICTED=0
DVD_CPM_COPYRIGHTED=1
DVD_CPM_NO_COPYRIGHT=0
DVD_CP_SEC_EXIST=1
DVD_CP_SEC_NONE=0
DVD_HOST_SEND_CHALLENGE=1
DVD_HOST_SEND_KEY2=4
DVD_HOST_SEND_RPC_STATE=11
DVD_INVALIDATE_AGID=9
DVD_LAYERS=4
DVD_LU_SEND_AGID=0
DVD_LU_SEND_ASF=8
DVD_LU_SEND_CHALLENGE=3
DVD_LU_SEND_KEY1=2
DVD_LU_SEND_RPC_STATE=10
DVD_LU_SEND_TITLE_KEY=7
DVD_READ_STRUCT=0x5390
DVD_STRUCT_BCA=0x03
DVD_STRUCT_COPYRIGHT=0x01
DVD_STRUCT_DISCKEY=0x02
DVD_STRUCT_MANUFACT=0x04
DVD_STRUCT_PHYSICAL=0x00
DVD_WRITE_STRUCT=0x5391
#'EOPNOTSUPP' undefined in 'EDRIVE_CANT_DO_THIS'
GPCMD_BLANK=0xa1
GPCMD_CLOSE_TRACK=0x5b
GPCMD_FLUSH_CACHE=0x35
GPCMD_FORMAT_UNIT=0x04
GPCMD_GET_CONFIGURATION=0x46
GPCMD_GET_EVENT_STATUS_NOTIFICATION=0x4a
GPCMD_GET_MEDIA_STATUS=0xda
GPCMD_GET_PERFORMANCE=0xac
GPCMD_INQUIRY=0x12
GPCMD_LOAD_UNLOAD=0xa6
GPCMD_MECHANISM_STATUS=0xbd
GPCMD_MODE_SELECT_10=0x55
GPCMD_MODE_SENSE_10=0x5a
GPCMD_PAUSE_RESUME=0x4b
GPCMD_PLAYAUDIO_TI=0x48
GPCMD_PLAY_AUDIO_10=0x45
GPCMD_PLAY_AUDIO_MSF=0x47
GPCMD_PLAY_AUDIO_TI=0x48
GPCMD_PLAY_CD=0xbc
GPCMD_PREVENT_ALLOW_MEDIUM_REMOVAL=0x1e
GPCMD_READ_10=0x28
GPCMD_READ_12=0xa8
GPCMD_READ_CD=0xbe
GPCMD_READ_CDVD_CAPACITY=0x25
GPCMD_READ_CD_MSF=0xb9
GPCMD_READ_DISC_INFO=0x51
GPCMD_READ_DVD_STRUCTURE=0xad
GPCMD_READ_FORMAT_CAPACITIES=0x23
GPCMD_READ_HEADER=0x44
GPCMD_READ_SUBCHANNEL=0x42
GPCMD_READ_TOC_PMA_ATIP=0x43
GPCMD_READ_TRACK_RZONE_INFO=0x52
GPCMD_REPAIR_RZONE_TRACK=0x58
GPCMD_REPORT_KEY=0xa4
GPCMD_REQUEST_SENSE=0x03
GPCMD_RESERVE_RZONE_TRACK=0x53
GPCMD_SCAN=0xba
GPCMD_SEEK=0x2b
GPCMD_SEND_DVD_STRUCTURE=0xad
GPCMD_SEND_EVENT=0xa2
GPCMD_SEND_KEY=0xa3
GPCMD_SEND_OPC=0x54
GPCMD_SET_READ_AHEAD=0xa7
GPCMD_SET_SPEED=0xbb
GPCMD_SET_STREAMING=0xb6
GPCMD_START_STOP_UNIT=0x1b
GPCMD_STOP_PLAY_SCAN=0x4e
GPCMD_TEST_UNIT_READY=0x00
GPCMD_VERIFY_10=0x2f
GPCMD_WRITE_10=0x2a
GPCMD_WRITE_AND_VERIFY_10=0x2e
GPMODE_ALL_PAGES=0x3f
GPMODE_AUDIO_CTL_PAGE=0x0e
GPMODE_CAPABILITIES_PAGE=0x2a
GPMODE_CDROM_PAGE=0x0d
GPMODE_FAULT_FAIL_PAGE=0x1c
GPMODE_POWER_PAGE=0x1a
GPMODE_R_W_ERROR_PAGE=0x01
GPMODE_TO_PROTECT_PAGE=0x1d
GPMODE_WRITE_PARMS_PAGE=0x05
_I386_BYTEORDER_H=None
_I386_TYPES_H=None
_LINUX_BYTEORDER_GENERIC_H=None
_LINUX_BYTEORDER_LITTLE_ENDIAN_H=None
_LINUX_BYTEORDER_SWAB_H=None
_LINUX_CDROM_H=None
__ELF__=1
__LITTLE_ENDIAN=1234
__LITTLE_ENDIAN_BITFIELD=None
#'__u16' undefined in '___constant_swab16'
#'__u32' undefined in '___constant_swab32'
#'__u64' undefined in '___constant_swab64'
#'__u16' undefined in '___swab16'
#'__u32' undefined in '___swab32'
#'__u64' undefined in '___swab64'
#'__u16' undefined in '__arch__swab16'
#'__u16' undefined in '__arch__swab16'
#'__arch__swab16p': failed dependancy:'__arch__swab16'
#'do' undefined in '__arch__swab16s'
#'__u32' undefined in '__arch__swab32'
#'__u32' undefined in '__arch__swab32'
#'__arch__swab32p': failed dependancy:'__arch__swab32'
#'do' undefined in '__arch__swab32s'
#'__u64' undefined in '__arch__swab64'
#'__u64' undefined in '__arch__swab64'
#'__arch__swab64p': failed dependancy:'__arch__swab64'
#'do' undefined in '__arch__swab64s'
#'__fswab16' undefined in '__swab16'
#'__be16_to_cpu': failed dependancy:'__swab16'
#'__swab16p' undefined in '__be16_to_cpup'
#'__swab16s' undefined in '__be16_to_cpus'
#'__fswab32' undefined in '__swab32'
#'__be32_to_cpu': failed dependancy:'__swab32'
#'__swab32p' undefined in '__be32_to_cpup'
#'__swab32s' undefined in '__be32_to_cpus'
#'__fswab64' undefined in '__swab64'
#'__be64_to_cpu': failed dependancy:'__swab64'
#'__swab64p' undefined in '__be64_to_cpup'
#'__swab64s' undefined in '__be64_to_cpus'
#'__u16' undefined in '___constant_swab16'
#'__constant_be16_to_cpu': failed dependancy:'___constant_swab16'
#'__u32' undefined in '___constant_swab32'
#'__constant_be32_to_cpu': failed dependancy:'___constant_swab32'
#'__u64' undefined in '___constant_swab64'
#'__constant_be64_to_cpu': failed dependancy:'___constant_swab64'
#'__u16' undefined in '___constant_swab16'
#'__constant_cpu_to_be16': failed dependancy:'___constant_swab16'
#'__u32' undefined in '___constant_swab32'
#'__constant_cpu_to_be32': failed dependancy:'___constant_swab32'
#'__u64' undefined in '___constant_swab64'
#'__constant_cpu_to_be64': failed dependancy:'___constant_swab64'
def __constant_cpu_to_le16(x):
  return ( (__u16 ) (x ) )
def __constant_cpu_to_le32(x):
  return ( (__u32 ) (x ) )
def __constant_cpu_to_le64(x):
  return ( (__u64 ) (x ) )
#'__u32' undefined in '___constant_swab32'
#'__constant_htonl': failed dependancy:'___constant_swab32'
#'__u16' undefined in '___constant_swab16'
#'__constant_htons': failed dependancy:'___constant_swab16'
def __constant_le16_to_cpu(x):
  return ( (__u16 ) (x ) )
def __constant_le32_to_cpu(x):
  return ( (__u32 ) (x ) )
def __constant_le64_to_cpu(x):
  return ( (__u64 ) (x ) )
#'__u32' undefined in '___constant_swab32'
#'__constant_ntohl': failed dependancy:'___constant_swab32'
#'__u16' undefined in '___constant_swab16'
#'__constant_ntohs': failed dependancy:'___constant_swab16'
#'__fswab16' undefined in '__swab16'
#'__cpu_to_be16': failed dependancy:'__swab16'
#'__swab16p' undefined in '__cpu_to_be16p'
#'__swab16s' undefined in '__cpu_to_be16s'
#'__fswab32' undefined in '__swab32'
#'__cpu_to_be32': failed dependancy:'__swab32'
#'__swab32p' undefined in '__cpu_to_be32p'
#'__swab32s' undefined in '__cpu_to_be32s'
#'__fswab64' undefined in '__swab64'
#'__cpu_to_be64': failed dependancy:'__swab64'
#'__swab64p' undefined in '__cpu_to_be64p'
#'__swab64s' undefined in '__cpu_to_be64s'
def __cpu_to_le16(x):
  return ( (__u16 ) (x ) )
#Traceback (most recent call last):
#  File "./h2py.py", line 203, in output_py
#    exec(_outs,env)
#  File "<string>", line 1
#     def __cpu_to_le16p(x):  return ( * (__u16* ) (x ) )
#                                      ^
# SyntaxError: invalid syntax
#skipping '__cpu_to_le16p'
#'do' undefined in '__cpu_to_le16s'
def __cpu_to_le32(x):
  return ( (__u32 ) (x ) )
#Traceback (most recent call last):
#  File "./h2py.py", line 203, in output_py
#    exec(_outs,env)
#  File "<string>", line 1
#     def __cpu_to_le32p(x):  return ( * (__u32* ) (x ) )
#                                      ^
# SyntaxError: invalid syntax
#skipping '__cpu_to_le32p'
#'do' undefined in '__cpu_to_le32s'
def __cpu_to_le64(x):
  return ( (__u64 ) (x ) )
#Traceback (most recent call last):
#  File "./h2py.py", line 203, in output_py
#    exec(_outs,env)
#  File "<string>", line 1
#     def __cpu_to_le64p(x):  return ( * (__u64* ) (x ) )
#                                      ^
# SyntaxError: invalid syntax
#skipping '__cpu_to_le64p'
#'do' undefined in '__cpu_to_le64s'
__i386=1
__i386__=1
def __le16_to_cpu(x):
  return ( (__u16 ) (x ) )
#Traceback (most recent call last):
#  File "./h2py.py", line 203, in output_py
#    exec(_outs,env)
#  File "<string>", line 1
#     def __le16_to_cpup(x):  return ( * (__u16* ) (x ) )
#                                      ^
# SyntaxError: invalid syntax
#skipping '__le16_to_cpup'
#'do' undefined in '__le16_to_cpus'
def __le32_to_cpu(x):
  return ( (__u32 ) (x ) )
#Traceback (most recent call last):
#  File "./h2py.py", line 203, in output_py
#    exec(_outs,env)
#  File "<string>", line 1
#     def __le32_to_cpup(x):  return ( * (__u32* ) (x ) )
#                                      ^
# SyntaxError: invalid syntax
#skipping '__le32_to_cpup'
#'do' undefined in '__le32_to_cpus'
def __le64_to_cpu(x):
  return ( (__u64 ) (x ) )
#Traceback (most recent call last):
#  File "./h2py.py", line 203, in output_py
#    exec(_outs,env)
#  File "<string>", line 1
#     def __le64_to_cpup(x):  return ( * (__u64* ) (x ) )
#                                      ^
# SyntaxError: invalid syntax
#skipping '__le64_to_cpup'
#'do' undefined in '__le64_to_cpus'
__linux=1
__linux__=1
#'__fswab16' undefined in '__swab16'
#'__fswab32' undefined in '__swab32'
#'__fswab64' undefined in '__swab64'
__unix=1
__unix__=1
i386=1
linux=1
unix=1
