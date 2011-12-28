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
'''

import redis

class RedisJsonFS(object):
    def __init__(self, host="127.0.0.1", ):
        pass
    
    
