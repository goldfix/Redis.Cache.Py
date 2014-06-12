'''
Created on 11/giu/2014

@author: ppartes-v
'''

from unittest.case import TestCase
from redis import cache
from redis.cache import item, utilities
import datetime
from redis.cache.item import ItemCache
import time


class Test(TestCase):

    def __init__(self):
        print "\n"
    pass

    def GetFromCSharp(self):
        f = open("value_Text.txt", "rb")        
        value_Text = f.read()
        f.flush()
        f.close()

        
        t = item._ManagementItemsCache()
        result = t.GetItemCache("k1")
        
        self.assertTrue(result, value_Text)
        print "GetFromCSharp::OK"
        
        return result

    def SetToCSharp(self):
        f = open("value_Text.txt", "rb")        
        value_Text = f.read()
        f.flush()
        f.close()

        t = item._ManagementItemsCache()
        result = t.Add("k2", value_Text, datetime.timedelta(hours=48, minutes=00, seconds=00), datetime.timedelta(hours=96, minutes=00, seconds=00), True)

        print "SetToCSharp::OK"

        result = t.GetItemCache("k2")
        
        return result
    
    
    def SetToCSharp_2(self):
        f = open("value_Text.txt", "rb")        
        value_Text = f.read()
        f.flush()
        f.close()
        
        ic = ItemCache()
        ic.Key= "K3"
        ic.Value = value_Text
        ic.AbsoluteExpiration = datetime.timedelta(hours=13)
        ic.SlidingExpiration = datetime.timedelta(seconds=3)
        ic.Save(True)

        time.sleep(2)
        result_1 = ItemCache.GetItemCache("K3")
        self.assertTrue(result_1.Value, value_Text)

        time.sleep(2)
        result_1 = ItemCache.GetItemCache("K3")
        self.assertTrue(result_1.Value, value_Text)
                                
        time.sleep(4)
        result_1 = ItemCache.GetItemCache("K3")
        self.assertIsNone(result_1, None)
        
        
        print "SetToCSharp_2::OK"
        
        pass


# x = Test().GetFromCSharp()
# x = Test().SetToCSharp()
x = Test().SetToCSharp_2()






