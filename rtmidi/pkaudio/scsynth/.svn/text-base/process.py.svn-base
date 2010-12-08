#!/usr/bin/env python
#
#   Copyright (C) 2006 by Patrick Stinson                                 
#   patrickkidd@gmail.com                                                 
#                                                                         
#   This program is free software; you can redistribute it and/or modify  
#   it under the terms of the GNU General Public License as published by  
#   the Free Software Foundation; either version 2 of the License, or     
#   (at your option) any later version.                                   
#                                                                         
#   This program is distributed in the hope that it will be useful,       
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
#   GNU General Public License for more details.                          
#                                                                         
#   You should have received a copy of the GNU General Public License     
#   along with this program; if not, write to the                         
#   Free Software Foundation, Inc.,                                       
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.  
#

"""
Control an scsynth process.

What are we trying to do here?
"""

import os
import time
import signal

if os.name == 'nt':
    import subprocess
else:
    import popen2


def is_alive(ret):
    if os.name == 'nt':
        return ret is None
    else:
        return ret == -1


class _Instance:
    """ Controls a running scsynth process,. Is this really necessary? """
    def __init__(self, proc):
        self.proc = proc

    def isAlive(self):
        return is_alive(self.proc.poll())

    def kill(self):
        if os.name == 'nt':
            print 'Can\'t kill processes on windows!'
        else:
            os.kill(self.proc.pid, signal.SIGKILL)


def start_local(exe='scsynth',
                exedir='/Applications/SuperCollider',
                port=57110,
                inputs=2, outputs=2, samplerate=48000,
                verbose=False):
    """ Start an return a local scsynth process. """
    fmt = '%(exe)s -u %(port)s -i %(inputs)s -o %(outputs)s'
    cmd = fmt % locals()
    fulldir = exedir and os.path.isdir(exedir)
    if fulldir:
        cmd = os.path.join(exedir, cmd)

    if verbose:
        print ""
        print "... ... Starting Supercollider Server ... ..."
        print ""
        print cmd

    if fulldir:
        _cwd = os.getcwd()
        os.chdir(exedir)

    proc = None
    if os.name == 'nt':
        proc = subprocess.Popen(cmd)
    else:
        proc = popen2.Popen4(cmd)

    if fulldir:
        os.chdir(_cwd)
    time.sleep(.5)

    ret = proc.poll()
    if not is_alive(ret):
        raise OSError('Could not start scsynth, error %i' % ret)
    return _Instance(proc)


def test():
    if os.name == 'nt':
        instance = start_local(exedir='C:\SC3')
    else:
        instance = start_local()
    print 'killing'
    instance.kill()


if __name__ == '__main__':
    test()

