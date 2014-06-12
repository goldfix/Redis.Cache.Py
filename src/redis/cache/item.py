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
from redis.cache import config, utilities, errors, dal
import datetime


class ItemCache(object):
    
    def __init__(self):
        self.Key = ""
        self.Value = ""
        
        self.SlidingExpiration = config.DefaultSlidingExpiration
        self.AbsoluteExpiration = config.DefaultAbsoluteExpiration
        
        pass
    
    def Save(self, forceOverWrite):
        m = _ManagementItemsCache()
        result = m.Add(self.Key, self.Value, self.SlidingExpiration, self.AbsoluteExpiration, forceOverWrite)
        return result
    
    @staticmethod
    def AddItemCache(itemsCache, forceOverWrite):
        
        if(itemsCache is None or not(itemsCache is ItemCache) ):
            raise errors.ArgumentError("Parameter is invalid (itemsCache)")
        
        return itemsCache.Save(forceOverWrite)
        pass
    
    @staticmethod
    def AddItem(key, value, forceOverWrite, slidingExpiration=None, absoluteExpiration=None):
        ic = ItemCache()
        ic.Key= key
        ic.Value = value
        
        if(absoluteExpiration is None):
            ic.AbsoluteExpiration = absoluteExpiration
        
        if(slidingExpiration is None):
            ic.SlidingExpiration = slidingExpiration
            
        return ic.Save(forceOverWrite)
    
    @staticmethod
    def DeleteItem(key):
        m = _ManagementItemsCache()
        return m.Delete(key)
        
    @staticmethod
    def ExistItem(key):
        m = _ManagementItemsCache()
        return m.Exist(key)
        
    @staticmethod
    def GetItemCache(key):
        m = _ManagementItemsCache()
        return m.GetItemCache(key)



class _ManagementItemsCache(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.DefaultAbsoluteExpiration = config.DefaultAbsoluteExpiration
        self.DefaultSlidingExpiration = config.DefaultSlidingExpiration
        self._TypeStorage = config.TypeStorage
        
        pass


    def _SetTTL(self, key, slidingExpiration, absoluteExpiration, dal):
        result = False
        
        if(slidingExpiration != utilities._NO_EXPIRATION or absoluteExpiration != utilities._NO_EXPIRATION):

            if(slidingExpiration != utilities._NO_EXPIRATION):
                result = dal.SetTTL(key, slidingExpiration)
                pass
            else:
                if(absoluteExpiration != utilities._NO_EXPIRATION):
                    result = dal.SetTTL(key, absoluteExpiration)
                    pass
                else:
                    # Continue...
                    pass
                pass
            pass
        else:
            # Continue...
            pass
        
        return  result
        pass


    def Add(self, key, value, slidingExpiration, absoluteExpiration, forceOverWrite):
        if(key is None or key.strip()==""):
            raise errors.ArgumentError("Parameter is invalid (key)")
        
        if(slidingExpiration != utilities._NO_EXPIRATION and absoluteExpiration != utilities._NO_EXPIRATION) and (slidingExpiration>=absoluteExpiration):
            raise errors.GenericError("Sliding Expiration is greater or equal than Absolute Expiration.")
            pass
        
        _dal = dal._RedisDal()
        ttl = utilities._TTLSerialize(slidingExpiration, absoluteExpiration, datetime.datetime.max)
        if(self._TypeStorage==config.UseList):
            if(not forceOverWrite):
                if(_dal.ItemExist(key)):
                    raise errors.GenericError("This Item Exists.")
                    pass
                else:
                    # Continue...
                    pass
                pass
            else:
                if(_dal.ItemExist(key)):
                    _dal.ItemDelete(key)
                    pass
                else:
                    # Continue...
                    pass
                pass
            pass
        
            result = _dal.AddListItemWithTTL(key, value, ttl)
            self._SetTTL(key, slidingExpiration, absoluteExpiration, _dal)
            return result
        else:
            raise errors.GenericError("NotImplementedException.")
            pass
        pass

    
    def GetItemCache(self, key):
        if(key is None or key.strip()==""):
            raise errors.ArgumentError("Parameter is invalid (key)")
        
        _dal = dal._RedisDal()
        result = _dal.GetListItem(key)
        
        if(result!=None and len(result)>0):
            ttl_Dt = utilities._TTL_DT_DeSerialize(result[0])
            ttl_Ts = utilities._TTL_TS_DeSerialize(result[0])
            
            if(utilities._TTL_Is_Expired(ttl_Dt)):
                _dal.DeleteTTL(key)
                return None
            else:
                # Update SLI TTL on Redis...
                if(ttl_Dt[0] != datetime.datetime.max):
                    ttl = utilities._TTLSerialize(ttl_Ts[0], ttl_Ts[1], ttl_Dt[1])
                    _dal.UpdateTTL_ListItem(key, ttl)
                    _dal.SetTTL(key, ttl_Ts[0])
                else:
                    pass
                
                ic = ItemCache()
                ic.SlidingExpiration = ttl_Ts[0]
                ic.AbsoluteExpiration = ttl_Ts[1]
                ic.Key = key
                ic.Value = result[1]
                return ic
        else:
            return None
            
        pass

    def GetValue(self, key):
        if(key is None or key.strip()==""):
            raise errors.ArgumentError("Parameter is invalid (key)")
        
        result  = self.GetItemCache(key)
        if(result!=None):
            return result.Value
        else:
            return None
        pass

    
    def Exist(self, key):
        if(key is None or key.strip()==""):
            raise errors.ArgumentError("Parameter is invalid (key)")
        
        _dal = dal._RedisDal()
        return _dal.ItemExist(key)

    def Delete(self, key):
        if(key is None or key.strip()==""):
            raise errors.ArgumentError("Parameter is invalid (key)")
        
        _dal = dal._RedisDal()
        return _dal.DeleteTTL(key)
    
    
    
    
    
    


