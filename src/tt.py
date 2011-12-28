# -*- coding: utf-8 -*-
import logging
import sys
import re

def log_example():
    import os
    # set the formatter, pid is the same in the process so, define it as static in the formatter
    formatter = logging.Formatter(''.join(('log [%(levelname)s %(asctime)s @ ',
                               str(os.getpid()), '] - %(message)s')))
    
    logger = logging.getLogger()

    hdlr = logging.FileHandler("/tmp/log")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

if __name__ == "__main__":
    #count got gid: None, sdgid: 122.143.2.112.1322736577998.7
    #count got gid: 7914c0d000007ea500019bfd4ed97510, sdgid: 121.20.178.29.1322739372025.3
    bigset = set()
    sd_set = set()
    mather = re.compile(r".*count got gid: [0-9a-z]{32}, sdgid:.*")
    find = re.compile(r"[0-9a-z]{32}")
    find2 = re.compile(r"sdgid: [0-9\.]*")

    all_linen = 0
    gid_pv = 0
    fn = open(sys.argv[1], "r")
    print sys.argv[1]
    for l in fn.readlines():
        all_linen += 1
        sdid = find2.findall(l)[0]
        sd_set.add(sdid)
        if mather.match(l):
            gid_pv += 1
            gid = find.findall(l)[0]
            bigset.add(gid)
    
    
    print "total visit:%d"%all_linen
    print "gid visit count: %s"%gid_pv
    
    print "bfd pv rate: %f"%(float(gid_pv)/float(all_linen))
    
    sd_c = len(sd_set)
    print "sdgid count %d"%sd_c
    gid_c = len(bigset)
    print "gid count %d"%gid_c
    print "rate: %f"%(float(gid_c)/float(sd_c))
    
    fn.close()
    
    