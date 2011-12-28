'''
Created on 2011-11-8

@author: wuyi

NOTICE:
iid(itemid) := [A-Za-z0-9-_]
uid(userid) := [A-Za-z0-9-_]
sim < 1.0
'''
import logging
from numpy import dot, array
import scipy.sparse as sparse

import mist
import storage

DEFAULT_N_USERS = 1000
DEFAULT_N_ITEMS = 10000



class Rcmdr():
    def __init__(self, name, ustep=100, istep=1000, cache=1024):
        # recommender name
        self.name = name

        self.usern = 0
        self.itemn = 0
        
        self.max_users = DEFAULT_N_USERS
        self.max_items = DEFAULT_N_ITEMS
        self.action = sparse.lil_matrix(self.max_users, self.max_items)
        
        self.ustep = ustep
        self.istep = istep
        
        self.n_cache = cache
        
        self.db = storage.MistDB()
    ''' -----------------------------------------------------------------------------------------
        data collection functions
    '''
    def add_user(self, uid, update=False):
        if not self.users.has_key(uid):
            self.users[uid] = self.usern
        else:
            if update:
                self.users[uid] = self.usern
            else:
                return False
        self.usern += 1
        return True
    
    def add_item(self, iid, update=False):
        if not self.items.has_key(iid):
            self.items[iid] = self.itemn
        else:
            if update:
                self.items[iid] = self.itemn
            else:
                return False
        self.itemn += 1
        return True
    
    def add_users(self, uids, update=False):
        for uid in uids:
            if not self.add_user(uid):
                pass
            
    def import_users_from_scv(self, filepath):
        pass
    
    def add_items(self, iids, update=False):
        for iid in iids:
            self.add_item(iid)
    
    def import_items_from_csv(self, filepath):
        pass
    
    def action(self, uid, iid, rating):
        '''save action to self.action
        '''
        if not self.action:
            return False
        u = self.users.get(uid)
        i = self.items.get(iid)
        self.action[u, i] += rating
        # mark as dirty, cause we need to re-caculate
        self.set_dirty(iid)
        
    def import_action_from_csv(self, filepath):
        pass
    
    ''' -----------------------------------------------------------------------------------------
        storage manage
    '''
        
    def init_rating_matrix(self, nusers, nitems):
        
        
        pass
    
    def set_dirty(self, iid): 
        pass
    
    def rm_dirty(self, iid):
        pass
    
    def is_dirty(self, iid):
        return True
    
    def gen_sim_key(self, iid1, iid2):
        return ''.join((iid1, ':', iid2))
    
    def crack_key(self, key):
        return key.split(':')
    
    def save_simi(self, iid1, iid2, sim):
        ''' save the i,j,sim to storage
        '''
        key = self.gen_sim_key(iid1, iid2)
        # TODO: save it to a storage!
    def get_stored_simi(self, key):
        if not self.has_key(key):
            return None
        else:
            return 0
    
    def has_key(self, key):
        ''' return whether we have the key in the storage
        '''
        return False
    
    def keys(self):
        ''' return all keys in the storage
        '''
        return None
    
    def get_similarity(self, iid1, iid2):
        key = self.gen_sim_key(iid1, iid2)
        if self.has_key(key):
            if not (self.is_dirty(iid1) and self.is_dirty(iid2)) :
                return self.get_stored_simi(key)
                
        # need to calculate:
        mst = mist.MistSparse(self.action)
        i = self.items.get(iid1, -1)
        j = self.items.get(iid2, -1)
        if i < 0 or j < 0:
            logging.error("item not added to me!")
        sim = mst.cossim_col(i, j)
        # save it
        self.save_simi(iid1, iid2, sim)
        self.rm_dirty(iid1)
        self.rm_dirty(iid2)

        return sim
    
    def calculate_all(self):
        ''' update all similarity
        '''
        pass
    
    def recalculate(self):
        ''' recalculate all stored simi
            you should never call it when nessesary
        '''
        mst = mist.MistSparse(self.action)
        for k in self.keys():
            iid1, iid2 = self.crack_key(k)
            
            i = self.items.get(iid1, -1)
            j = self.items.get(iid2, -1)
            if i < 0 or j < 0:
                raise Exception, "item not added to me!"
            sim = mst.cossim_col(i, j)
            self.save_simi(iid1, iid2, sim)
            
    
    def recommend(self, iid, topN):
        for i in self.items.keys():
            pass
        
    
    def fast_recommend(self, iid, topN):
        ''' use only cached simi
        '''
        pass