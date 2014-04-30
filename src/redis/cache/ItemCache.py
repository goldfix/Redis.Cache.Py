'''
Created on 30/apr/2014

@author: ppartes-v
'''

class RedisCacheDal(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        pass

class RedisCacheException(Exception):
    '''
    Custom Redis.Cache Exception 
    '''
    def __init__(self, msg, innerException):
        self.message = msg
        self.innerException = innerException
        pass




