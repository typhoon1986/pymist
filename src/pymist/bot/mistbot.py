
'''
Created on 2011-11-9

@author: wuyi
'''
import os, sys
import storage
import logging
import re
import random

class MistBot():
    def __init__(self, dbname=None):
        # init storage
        self.db = storage.MistDB(dbname)
        if self.db.get_key_count() == 0:
            # db is empty
            self.db = None
        
    
    def set_db(self, dbname):
        tmpdb = storage.MistDB(dbname)
        if tmpdb.get_key_count() == 0:
            return False
        else:
            self.db = tmpdb
            return True
    
    def import_text(self, filepath, dbname):
        """ import conversation text, format is like
            K: [question regex]
            V1: [answer]
            V2: [answer]
            ...
        """
        tmpdb = MistDB(dbname)
        fn = open(filepath, "r")
        key = ""
        v = []
        got_key = False
        for line in fn.readlines():
            if line.startswith("K:"):
                if key and v:
                    # save last k-v pair
                    logging.info("adding :%s", key)
                    logging.info("value: %s", v)
                    tmpdb.set(key, v)
                    key = ""
                    v = []
                else:
                    raise Exception, "text format error"
                # next key
                key = line.replace("K: ", "")
            elif line.startswith("V:"):
                v.append(line.replace("V: ", ""))
        
        fn.close() 
    
    def get_answer(self, question):
        if not self.db:
            return None
        # db key is question pattern
        key = ""
        for pg in self.db.pages:
            for ptn in self.db.keys(pg):
                if re.match(ptn, question):
                    # got matched question pattern
                    key = ptn
                    break
            if key:
                break
        # return a random answer
        return random.choice(self.db.get(key))
                    
    
if __name__ == "__main":
    bot = MistBot()
    bot.import_text(sys.argv[1], sys.argv[2])
