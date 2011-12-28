'''
Created on 2011-11-9

@author: wuyi
'''
import redis
from optparse import OptionParser
import time
import os
import pickle

def mv_str(r_source, r_dest, ptn="*", quiet=False, force=False):
    keys = r_source.keys(ptn)
    for k in keys:
        if r_dest.keys(k):
            if not force:
                if not quiet:
                    print "skipping %s"%k
                continue
        if not quiet:
            print "copying %s"%k
        r_dest.set(k, r_source.get(k))

def mv_list(r_source, r_dest, quiet):
    """ only for rpush queue
    """
    keys = r_source.keys("*")
    for k in keys:
        length = r_source.llen(k)
        i = 0
        while (i<length):
            print "add queue no.:%d"%i
            v = r_source.lindex(k, i)
            r_dest.rpush(k, v)
            i += 1



if __name__ == "__main__":
    usage = """usage: %prog [options] sourcehost:port:db desthost:port:db"""
    parser = OptionParser(usage=usage)

    parser.add_option("-q", "--quiet", dest="quiet",
                      default = False, action="store_true",
                      help="quiet mode")
    
    parser.add_option("-t", "--type", dest="type",
                      default = "normal",
                      help="available types: normal, lpoplist")
    
    parser.add_option("-p", "--key-pattern", dest="pattern",
                      default = "*",
                      help="keys to move")
    
    parser.add_option("-o", "--output", dest="output",
                      default = "",
                      help="output to a dump file")
    
    parser.add_option("-i", "--input", dest="input",
                      default = "",
                      help="input from a dump file")
    
    parser.add_option("-f", "--force", dest="force",
                      default = False, action="store_true",
                      help="force over write the dest keys")

    (options, args) = parser.parse_args()
    all = {}
    if options.output or options.input:
        if not len(args) == 1:
            print usage
            exit(1)
        if options.output and options.input:
            print "choose dump or load!"
            exit(1)
        
        if options.output:
#            if not os.access(options.output, os.os.W_OK):
#                print "can not access writable %s"%options.output
#                exit(1)
            # dump out the data
            print "dumping................"
            print "%s ---> %s"%(args[0], options.output)
            print "press any key to start, press Ctrl+C to exit"
            anykey = raw_input()
            try:
                shost, sport, sdb = args[0].split(':')
            except:
                print usage
                exit(1)
            r_source = redis.Redis(host=shost, db=sdb, password="", port=int(sport))
            if options.type == "normal":
#                all = r_source.mget(r_source.keys(options.pattern))
                for k in r_source.keys(options.pattern):
                    all[k] = r_source.get(k)
                fn = open(options.output, "wb")
                pickle.dump(all, fn)
                fn.close()
                print "Done!"
            else:
                print "queue not support!"
                exit(1)
            
        if options.input:
            if not os.access(options.input, os.R_OK):
                print "can not access readable %s"%options.input
                exit(1)
            print "loading from file............"
            print "%s ---> %s"%(options.input, args[0])
            print "press any key to start, press Ctrl+C to exit"
            anykey = raw_input()
        
            try:
                shost, sport, sdb = args[0].split(':')
            except:
                print usage
                exit(1)
            r_source = redis.Redis(host=shost, db=sdb, password="", port=int(sport))
            fn = open(options.input, "r")
            all = pickle.load(fn)
            fn.close()
            if not type(all) is dict:
                print "input file error!"
                exit(1)
            r_source.mset(all)
            print "Done!"
    else:
        if not len(args) == 2:
            print usage
            exit(1)
    
        source = args[0]
        dest = args[1]
        try:
            shost, sport, sdb = source.split(':')
            dhost, dport, ddb = dest.split(':')
        except:
            print usage
            exit(1)
    
        print "copying................"
        print "%s ---> %s"%(source, dest)
        print "press any key to start, press Ctrl+C to exit"
        anykey = raw_input()
        
        print "Please wait..."
        r_source = redis.Redis(host=shost, db=sdb, password="", port=int(sport))
        r_dest = redis.Redis(host=sdb, db=ddb, password="", port=int(dport))
        
        if options.type == "normal":
            mv_str(r_source, r_dest, options.pattern, options.quiet, options.force)
        elif options.type == "lpoplist":
            mv_list(r_source, r_dest, options.quiet)
        del r_source
        del r_dest
