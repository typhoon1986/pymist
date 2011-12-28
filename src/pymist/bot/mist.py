# -*- coding: utf-8 -*-
'''
Created on Oct 11, 2011

@author: wuyi
'''

from numpy import dot, array
from numpy.linalg import norm
from numpy.random import rand
import numpy
import scipy
import scipy.sparse as sparse
import time

class MistSparse():
    def __init__(self, sps_mtrx):
        if not type(sps_mtrx) == sparse.lil.lil_matrix:
            raise TypeError, "must input a lil_matrix"
        self.mtrx = sps_mtrx
    
    def get_shape(self):
        return self.mtrx.shape
    
    def avg_row(self, i):
        A = self.mtrx.getrowview(i)
        return A.mean()
    
    def avg_col(self, i):
        A = self.mtrx.getcol(i)
        return A.mean()
    
    def sum_row(self, i):
        A = self.mtrx.getrowview(i)
        return A.sum()
    
    def sum_col(self, i):
        A = self.mtrx.getcol(i)
        return A.sum()
    
    def cossim_row(self, i, j):
        A = self.mtrx.getrowview(i)
        B = self.mtrx.getrowview(j)
#        a1 = A.toarray()[0]
#        b1 = B.toarray()[0]
#        print dot(a1,b1)
        dp = dot(A, B.T).data
        if not dp:
            return 0
        else:
            dp = dp[0]
        np = norm(A.todense()) * norm(B.todense())
        sim = dp / np
        return sim
    
    def corrsim_row(self, i, j):
        # correlation based
        pass
    
    def adjcossim_row(self, i, j):
        # adjusted cosine
        pass
    
    def cossim_col(self, i, j):
        # cosine based
        A = self.mtrx.getcol(i)
        B = self.mtrx.getcol(j)

        dp = dot(A.T, B).data
        if not dp:
            return 0
        else:
            dp = dp[0]
        np = norm(A.todense()) * norm(B.todense())
        sim = dp / np
        return sim


    
def main():
    i = (rand(100)*5).astype(int)
    j = (rand(100)*5).astype(int)
    print dot(i, j)
    
    A = sparse.lil_matrix((10000,20000))
    A[0,:100] = i
    print A.data
    
    import pickle
    import zlib
    print "start dumping..."
    str = pickle.dumps(A)

    zipcode = zlib.compress(str)
    print len(str) / len(zipcode)
    
    str = zlib.decompress(zipcode)
    print "loading..."
    B = pickle.loads(str)
    print type(B)


if __name__ == "__main__":
    main()
