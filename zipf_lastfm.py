#!/usr/bin/env python

import json
import urllib2
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

class LastFmApi:
  def __init__(self, api_key=None):
    self.api_key = api_key
  def call(self, method=None, artist=None, limit=None, user = None, api_key=None):
    if api_key is None:
      api_key = self.api_key
    addr ='http://ws.audioscrobbler.com/2.0/?'
    if method:
      addr+='&method='+method
    if artist:
      addr+='&artist='+artist.replace(' ','%20')
    if api_key:
      addr+='&api_key='+api_key
    if limit:
      addr+='&limit='+str(limit)
    if user:
      addr+='&user='+user
    addr+='&format=json'
    req = urllib2.Request(url=addr)
    api_page = urllib2.urlopen(req)
    return json.loads(api_page.read())

class LastFmUser:
  def __init__(self, api_key=None, user=None):
    self.lastApi  = LastFmApi(api_key)
    self.user     = user
  def get_top_plays(self, limit=30):
    doc = self.lastApi.call(method='user.gettopartists', user=self.user, limit=limit)
    return [a['playcount'] for a in doc['topartists']['artist']]

def user_experiment():
  api_key = None
  with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()
  username = 'hermes_thoth'
  N = 30
  user = LastFmUser(api_key, username)
  playcounts = user.get_top_plays(N)
  fplays = [float(i) for i in playcounts]
  total_counts = np.sum(fplays)
  f_counts = [ float(i)/total_counts for i in fplays]
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
    t = zipf_t(s, N)
    zipf_vals = [zipf(k,s,t) for k in range(1,N+1)]
    plt.loglog(range(1,N+1), zipf_vals)
    plt.xlim([0.0, float(N)])
    plt.xlabel('rank k')
    plt.ylabel('frequency f')
    plt.legend(lgnd,'upper right')
    print s, kl_divergence(f_counts, zipf_vals)

def plot_fit_zipf(f_counts, N, dom):
  def kl_optimize(s_arr):
    s = s_arr[0]
    t = zipf_t(s, N)
    zipf_vals = [zipf(k,s,t) for k in range(1,N+1)]
    return kl_divergence(f_counts, zipf_vals)
  res = opt.minimize(kl_optimize,[0.5],method='nelder-mead')
  print res.x
  kls = []
  for s in dom:
    t = zipf_t(s, N)
    zipf_vals = [zipf(k,s,t) for k in range(1,N+1)]
    kls.append(float(kl_divergence(f_counts, zipf_vals)))
  plt.plot(dom, kls)
  plt.xlabel('s')
  plt.annotate('global min at ~'+str(0.48) , xy=(res.x, res.fun), xytext=(res.x+res.x/30.0, res.fun+7*res.fun),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
  plt.legend(['KL divergence'], 'upper right')
  plt.xlim([dom[0], dom[-1]])
  plt.show()



def kl_divergence(p,q):
  return np.sum([pi*(np.log(pi)-np.log(qi)) for pi,qi in zip(p,q)])

def random_walk(username, N, limit, api_key):
  pass

def zipf_t(s,Nelem):
  ''' the inverse of the sum in the zipf distribution formula'''
  return 1/np.sum([1/(float(n)**s) for n in range(1,Nelem+1)])

def zipf(k, s, t):
  ''' the zipf frequency for element ranked k'''
  return t*(k**-s)

def main():
  user_experiment()
  #print kl_divergence([0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4])

if __name__=='__main__':
  main()
