'''
Created on 04/mag/2014

@author: ppartes-v
'''

class GenericError(Exception):

    def __init__(self, message, inner=None):
        self.message = message
        self.inner = inner
    
        pass
    
    def GetInnerError(self):
        return self.inner

    def GetMessageError(self):
        return self.message
    
    
class NotProvidedError(GenericError):
    pass