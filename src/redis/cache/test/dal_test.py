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
from unittest.case import TestCase
from redis.cache import dal, utilities, config
import datetime


class Test(TestCase):

    def __init__(self):
        print "\n"
    pass


    def ItemExist_Test(self):
        
        result = dal.RedisDal().ItemExist("test_1122")
        self.assertTrue((result==False))
        print "ItemExist_Test::OK"
        
        pass

    def AddListItem_Test(self):
        dal.RedisDal().ItemDelete("key1234")
        result = dal.RedisDal().AddListItem("key1234", "val1")
        result = dal.RedisDal().AddListItem("key1234", "val2")
        result = dal.RedisDal().GetListItem("key1234")
        self.assertTupleEqual(result, ('val1', 'val2'))         
        print "AddListItem_Test::OK"
        pass


    def AddListItemWithTTL_Test(self):
        
        #Set TTL
        ttlSLI = datetime.timedelta(hours=0, minutes=0, seconds=20)
        ttlABS = datetime.timedelta(hours=0, minutes=0, seconds=30)
        ttl = utilities._TTLSerialize(ttlSLI, ttlABS, datetime.datetime.max)
        
        dal.RedisDal().ItemDelete("key456")
        
        result = dal.RedisDal().AddListItemWithTTL("key456", "value_1", ttl)
        
        dal.RedisDal().SetTTL("key456", ttlSLI)
        
        result = dal.RedisDal().GetListItem("key456")
        
        self.assertTupleEqual(result, (ttl, 'value_1'))
        self.assertTrue(dal.RedisDal()._db.ttl("key456"), 20)
        
        
        #Update TTL
        ttlSLI = datetime.timedelta(hours=0, minutes=0, seconds=10)
        ttl = utilities._TTLSerialize(ttlSLI, ttlABS, datetime.datetime.max)
        
        dal.RedisDal().SetTTL("key456", ttlSLI)
        dal.RedisDal().UpdateTTL_ListItem("key456", ttl)
        result = dal.RedisDal().GetListItem("key456")
        
        self.assertTrue(dal.RedisDal()._db.ttl("key456"), 10)
        self.assertTupleEqual(result, (ttl, 'value_1'))
        
        #Delete TTL
        ttlSLI = config.DefaultSlidingExpiration
        ttlABS = config.DefaultAbsoluteExpiration
        ttl = utilities._TTLSerialize(ttlSLI, ttlABS, datetime.datetime.max)
        
        dal.RedisDal().UpdateTTL_ListItem("key456", ttl)
        dal.RedisDal().DeleteTTL("key456")
        
        result = dal.RedisDal().GetListItem("key456")
        
        self.assertTrue(dal.RedisDal()._db.ttl("key456"), -1)
        self.assertTupleEqual(result, (ttl, 'value_1'))
        
        print "AddListItemWithTTL_Test::OK"
        pass

# x = Test().ItemExist_Test()
# x = Test().AddListItem_Test()
x = Test().AddListItemWithTTL_Test()

 

