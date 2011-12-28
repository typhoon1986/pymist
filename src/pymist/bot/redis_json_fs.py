'''
Created on 2011-11-25

@author: wuyi

redis_json_fs: using k-v db to define some ops like a file system.
ops are:
@ mkdir
@ listdir
@ rmdir
@ add2dir

@ mkfile
@ readfile
@ rmfile
@ writefile

@ mv
@ cp
'''

import redis
import pickle

class RedisJsonFS(object):
    def __init__(self, host="127.0.0.1", port=6379, db=0, passwd=""):
        self.r = redis.Redis(host=host, port=port, password=passwd, db=db)
        
    def _check_path(self, path):
        if not type(path) is str:
            return -1
        if path[0] != '/' or path == '/':
            return -2
        
        return 0
    
    def _path2key(self, path):
        return path.replace("/", ":")
        
    
    def mkdir(self, dirname):
        if self._check_path(dirname) != 0:
            return -1
        k = self.r.keys(self._path2key(dirname))
        if k:
            if self.r.type(k) == "set":
                return -1
            else:
                raise Exception, "dir must be a set type"
        else:
            pass
    
    def listdir(self, dirname):
        pass
    
    def rmdir(self, dirname):
        pass
    
    def add2dir(self, dirname, filename):
        pass
    
    def mkfile(self, path):
        pass
    
    def readfile(self, path):
        pass
    
    def rmfile(self, path):
        pass
    
    def writefile(self, path):
        pass
    
    def getcwd(self):
        pass
    
