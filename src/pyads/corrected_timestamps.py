
from __future__ import annotations

import pyads
from pyads.pyads_ex import adsSyncReadReqEx2, adsSyncWriteReqEx

__all__ = [
    "read_external_time_set",
    "read_external_time_set_all",
    "write_external_time_set",
    "write_external_time_set_all",
]

# For index group definitions, see documentation
# https://infosys.beckhoff.com/english.php?content=../content/1033/tc3_grundlagen/6313276043.html&id=616515874922742378
ADSIGRP_EXTERNALTIME = 0xF088
# ioffs&0xf == timebase (0 = None, 1 = Hard, 2 = Medium, 3 = Soft)
ADSIOFFS_EXTERNALTIME_SET = 0x00000000
# AdsR: ITcExternalTime::TimeType - get base time of calling AmsAddr; AdsW: nothing - set base time of calling AmsAddr;
ADSIOFFS_EXTERNALTIME_OFFSET = 0x00000100
# AdsR: timeoffset (__int64); AdsW: timeoffset (__int64);
ADSIOFFS_EXTERNALTIME_ABSOLUTE = 0x00000200
# AdsR: actuale time corrected by timeoffset (__int64);
ADSIOFFS_EXTERNALTIME_PROVIDER = 0x00000300
# AdsR: OTCID of provider;
ADSIOFFS_EXTERNALTIME_SETALL = 0x00000400
# AdsR: ITcExternalTime::TimeType - get base time for all clients!; AdsW: nothing - set base time for all clients;


def ADSIOFFS_EXTERNALTIME_TYPE(io):
    return (io) & 0x000000FF


def read_external_time_provider(plc: pyads.Connection, eTimeType: int) -> int:
    """Reading the object ID from the TimeOffset provider."""
    return adsSyncReadReqEx2(
        port=plc._port,
        address=plc._adr,
        index_group=0xF088,
        index_offset=ADSIOFFS_EXTERNALTIME_PROVIDER
        | ADSIOFFS_EXTERNALTIME_TYPE(eTimeType),
        data_type=pyads.PLCTYPE_DINT,
    )


def read_external_time_offset(plc: pyads.Connection, eTimeType: int) -> int:
    """Reading the current offset for a type."""
    return adsSyncReadReqEx2(
        port=plc._port,
        address=plc._adr,
        index_group=0xF088,
        index_offset=ADSIOFFS_EXTERNALTIME_OFFSET
        | ADSIOFFS_EXTERNALTIME_TYPE(eTimeType),
        data_type=pyads.PLCTYPE_LINT,
    )


def read_external_time_absolute(plc: pyads.Connection, eTimeType: int) -> int:
    """Reading the corrected time stamp."""
    return adsSyncReadReqEx2(
        port=plc._port,
        address=plc._adr,
        index_group=0xF088,
        index_offset=ADSIOFFS_EXTERNALTIME_ABSOLUTE
        | ADSIOFFS_EXTERNALTIME_TYPE(eTimeType),
        data_type=pyads.PLCTYPE_LINT,
    )


def read_external_time_set(plc: pyads.Connection) -> int:
    """Read the currently configured offset type for the respective ADS client."""
    return adsSyncReadReqEx2(
        port=plc._port,
        address=plc._adr,
        index_group=0xF088,
        index_offset=ADSIOFFS_EXTERNALTIME_SET,
        data_type=pyads.PLCTYPE_DINT,
    )


def write_external_time_set(plc: pyads.Connection, provider: int) -> None:
    """Set the offset type for the ADSDevice notifications of the respective ADS client."""
    adsSyncWriteReqEx(
        port=plc._port,
        address=plc._adr,
        index_group=ADSIGRP_EXTERNALTIME,
        index_offset=ADSIOFFS_EXTERNALTIME_SET | ADSIOFFS_EXTERNALTIME_TYPE(provider),
        value=0,
        plc_data_type=None,
    )


def read_external_time_set_all(plc: pyads.Connection) -> int:
    """Reads the type that is used if no other type is set."""
    return adsSyncReadReqEx2(
        port=plc._port,
        address=plc._adr,
        index_group=0xF088,
        index_offset=ADSIOFFS_EXTERNALTIME_SETALL,
        data_type=pyads.PLCTYPE_DINT,
    )


def write_external_time_set_all(plc: pyads.Connection, provider: int) -> None:
    """Sets the type that is used if no other type is set."""
    adsSyncWriteReqEx(
        port=plc._port,
        address=plc._adr,
        index_group=ADSIGRP_EXTERNALTIME,
        index_offset=ADSIOFFS_EXTERNALTIME_SETALL
        | ADSIOFFS_EXTERNALTIME_TYPE(provider),
        value=0,
        plc_data_type=None,
    )
