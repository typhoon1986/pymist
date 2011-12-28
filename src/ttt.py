# -*- coding: utf-8 -*-
from itertools import product, compress
def parse_query_string(query_str, and_symbol = '&', assign_symbol = '='):
    '''解析url query string得到参数和值的对
    
     参数:
         and_symbol : str, 连接多个参数的对的字符串
         assign_symbol : str，连接参数及其值的字符串
    
    返回值 ： dict
    '''
    param = {}
    if not query_str:
        return {}
    kv_pairs = query_str.split(and_symbol)
    k, v = None, None
    for kv in kv_pairs:
        if len(kv) > 0:
            try:
                k, v = kv.split(assign_symbol, 1)
            except:
                raise ValueError("invalid key-value pair: '%s' with separator '%s'"%(kv, assign_symbol))
            param[k] = v
    return param
def result_dedup(result):
    iids = []
    for r in result:
        iids.append(r[0])
    iid_fine = set()
    ret_val = []
    # 重复的iid权重相加，并规整权重
    max_w = 0
    for iid, w, info in result:
        if iid in iid_fine:
            continue
        if iids.count(iid) > 1 :
            # 将所有重复的的w相加
            total_w = 0
            for r in result:
                if r[0] == iid:
                    total_w += r[1]
            tmp = [iid, total_w, info]
            ret_val.append(tmp)
            iid_fine.add(iid)

        else:
            ret_val.append([iid, w, info])
            iid_fine.add(iid)

    return ret_val

def combinations2(iter):
    ret = list(( list(set(compress(iter,mask))) for mask in product(*[[0,1]]*len(iter)) ))
    ret.remove([])
    return ret

if __name__ == "__main__":
    print combinations2(["资讯"])