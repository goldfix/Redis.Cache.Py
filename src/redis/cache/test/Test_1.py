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

import redis
import uuid
import datetime

from unittest.case import TestCase

class MyUnitTest(TestCase):

    def __init__(self):
        pass
    
    def LoadData_Test_1(self):
        
        p = redis.StrictRedis("127.0.0.1", db=0)
        
        p = p.pipeline()
        
        
        for i in range(0, 10):
            k = uuid.uuid4()
            v = str( k ) + "---" + datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ%f")
            
            #print  (k, v)
            p.append(k, v)
            print( "K: " + str(i) + "/1000: " + str(k))
        
        for z in range(0, 10):
            k = uuid.uuid4()
            print( "SET K: " + str(z) + "/1000: " + str(k))
            for i in range(0, 10):
                v = str( k ) + str(uuid.uuid4()) + "---" + datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ%f")
                p.sadd(k, v)
                pass
        
        
        p.execute()
             
        print( "END" )
        pass
    
    def LoadData_Test_2(self):
        
        r = redis.StrictRedis("127.0.0.1", db=0)
        ks = r.keys()
        
        for k in ks:
            if(r.type(k) != b"string") and (r.scard(k)>2):
                print( r.scard(k) )
            #print( k )
            pass
        
        print(len( ks ) )
        
        pass
    
    def LoadData_Test_3(self):
        
        r = redis.StrictRedis("127.0.0.1")
        print (r.info()["redis_version"])
        
        pass
    
    
    def CSharpTest(self):
        r = redis.StrictRedis("127.0.0.1")

        result = r.lrange("k_string", 0, 1)
        self.assertTrue(result[1] == "Test 1234567890 Test 0987654321 Test 1234567890 Test 0987654321 Test 1234567890 Test 0987654321 メンズア")
        print "assertTrue :: k_string :: OK"
        
        result = r.lrange("k_int16", 0, 1)
        self.assertTrue(int( result[1]) == 12345)
        print "assertTrue :: k_int16 :: OK"        
        
        result = r.lrange("k_double", 0, 1)
        self.assertTrue( float( result[1]) == 12345.06789)
        print "assertTrue :: k_double :: OK"        
        
        result = r.lrange("k_byte[]", 0, 1)
        tmp = result[1].decode("utf-8") 
        self.assertTrue(result[1] == "Test 1234567890 Test 0987654321 Test 1234567890 Test 0987654321 Test 1234567890 Test 0987654321 メンズア")
        print "assertTrue :: k_byte[] :: OK"
        
        pass
    
    
    
# x = MyClass().LoadData_Test_1()
# x = MyUnitTest().CSharpTest()







