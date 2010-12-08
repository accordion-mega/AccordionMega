""" Python CDDB-Access
Access a freedb service from Python.
"""

import urllib
import os
import getpass
import string
import re
import socket
try:
	socket.setdefaulttimeout(30) #don't want things to wait forever now do we?
except:
	pass

__version__ = "0.1.0"

class PyCDDB:
    def __init__(self, cddb_server = 'http://freedb.freedb.org/~cddb/cddb.cgi',
                 app = "PyCDDB", version = __version__):
        self.cddb_server = cddb_server
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.app = app
        self.version = version
        self.protocol = 5
        self.code = 0

    def status(self):
        return self.code

    def message(self):
        if self.code == 0:
            return ""
        elif self.code == 200:
            return "Found exact match"
        elif self.code == 202:
            return "No match found"
        elif self.code == 210:
            return "Ok"
        elif self.code == 211:
            return "Found inexact matches"
        elif self.code == 401:
            return "Specified CDDB entry not found"
        elif self.code == 402:
            return "Server error"
        elif self.code == 403:
            return "Database entry is corrupt"
        elif self.code == 409:
            return "No handshake"

    def query(self, discid):
        if discid != "":
            result = []
            self.track_offset = map(string.atoi, string.split(discid)[2:-1])
            self.disc_length = string.atoi(string.split(discid)[-1:][0]) * 75
            query = urllib.quote_plus(string.rstrip(discid))
            url = "%s?cmd=cddb+query+%s&hello=%s+%s+%s+%s&proto=%d" % \
                  (self.cddb_server, query, self.user, self.host, self.app,
                   self.version, self.protocol)
            response = urllib.urlopen(url)
            header = response.readline()
            if re.match("[0-9]+.*", header):
                self.code = string.atoi(string.split(header, ' ', 1)[0])
                if self.code == 200: # Exact match
                    info = string.split(header, ' ', 3)
                    result.append( { 'category': info[1], 'disc_id': info[2], 'title': info[3] } )
                elif self.code == 210 or self.code == 211: # Multiple exact mattches or inexact match
                    line = string.rstrip(response.readline())
                    while line != ".":
                        info = string.split(line, ' ', 2)
                        result.append( { 'category': info[0], 'disc_id': info[1], 'title': info[2] } )
                        line = string.rstrip(response.readline())

            return result

    def read(self, query_item):
        result = {}
        url = "%s?cmd=cddb+read+%s+%s&hello=%s+%s+%s+%s&proto=%d" % \
              (self.cddb_server, query_item['category'], query_item['disc_id'],
               self.user, self.host, self.app, self.version, self.protocol)
        response = urllib.urlopen(url)
        header = response.readline()
        self.code = string.atoi(string.split(header, ' ', 1)[0])
        if self.code == 210:
            re_indexed_key = re.compile("([^=0123456789]+)([0-9]+)=(.*)")
            re_key = re.compile("([^=]+)=(.*)")
            for line in response.readlines():
                line = string.rstrip(line)
                m = re_indexed_key.match(line)
                if m:
                    (key, index, data) = m.groups()
                    if result.has_key(key):
                        result[key].append(data)
                    else:
                        result[key] = []
                        result[key].append(data)
                else:
                    m = re_key.match(line)
                    if m:
                        (key, data) = m.groups()
                        result[key] = data
        return result
