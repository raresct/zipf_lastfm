#!/usr/bin/env python

import stats_util as su
import lastfm_api as last
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def user_experiment():
  api_key = None
  with open('api_key/api_key.txt', 'r') as f:
    api_key = f.read().strip()
  username = 'hermes_thoth'
  N = 30
  user = last.LastFmUser(api_key, username)
  playcounts = user.get_top_plays(N)
  fplays = [float(i) for i in playcounts]
  print([str(int(i)) for i in fplays])
  total_counts = np.sum(fplays)
  f_counts = [ float(i)/total_counts for i in fplays]
  print(['%.2f' % i for i in f_counts])
  some_zipf_dom = [0.25, 0.5, 0.75, 1.0]
  fit_zipf_dom = np.arange(0.25, 0.75, 0.01)
  plot_some_zipf(f_counts, N, some_zipf_dom)
  plt.figure()
  plot_fit_zipf(f_counts, N, fit_zipf_dom)
  plt.show()

def plot_some_zipf(f_counts, N, dom):
  plt.loglog(range(1,N+1), f_counts, 'r+')
  lgnd = ['play frequencies']+['s='+str(s) for s in dom]
  for s in dom:
    t = su.zipf_t(s, N)
    zipf_vals = [su.zipf(k,s,t) for k in range(1,N+1)]
    plt.loglog(range(1,N+1), zipf_vals)
    plt.xlim([0.0, float(N)])
    plt.xlabel('rank k')
    plt.ylabel('frequency f')
    plt.legend(lgnd,'upper right')
    #print s, su.kl_divergence(f_counts, zipf_vals)

def plot_fit_zipf(f_counts, N, dom):
  res = opt.minimize(su.kl_optimize, [0], args=([f_counts]))
  kls = []
  for s in dom:
    t = su.zipf_t(s, N)
    zipf_vals = [su.zipf(k,s,t) for k in range(1,N+1)]
    kls.append(float(su.kl_divergence(f_counts, zipf_vals)))
  plt.plot(dom, kls)
  plt.xlabel('s')
  #plt.annotate('global min at ~'+str(0.48) , xy=(res.x, res.fun), xytext=(res.x+res.x/30.0, res.fun+7*res.fun),
  #            arrowprops=dict(facecolor='black', shrink=0.05),
  #         )
  plt.legend(['KL divergence'], 'upper right')
  plt.xlim([dom[0], dom[-1]])
  plt.show()

def random_walk(username, N, limit, api_key):
  pass

def main():
  user_experiment()

if __name__=='__main__':
  main()
