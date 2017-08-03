# -*- coding: utf-8 -*-
"""
Created on Mon May 15 02:52:34 2017

@author: Hao Guo
"""

'''
risk budgeting for black-litterman-based portfolio
'''
import numpy as np 
import pandas as pd
import plotly
from plotly.graph_objs import Surface

obs_window = 900
roll_window = 30
T = (len(data) - obs_window)/30 # number of windows
N = ret.shape[1] # number of stocks

p_pc = np.asmatrix(np.zeros((N,T)))
p_mt = np.asmatrix(np.zeros((N,T)))
enb_pc = np.zeros(T)
enb_mt = np.zeros(T)
margin_risk = np.asmatrix(np.zeros((N,T)))
wgt = np.asmatrix(np.zeros((N,T)))
delta = 1.0
tau = 0.05

for t in xrange(T):
    Sigma = np.asmatrix(np.cov(ret.ix[t*roll_window:t*roll_window+obs_window].T))
    Mu = np.mean(ret.ix[t*roll_window:t*roll_window+obs_window],axis=0)
    weq = weights_mv(Mu, Sigma)
    ts = tau * Sigma
    P = np.vstack((weq.reshape((425)),weights_equal(Sigma)))
    Q = np.array([np.sum(weq.reshape((425))*Mu)*(np.random.random()*2-1),\
              np.mean(Mu)*(np.random.random()*2-1)])
    Omega = np.dot(np.dot(P,ts),P.T) * np.eye(Q.shape[0])
    w = weights_bl(weq, Sigma, P, Q, Omega, delta = 1.0, tau = 0.05)
    wgt[:,t] = w
    w = w.T   
    t_pc = torsion(Sigma, 'pca')
    t_mt = torsion(Sigma, 'minimum-torsion',  method='exact')
    p_pc[:,t], enb_pc[t] = EffectiveBets(w, Sigma, t_pc)
    p_mt[:,t], enb_mt[t] = EffectiveBets(w, Sigma, t_mt)
    margin_risk[:,t] = w.reshape((N,1)) * np.asarray(np.asmatrix(Sigma)*np.asmatrix(w).T) \
                       / (np.asmatrix(w) * np.asmatrix(Sigma) * np.asmatrix(w).T)
    

import plotly
from plotly.graph_objs import Surface

plotly.offline.plot([
    dict(z=np.sort(p_mt,axis=0)[::-1], type='surface'),
    dict(z=np.sort(wgt,axis=0)[::-1], showscale=False, opacity=0.9, type='surface')])

'''
plotly.offline.plot([
    dict(z=np.sort(p_pc,axis=0)[::-1], type='surface'),
    dict(z=np.sort(wgt,axis=0)[::-1], showscale=False, opacity=0.9, type='surface')])
    
plotly.offline.plot([
    dict(z=np.sort(margin_risk,axis=0)[::-1], type='surface'),
    dict(z=np.sort(wgt,axis=0)[::-1], showscale=False, opacity=0.9, type='surface')])
    
'''
