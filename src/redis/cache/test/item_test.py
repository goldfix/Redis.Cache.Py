'''
Created on 11/giu/2014

@author: ppartes-v
'''

from unittest.case import TestCase
from redis import cache
from redis.cache import item, utilities
import datetime


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


# x = Test().GetFromCSharp()
x = Test().SetToCSharp()






