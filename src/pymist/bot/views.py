# Create your views here.
'''
Created on 2011-11-25

@author: wuyi
'''
import bot
import bot.mistbot
import logging
import urllib2
import urlparse

def do(request):
    meta = request.META
    method = meta['SCRIPT_NAME']
    
    if method is None or len(method) == 0:
        path = meta['PATH_INFO']
        method = path[1:path.find('.')]
    #param = util.parse_query_string(urllib2.unquote(meta['QUERY_STRING']))
    param = urlparse.parse_qs(urllib2.unquote(meta['QUERY_STRING']))
        
    logging.warning("method: %s", method)
    logging.warning("param: %s ", " ".join(param.get("q")))
    
    mybot = bot.mistbot.MistBot(method)
    body = mybot.get_answer(str(" ".join(param.get("q"))))
    response = HttpResponse(body)
    return response
