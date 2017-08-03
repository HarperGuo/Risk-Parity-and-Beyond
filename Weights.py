# -*- coding: utf-8 -*-
"""
Created on Sat May 13 14:40:29 2017

@author: Hao Guo
"""
import numpy as np 
import cvxopt
from numpy.linalg import inv


def weights_equal(Sigma):
    n = Sigma.shape[1]
    w = np.ones((n))*1.0/n
    return w
    
def weights_mv(Mu, Sigma, delta=1.0, short_selling=False):
    n = Sigma.shape[1]
    Mu = np.asmatrix(Mu)
    Sigma = np.asmatrix(Sigma)
    if short_selling == False:
        obj = cvxopt.matrix(delta/2*Sigma)
        q = cvxopt.matrix(Mu, (n,1))
        A = cvxopt.matrix(1.0, (1,n))
        b = cvxopt.matrix(1.0)
        G = cvxopt.matrix(0.0, (n,n))
        G[::n+1] = -1.0
        h = cvxopt.matrix(0.0, (n,1))
        w = cvxopt.solvers.qp(obj, -q, G, h, A, b)['x']
        w = np.array(w)
    else:
        ones = np.matrix(np.ones(n))
        w = 1/delta*inv(Sigma)*(Mu+(delta-ones*inv(Sigma)* Mu.T)/(ones*inv(Sigma)* ones.T)*ones).T
    return w
    
def weights_bl(w_eq, Sigma, P, Q, Omega, delta=1.0, tau=0.05, short_selling=False):
    n = Sigma.shape[1]
    Sigma = np.asmatrix(Sigma)
    pi = delta * Sigma * np.asmatrix(w_eq)
    ts = tau * Sigma
    # Compute posterior estimate of the mean
    Mu_bar = inv(inv(ts)+np.asmatrix(P.T)*inv(Omega)*np.asmatrix(P)) \
            * (inv(ts)*pi + np.asmatrix(P.T)*inv(Omega)*np.asmatrix(Q).T)
    # Compute posterior estimate of the uncertainty in the mean
    posteriorSigma = inv(inv(ts)+np.asmatrix(P.T)*inv(Omega)*np.asmatrix(P))
    # Compute posterior weights based on uncertainty in mean
    if short_selling == False:
        obj = cvxopt.matrix(delta/2*posteriorSigma)
        q = cvxopt.matrix(Mu_bar, (n,1))
        A = cvxopt.matrix(1.0, (1,n))
        b = cvxopt.matrix(1.0)
        G = cvxopt.matrix(0.0, (n,n))
        G[::n+1] = -1.0
        h = cvxopt.matrix(0.0, (n,1))
        w = cvxopt.solvers.qp(obj, -q, G, h, A, b)['x']
        w = np.array(w)
    else:
        Sigma_bar = inv(Sigma + posteriorSigma)
        w = 1/delta*inv(Sigma_bar)*inv(posteriorSigma)\
                     *(inv(ts)*pi + np.asmatrix(P.T)*inv(Omega)*np.asmatrix(Q))
    return w