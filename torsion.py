# -*- coding: utf-8 -*-
"""
Created on Sat May 13 01:30:50 2017

@author: Hao Guo
"""
import numpy as np
from numpy import linalg 
from scipy.linalg import sqrtm

def torsion(Sigma, model, method='exact', max_niter=10000):
    n = Sigma.shape[0]    
    
    if model == 'pca':
        eigval, eigvec = linalg.eig(Sigma)
        idx = np.argsort(-eigval) 
        t = eigvec[:,idx]
        
    elif model == 'minimum-torsion':
        # C: correlation matrix
        sigma = np.sqrt(np.diag(Sigma))
        C = np.asmatrix(np.diag(1.0/sigma)) * np.asmatrix(Sigma) * np.asmatrix(np.diag(1.0/sigma))
        # Riccati root of correlation matrix
        c = sqrtm(C)
        if method == 'approximate':
            t = (np.asmatrix(sigma) / np.asmatrix(c)) * np.asmatrix(np.diag(1.0/sigma))
        elif method == 'exact':
            # initialize
            d = np.ones((n))
            f = np.zeros((max_niter))
            # iterating
            for i in xrange(max_niter):
                U = np.asmatrix(np.diag(d)) * c * c * np.asmatrix(np.diag(d))
                u = sqrtm(U)
                q = linalg.inv(u) * np.asmatrix(np.diag(d)) * c
                d = np.diag(q * c)
                pi = np.asmatrix(np.diag(d)) * q
                f[i] = linalg.norm(c - pi, 'fro')
                # if converge
                if i > 0 and abs(f[i]-f[i-1])/f[i] <= 1e-4:
                    f = f[0:i]
                    break
                elif i == max_niter and abs(f[max_niter]-f[max_niter-1])/f[max_niter] >= 1e-4:
                    print 'number of max iterations reached: n_iter = ' + str(max_niter)
            x = pi * linalg.inv(np.asmatrix(c))
            t = np.asmatrix(np.diag(sigma)) * x * np.asmatrix(np.diag(1.0/sigma))
    return t
    

    
