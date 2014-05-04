'''
Created on 04/mag/2014

@author: ppartes-v
'''

from redis.cache import utilities
from redis.cache.utilities import _COMPRESS, _DECOMPRESS, _SERIALIZE,\
    _DESERIALIZE
from unittest.case import TestCase
from redis.cache.errors import NotProvidedError
import datetime


class Test(TestCase):
    
    def __init__(self):
        print "\n"
        pass

    def CompressionTest(self):
        print "CompressionTest :: Init..."
        f = open("txt_test_long.txt", "rb")        
        str_to_compress = f.read()
        f.flush()
        f.close()

        str_compressed = utilities._Deflate(str_to_compress, _COMPRESS)
        str_decompressed = utilities._Deflate(str_compressed, _DECOMPRESS)
        self.assertTrue((str_to_compress==str_decompressed))
        
        try:
            str_compressed = utilities._Deflate(str_to_compress, _COMPRESS)
            str_decompressed = utilities._Deflate(str_compressed, 3)
            self.assertTrue((str_to_compress==str_decompressed))
        except (NotProvidedError):
            print "CompressionTest :: OK"

    def SerializationTest(self):
        print "SerializationTest :: Init..."
        f = open("txt_test_long.txt", "rb")        
        str_to_serialize = f.read()
        f.flush()
        f.close()
        
        str_serialized = utilities._Serialize(str_to_serialize, _SERIALIZE)
        str_deserialized = utilities._Serialize(str_serialized, _DESERIALIZE)
        self.assertTrue((str_to_serialize, str_deserialized ) )
        
        try:
            str_serialized = utilities._Serialize(str_to_serialize, _SERIALIZE)
            str_deserialized = utilities._Serialize(str_serialized, 5)
            self.assertTrue((str_to_serialize, str_deserialized ) )
        except (NotProvidedError):
            print "SerializationTest :: OK"
        
        pass

    def TTL_Test(self):
        
        ttl_sli =  datetime.timedelta(hours=11, minutes=22, seconds=33)
        ttl_abs =  datetime.timedelta(hours=22, minutes=11, seconds=00)
        
        result = utilities._TTLSerialize(ttl_sli, ttl_abs, datetime.datetime.max)
        print result

        pass

# if __name__ == "__main__":
#     import sys;sys.argv = ['Test.CompressionTest']
#     unittest.main()
    
# p = Test().CompressionTest()
# p = Test().SerializationTest()
# p = Test().TTL_Test()




