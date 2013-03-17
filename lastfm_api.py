#!/usr/bin/env python

import json
import urllib2

class LastFmApi:
  def __init__(self, api_key=None):
    self.api_key = api_key
  def call(self, method=None, artist=None, limit=None, user = None, api_key=None):
    if api_key is None:
      api_key = self.api_key
    addr  = 'http://ws.audioscrobbler.com/2.0/?'
    aritst, user  = [urllib2.quote(x) if x else '' for x in [artist, user]]
    addr += '&api_key={}&method={}&artist={}&user={}&limit={}'.format(api_key, method, artist, user, limit)
    addr +='&format=json'
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

def main():
  pass

if __name__=='__main__':
  main()
