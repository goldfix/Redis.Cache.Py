'''
Created on 04/mag/2014

@author: ppartes-v
'''
import zlib
from redis.cache.errors import NotProvidedError
import pickle
import datetime

_COMPRESS = 1
_DECOMPRESS = 2

_SERIALIZE = 3
_DESERIALIZE = 4

_NO_EXPIRATION = datetime.timedelta(hours=00, minutes=00, seconds=00)
_No_TTL = "ND"

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


def _TTLSerialize(ttlSLI, ttlABS, forceUpdateDtABS):
    
    dtResult = (datetime.datetime.utcnow() + ttlSLI)
    str_dtSLI = dtResult.strftime("%Y%m%dT%H%M%S")
    str_tsSLI = str(ttlSLI).split(":")[0].zfill(2) + str(ttlSLI).split(":")[1].zfill(2) + str(ttlSLI).split(":")[2].zfill(2)

    if(ttlSLI==_NO_EXPIRATION):
        str_dtSLI = _No_TTL
        str_tsSLI = _No_TTL
        
    dtResult = (datetime.datetime.utcnow() + ttlABS)
    str_dtABS = dtResult.strftime("%Y%m%dT%H%M%S")
    str_tsABS = str(ttlABS).split(":")[0].zfill(2) + str(ttlABS).split(":")[1].zfill(2) + str(ttlABS).split(":")[2].zfill(2)

    if(ttlABS==_NO_EXPIRATION):
        str_dtABS = _No_TTL
        str_tsABS = _No_TTL

    if(forceUpdateDtABS != datetime.datetime.max):
        str_dtABS = forceUpdateDtABS.strftime("%Y%m%dT%H%M%S")

    strResult = str_dtSLI + "|" + str_tsSLI + "|" + str_dtABS + "|" + str_tsABS
 
    return strResult
 




