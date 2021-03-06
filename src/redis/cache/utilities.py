# -*- coding: utf-8 -*- 
'''
Copyright (c) 2014, pietro partescano
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Redis.Cache.Py nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import zlib
from redis.cache.errors import NotProvidedError
import pickle
import datetime
from redis.cache import errors, config
from locale import str


_COMPRESS = 1
_DECOMPRESS = 2

_SERIALIZE = 3
_DESERIALIZE = 4

_NO_EXPIRATION = datetime.timedelta(hours=00, minutes=00, seconds=00)
_No_TTL = "ND"

_StatusItem_None = 0
_StatusItem_Compressed = 1
_StatusItem_Serialized = 2

def StatusItemDeSerialize(v):
    result = str(v).split("|")[4]
    return result


def _ConvertObjToRedisValue(value):
    if(value is None):
        raise errors.ArgumentError("Parameter is invalid (value)")
    
    result = value
    statusItem = _StatusItem_None
    if( (type(value) is int) or (type(value) is float) or (type(value) is long) or (type(value) is complex) or (type(value) is bool) ):
        pass
    elif( (type(value) is str) or (type(value) is unicode) ):
        if (config.UseCompression):
            result = _Deflate(result, _COMPRESS)
            statusItem = _StatusItem_Compressed 
        else:
            pass        
    else:
        if (config.UseCompression):
            result = _Serialize(result, _SERIALIZE)
            result = _Deflate(result, _COMPRESS)
            statusItem = _StatusItem_Compressed + _StatusItem_Serialized 
        else:
            result = _Serialize(result, _SERIALIZE)
            statusItem = _StatusItem_Serialized

    return result, statusItem 


def _ConvertRedisValueToObject(value, statusItem):
    if(value is None or statusItem is None):
        raise errors.ArgumentError("Parameter is invalid (value or statusItem)")
    
    result = value
    if((statusItem & _StatusItem_None)==_StatusItem_None):
        pass
    if((statusItem & _StatusItem_Compressed)==_StatusItem_Compressed):
        result = _Deflate(result, _DECOMPRESS)
        pass
    if((statusItem & _StatusItem_Serialized)==_StatusItem_Serialized):
        result = _Serialize(result, _DESERIALIZE)
        pass
    
    return result



def _Deflate(source_bytes, type_operation):
    if (type_operation==_COMPRESS):
        cmpss = zlib.compressobj(6,zlib.DEFLATED,-zlib.MAX_WBITS)
        bytes_compressed = cmpss.compress(source_bytes)
        bytes_compressed += cmpss.flush()
        
        return bytes_compressed

    elif(type_operation==_DECOMPRESS):
        decmpss = zlib.decompressobj(-zlib.MAX_WBITS)
        bytes_decompressed = decmpss.decompress(source_bytes)
        bytes_decompressed += decmpss.flush()
        
        return bytes_decompressed 
    else:
        raise NotProvidedError("type_operation not correct")
    
    pass

def _Serialize(data, type_operation):
    if (type_operation==_SERIALIZE):
        data_serialized = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        return data_serialized

    elif(type_operation==_DESERIALIZE):
        data_deserialized = pickle.loads(data)
        return data_deserialized
    
    else:
        raise NotProvidedError("type_operation not correct")
    
    pass


def _TTLSerialize(ttlSLI, ttlABS, forceUpdateDtABS, statusItem):
    
    dtResult = (datetime.datetime.utcnow() + ttlSLI)
    str_dtSLI = dtResult.strftime("%Y%m%dT%H%M%S")
    str_tsSLI = str(int(ttlSLI.total_seconds()))

    if(ttlSLI==_NO_EXPIRATION):
        str_dtSLI = _No_TTL
        str_tsSLI = _No_TTL
        
    dtResult = (datetime.datetime.utcnow() + ttlABS)
    str_dtABS = dtResult.strftime("%Y%m%dT%H%M%S")
    str_tsABS = str(int(ttlABS.total_seconds()))

    if(ttlABS==_NO_EXPIRATION):
        str_dtABS = _No_TTL
        str_tsABS = _No_TTL

    if(forceUpdateDtABS != datetime.datetime.max):
        str_dtABS = forceUpdateDtABS.strftime("%Y%m%dT%H%M%S")

    strResult = str_dtSLI + "|" + str_tsSLI + "|" + str_dtABS + "|" + str_tsABS + "|" + str(statusItem)
 
    return strResult
 
def _TTL_TS_DeSerialize(ttl):
    
    if(ttl is None or ttl.strip()==""):
        raise errors.ArgumentError("Parameter is invalid (ttl)")
    
    dts = ttl.split("|")
    tsSLI = _NO_EXPIRATION
    tsABS = _NO_EXPIRATION
    
    if(dts[1]!=_No_TTL):
        tsSLI = datetime.timedelta(seconds=int(dts[1]))
        pass

    if(dts[3]!=_No_TTL):
        tsABS = datetime.timedelta(seconds=int(dts[3]))
        pass    
    
    result = (tsSLI, tsABS)
    return result

def _TTL_DT_DeSerialize(ttl):
    
    if(ttl is None or ttl.strip()==""):
        raise errors.ArgumentError("Parameter is invalid (ttl)")
    
    dts = ttl.split("|")
    dtSLI = datetime.datetime.max
    dtABS = datetime.datetime.max
    
    if(dts[0]!=_No_TTL):
        dtSLI = datetime.datetime.strptime(dts[0], "%Y%m%dT%H%M%S")
        pass

    if(dts[2]!=_No_TTL):
        dtABS = datetime.datetime.strptime(dts[2], "%Y%m%dT%H%M%S")
        pass    
    
    result = (dtSLI, dtABS)
    return result


def _TTL_Is_Expired(ttl):
    
    if(ttl is None):
        raise errors.ArgumentError("Parameter is invalid (ttl)")
    
    dtNow = datetime.datetime.utcnow()
    dt = ttl
    if( type(ttl) is str ):
        dt = _TTL_DT_DeSerialize(ttl)
    
    if(dtNow>dt[0]) or (dtNow>dt[1]):
        return True
    else:
        return False




