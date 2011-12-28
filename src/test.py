# -*- coding: utf-8 -*-
import plistlib
import logging
import logging.handlers
from urllib import unquote

def encrypt_des(key, msg):
    """
        @key: des encrypt key
        @msg: message string to encrypt, must not have '\0'
    """
    import Crypto.Cipher.DES as des
    length = len(msg)
    n = (int(length / 8) + 1) * 8
    padding_msg = msg.ljust(n, '\0')
    de = des.new(key)
    en_str = de.encrypt(padding_msg).encode("BASE64")
    del de
    return en_str

def decrypt_des(key, des_base64_string):
    import Crypto.Cipher.DES as des
    print "decoding:",des_base64_string
    en = des_base64_string.decode("BASE64")
    de = des.new(key)
    ret = de.decrypt(en)
    del de
    return ret.replace('\0', '')
    
def crack_url(url):
    tmp = url.split('?')
    query = ''.join(tmp[1:])
    
    method = tmp[0].split('/')[-1]
    method = method.replace(".do", '')
    params = crack_query_string(method, query)
    return method, params

def list_dedup(l):
    return list(set(l))

def add_info():
    import redis
    import json
    import time
    r1 = redis.Redis(host="localhost", port=6380, password="", db=220)
    data = [("A2", 0.91), ("A3", 0.87), ("A4", 0.38)]
    r1.set("bfdtest100:vav:A1", json.dumps(data))
    A1={"name":"A1",
        "iid":"A1",
        "url":"www.www.ww",
        "attr1":"asdfasdfasdfsdfasfdasdf"}
    A2={"name":"A2",
        "iid":"A2",
        "url":"www.www.ww",
        "attr1":"{}"}
    A3={"name":"A3",
        "iid":"A3",
        "url":"www.www.ww",
        "attr1":"{}"}
    A4={"name":"A4",
        "iid":"A4",
        "url":"www.www.ww",
        "attr1":"{}"}
    
    r1.set("bfdtest100:item:A1", json.dumps(A1))
    r1.set("bfdtest100:item:A2", json.dumps(A2))
    r1.set("bfdtest100:item:A3", json.dumps(A3))
    r1.set("bfdtest100:item:A4", json.dumps(A4))

    his = [["A1", time.time()],
           ["A2", time.time()]]

    r1.set("bfdtest100:bro:U01", json.dumps(his))

def code_compile():
    code = '''a=1
b=2
print "%s"%(a+b)
    '''
    obj = compile(code, "string", 'exec')
    print obj
    exec obj

def log_example():
    import logging
    import os
    # set the formatter, pid is the same in the process so, define it as static in the formatter
    formatter = logging.Formatter(''.join(('[%(levelname)s %(asctime)s @ ',
                               str(os.getpid()), '] - %(message)s')))
    
    logger = logging.getLogger()

    hdlr = logging.FileHandler("/tmp/log")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger


if __name__ == "__main__":
    logger = log_example()
    logger.info("Pong")
        




    
    