#!/usr/bin/env python

import numpy as np
import unittest

def kl_divergence(p,q):
  return np.sum([pi*(np.log(pi)-np.log(qi)) for pi,qi in zip(p,q)])
def kl_optimize(s, p):
    N = len(p)
    t = zipf_t(s, N)
    zipf_vals = [zipf(k,s,t) for k in range(1,N+1)]
    return kl_divergence(p, zipf_vals)

def zipf_t(s,Nelem):
  ''' the inverse of the sum in the zipf distribution formula'''
  return 1/np.sum([1/(float(n)**s) for n in range(1,Nelem+1)])

def zipf(k, s, t):
  ''' the zipf frequency for element ranked k'''
  return t*(k**-s)

class SuTest(unittest.TestCase):
  def test_kl(self):
    self.assertEqual(kl_divergence([0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4]), 0.0)
  def test_kl_optimize(self):
    f_counts_str = ['0.11', '0.07', '0.06', '0.05', '0.04', '0.04', '0.04', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.03', '0.02', '0.02', '0.02', '0.02', '0.02', '0.02', '0.02', '0.02', '0.02']
    f_counts = [float(x) for x in f_counts_str]
    import scipy.optimize as opt
    res = opt.minimize(kl_optimize, [0], args=([f_counts]), method='nelder-mead')
    my_eps = 10**-6
    self.assertTrue(np.abs(res.x-np.array([0.4765])) < my_eps)

def main():
  unittest.main()

if __name__=='__main__':
  main()
