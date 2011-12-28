'''
Created on 2011-11-10

@author: wuyi
'''
import json
import logging
import re

# dependences
import memcache
import redis

class MistSet(object):
    def __init__(self, serverlist=["127.0.0.1:11211"]):
        """ python-memcache can store any object, forget the serialization, you stupid!
            should we make it thread safe?
        """
        self.mc = memcache.Client(serverlist, debug=1)
        
    def get_set_size(self, key):
        set_obj = self.mc.get(key)
        if not set_obj:
            return 0
        else:
            return len(set_obj)
        
    def add(self, key, value):
        code = self.mc.add(key, set(value))
        if not code:
            set_obj = self.mc.get(key)
            
            if not type(set_obj) is set:
                raise Exception, "get data is not a set type, maybe this is due to a key conflict"
            set_obj.add(value)
            code = self.mc.set(key, set_obj)
        return code

    def get(self, key):
        return self.mc.get(key)
        
    def remove(self, key, value):
        set_obj = self.mc.get(key)
        if not set_obj:
            # no data in the key, clear the key
            self.mc.delete(key)
        else:
            set_obj.remove(value)
            self.mc.set(key, set_obj)
    
    def clear_set(self, key):
        self.mc.delete(key)
        

class MistDB(object):
    """ fast k-v databases
        store all the keys in several pages, default page size is 100
        store current page count
        
        do 'set' will: 1. set k-v 
                       2. add the key to key list(search from first page to add)
                       3. if pages are all full, add a new page
        do 'delelte' will: 1. delete k-v
                           2. delete the key in the key list
                               
    """
    
    def __init__(self, name, serverlist=["127.0.0.1:11211"], pgsize=100):
        self.mc = memcache.Client(serverlist, debug=1)

        
        # put all keys in several k-v, each has [pgsize] number of keys stored 
        self.pgsize = pgsize
        self.cached_keys = MistSet(serverlist)
        
        # the db name
        self.name = name
        self.pages = self._get_pages()
    
        self.key_count = self.get_key_count()
    
    def _get_pages(self):
        key = ':'.join([self.name, "pages"])
        pg = self.mc.get(key)
        if pg is None:
            return -1
        return pg
    
    def _set_pages(self, pages):
        key = ':'.join([self.name, "pages"])
        self.mc.set(key, pages)
        
    def _clear_pages(self):
        key = ':'.join([self.name, "pages"])
        self.mc.delete(key)
        self.pages = -1

    
    def _make_cached_keys_key(self, name, page):
        return ':'.join([self.name, "keylist", str(page)])

    def _update_cached_keys(self, key):
        """ put 'key' into the key list of the DB
            @key : new added key
        """
        if self.pages == -1:
            # no data yet stored
            self.pages = 0
        # find the first page that has space.
        # NOTICE: we do not care about sequence, wherever it stores
        for pg in range(0, self.pages + 1):
            kl_key = self._make_cached_keys_key(self.name, pg)
            sz = self.cached_keys.get_set_size(kl_key)
            if sz < self.pgsize:
                # 
                self.cached_keys.add(kl_key, key)
                return pg
        # need to add a page
        self.pages += 1
        self._set_pages(self.pages)
        kl_key = self._make_cached_keys_key(self.name, self.pages)
            
        # update the new key to a set
        self.cached_keys.add(kl_key, key)
        return self.pages

    def _remove_cached_keys(self, key):
        pg = self.get_key_page(key)
        kl_key = self._make_cached_keys_key(self.name, pg)
        self.cached_keys.remove(kl_key, key)
    
    def keys(self, page):
        if page > self.pages or self.pages == -1:
            return []
        kl_key = self._make_cached_keys_key(self.name, page)
        pg_keys = self.cached_keys.get(kl_key)
        if not pg_keys:
            return []
        return pg_keys

    def find_matched_keys(self, regex):
        matched = []
        flt = re.compile(regex)
        for pg in range(0, self.pages+1):
            for key in self.keys(pg):
                m = flt.match(key)
                if m:
                    matched.append(m.group(0))
        return matched
    
    def set(self, key, value, t=0):
        # TODO: validate input
        
        # update cached keys first then self.pages will be updated
        page = self._update_cached_keys(key)
        # the key is stored at page
        data ={"value":value,
               "page": page}
        self.mc.set(key, data, t)
    
    def get(self, key):
        data = self.mc.get(key)
        if not data:
            return None
        else:
            return data.get("value", None)

    def get_key_page(self, key):
        data = self.mc.get(key)
        if not data:
            return -1
        else:
            return data.get("page", None)
    
    def get_key_count(self):
        c = 0
        for pg in range(0, self.pages+1):
            c += len(self.keys(pg))
        return c
    
    def delete(self, key):
        
        self._remove_cached_keys(key)
        self.mc.delete(key)

    def flush_db(self):
        """ clear all data in the db
        """
        for pg in range(0, self.pages + 1):
            self.mc.delete_multi(self.keys(pg))
            kl_key = self._make_cached_keys_key(self.name, pg)
            self.cached_keys.clear_set(kl_key)
        # clear pages info of the db
        self._clear_pages()
        
    def flush_all(self):
        self.mc.flush_all()
            
class MistRedis(redis.Redis):
    """ use redis will be faster!
    """
    def get_key_count(self):
        return self.dbsize()
    
    def get_key_page(self):
        pass

if __name__ == "__main__":
    # some tests
#    db = MistDB("db1")
#    db.flush_all()
#    db.flush_db()

#    print db.pages
#    print db.keys(0)
#    
#    
    db = MistDB("db1")
    db.flush_db()

    for i in range(1,164):
        key = "info%d"%i
        db.set(key, "some string")


    print db.get_key_count()
#    print db.delete("info37")
    #db.delete("OOOOOOOOOOOOOOOOOOOOOOOO")#, "JJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    kl = db.keys(page=1)
    print kl
    print len(kl)
#    print kl.index("info38")
#    print db.get("info38")
##    kl = db.keys(1)
##    print len(kl)
#    print db.pages