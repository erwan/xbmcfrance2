"""
 Copyright (c) 2007 Daniel Svensson, <dsvensson@gmail.com>

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

import re
import urllib2
import cookielib
import os.path
import time

from xml.sax.saxutils import escape

import xbmcutils.net

class VideoStreamError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class PrivilegeError(Exception):
  def __init__(self):
    self.value = 'Insufficient permissions, operation aborted.'
  def __str__(self):
    return repr(self.value)

class France2:
  """France2 web grabber class."""

  PLAYER_URL = "http://jt.france2.fr/player/%program%/index-fr.php"
  PROGRAMS = [
    ["8h", "Journal de 8H"],
    ["13h", "Journal de 13H"],
    ["20h", "Journal de 20H"]
  ]

  def __init__(self):
    self.base_path = os.getcwd().replace(';','')
    # mms://sdmc.contents.edgestreams.net/horsgv/regions/siege/infos/f2/20h/HD_20h_20080925.wmv
    self.stream_pattern = re.compile('src="(mms://[^"]+)"')
    self.name_pattern = re.compile('<div class="editiondate"><h1>([^<>]+)</h1></div>')

    # Cache info so we don't retrieve it every time
    self.cache = {
      
    }

    # Callback related stuff
    self.report_hook = None
    self.report_udata = None
    self.filter_hook = None
    self.filter_udata = None

  def retrieve(self, url, data=None, headers={}):
    """Downloads an url."""
    return xbmcutils.net.retrieve (url, data, headers,
                                   self.report_hook,
                                   self.report_udata)

    return data

  def get_lastjt(self, program):
    """Get the URL for the most recent 'program'"""
    if program in self.cache:
      return self.cache[program]

    page_url = self.PLAYER_URL.replace("%program%", program)
    html = self.retrieve(page_url)
    match = self.stream_pattern.search(html)
    if match != None:
      stream_url = match.group(1)
    match2 = self.name_pattern.search(html)
    if match2 != None:
      name = match2.group(1)
    self.cache[program] = {
      "url": stream_url,
      "name": name
    }
    return self.cache[program]
