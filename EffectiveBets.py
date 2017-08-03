# -*- coding: utf-8 -*-
"""
Created on Sat May 13 01:43:22 2017

@author: Hao Guo
"""

    
def EffectiveBets(w, Sigma, t):
    w = np.asmatrix(w)
    p = np.asmatrix(np.asarray(linalg.inv(t.T) * w.T) * np.asarray(t * Sigma * w.T)) / (w * Sigma * w.T)  
    enb = np.exp(- p.T * np.log(p))
    return p, enb